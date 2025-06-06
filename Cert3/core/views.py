from django.contrib.auth import logout
from .models import combustible, codigoPlanta, producto
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
import datetime, json
from django.conf import settings
from slack_sdk import WebClient
from django.db.models import Sum
import requests


# Create your views here.
def home(request):
    title = "inicio"
    data={
        "title":title
    }
    return redirect('listar_registros')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir a la página deseada después de iniciar sesión
            return redirect('home')
        else:
            # Mostrar un mensaje de error si las credenciales son incorrectas
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

            messages.info(request, 'Este es un mensaje de prueba.')
    return render(request, 'home')

def exit(request):
    logout(request)
    return redirect('home')

def enviar_notificacion_slack(registro):
    try:
        webhook_url = settings.SLACK_WEBHOOK_URL

        # Construir el mensaje en formato JSON
        mensaje = {
            "text": f"{registro.fecha_hora.strftime('%d-%m-%Y %H:%M')} | {registro.codigo.clave} – Nuevo Registro de Producción – "

                    f"{registro.producto.nombre} {registro.litros} litros registrados | "
                    f"Total Almacenado: {calcular_total_almacenado()} litros"
        }

        # Enviar mensaje a Slack usando requests
        response = requests.post(webhook_url, json=mensaje)

        if response.status_code == 200:
            print("Notificación enviada exitosamente a Slack.")
        else:
            print(f"Error al enviar notificación a Slack. Código de error: {response.status_code}")

    except Exception as e:
        print(f"Error al enviar notificación a Slack: {str(e)}")

def calcular_total_almacenado():
    # Calcular el total almacenado sumando todos los litros de los registros
    registros = combustible.objects.filter(eliminado=False)
    total = registros.aggregate(Sum('litros'))['litros__sum'] or 0
    return total

def crear_registro(request):
    plantas = codigoPlanta.objects.all()

    # Crear una lista para almacenar los datos de cada código de planta con sus productos
    plantas_json = []
    for planta in plantas:
        # Obtener los productos asociados a cada código de planta y convertirlos a listas de Python
        productos = list(planta.productos.all().values())
        
        # Crear un diccionario con la información del código de planta y sus productos
        planta_data = {
            'clave': planta.clave,
            'descripcion': planta.descripcion,
            'productos': productos
        }
        
        # Agregar el diccionario a la lista de plantas en formato JSON
        plantas_json.append(planta_data)
    
    # Convertir la lista de plantas en formato JSON
    plantas_json_str = json.dumps(plantas_json)
    total_almacenado = calcular_total_almacenado() #slack aqui

    context = {
        'total_almacenado': total_almacenado
    }

    context = {
        'codigo_plantas': plantas,
        'plantas_json': plantas_json_str
    }

    if request.method == 'POST':
        codigo_clave = request.POST.get('cmbCodigo')
        litros = request.POST.get('txtLitros')
        producto_id = request.POST.get('cmbProducto')  # Debe ser el id del producto

        try:
            codigo_planta = codigoPlanta.objects.get(clave=codigo_clave)
            producto_seleccionado = producto.objects.get(id=producto_id)  # Obtener el producto por su id

            if not codigo_planta or not litros or not producto_seleccionado:
                messages.error(request, 'Por favor completa todos los campos del formulario.')
            else:
                now = datetime.datetime.now()
                if now.hour < 6:
                    turno = 'MM'
                elif now.hour < 12:
                    turno = 'AM'
                else:
                    turno = 'PM'

                combust = combustible(
                    codigo=codigo_planta,
                    litros=litros,
                    producto=producto_seleccionado,
                    operario=request.user,
                    turno=turno
                )
            
                combust.save()
                enviar_notificacion_slack(combust) #slack aqui


                messages.success(request, '¡El registro se ha creado exitosamente!')
                return redirect('home')  # Redirigir a la página de inicio

        except codigoPlanta.DoesNotExist:
            messages.error(request, 'El código de planta seleccionado no es válido.')
        except producto.DoesNotExist:
            messages.error(request, 'El producto seleccionado no es válido.')

    return render(request, 'core/formulario.html', context)


def listar_registros(request):
        # Obtener todos los registros de la base de datos
    registros = combustible.objects.all()

    # Obtener el parámetro de filtro de la URL
    filtro = request.GET.get('filtro', None)

    # Filtrar los registros según el parámetro
    if filtro == 'mis_registros':
        registros = registros.filter(operario=request.user)

    context = {
        'registros': registros,
        'filtro_actual': filtro,
    }

    return render(request, 'core/home.html', context)

def editar_registro(request, pk):
    registro = get_object_or_404(combustible, pk=pk)
    plantas = codigoPlanta.objects.all()

    # Crear una lista para almacenar los datos de cada código de planta con sus productos
    plantas_json = []
    for planta in plantas:
        # Obtener los productos asociados a cada código de planta y convertirlos a listas de Python
        productos = list(planta.productos.all().values())
        
        # Crear un diccionario con la información del código de planta y sus productos
        planta_data = {
            'clave': planta.clave,
            'descripcion': planta.descripcion,
            'productos': productos,
        }
        
        # Agregar el diccionario a la lista de plantas en formato JSON
        plantas_json.append(planta_data)
    
    # Convertir la lista de plantas en formato JSON
    plantas_json_str = json.dumps(plantas_json)

    context = {
        'codigo_plantas': plantas,
        'plantas_json': plantas_json_str,
        'registro': registro
    }

    # Verificar que el usuario actual sea el operario del registro
    if registro.operario != request.user:
        return redirect('listar_registros')

    if request.method == 'POST':
        litros = request.POST.get('txtLitros')
        codigo_clave = request.POST.get('cmbCodigo')
        producto_id = request.POST.get('cmbProducto')

        # Validar que los campos recibidos no estén vacíos
        if litros and codigo_clave and producto_id:
            try:
                codigo = codigoPlanta.objects.get(clave=codigo_clave)
                producto_seleccionado = producto.objects.get(id=producto_id)

                # Actualizar los campos del registro existente
                registro.litros = litros
                registro.codigo = codigo
                registro.producto = producto_seleccionado
                registro.fecha_modificacion = timezone.now()
                registro.usuario_modificador = request.user

                registro.save()

                messages.success(request, '¡El registro se ha actualizado exitosamente!')
                return redirect('listar_registros')

            except codigoPlanta.DoesNotExist:
                messages.error(request, 'El código de planta seleccionado no es válido.')
            except producto.DoesNotExist:
                messages.error(request, 'El producto seleccionado no es válido.')
        else:
            messages.error(request, 'Por favor completa todos los campos del formulario.')

    return render(request, 'core/formularioEditarRegistro.html', context)

def eliminar_registro(request, pk):
    
    registro = get_object_or_404(combustible, pk=pk)

    if request.method == 'POST':
        registro.eliminar()  # Llamar al método de eliminación lógica
        registro.fecha_modificacion = timezone.now()
        registro.usuario_modificador = request.user
        registro.save()
        return redirect('listar_registros')

    context = {
        'registro': registro
    }
    return render(request, 'core/eliminarRegistro.html', context)