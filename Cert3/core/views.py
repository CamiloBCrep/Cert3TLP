from django.contrib.auth import logout
from .models import combustible, codigoPlanta, producto
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
import datetime, json
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



def crear_registro(request):
    
    plantas = codigoPlanta.objects.all()
    
    productos_json = json.dumps(list(plantas.values())) 
    
    context = {
        'codigo_plantas': plantas,
        'productos_json': productos_json
    }

    if request.method == 'POST':

        codigo_clave = request.POST.get('cmbCodigo')
        litros = request.POST.get('txtLitros')
        producto_id = request.POST.get('cmbProducto')  # Cambiado a producto_id para evitar confusión con el nombre 'producto'
        
        codigo = codigoPlanta.objects.get(clave=codigo_clave)
        producto_seleccionado = producto.objects.get(id=producto_id)  # Obtener el objeto producto
        
        now = datetime.datetime.now()

        if now.hour < 6:
            turno = 'MM'
        elif now.hour < 12:
            turno = 'AM'
        else:
            turno = 'PM'

        if not codigo or not litros or not producto_seleccionado:
            messages.error(request, 'Por favor completa todos los campos del formulario.')
        else:
            combust = combustible(
                codigo=codigo,
                litros=litros,
                producto=producto_seleccionado,  # Asignar el objeto producto obtenido
                operario=request.user,
                turno=turno
            )
            
            combust.save()

            messages.success(request, '¡El registro se ha creado exitosamente!')
            return redirect('home')  # Ajusta esta redirección según tu configuración de URLs

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
    

    # Verificar que el usuario actual sea el operario del registro
    if registro.operario != request.user:
        return redirect('listar_registros')

    if request.method == 'POST':
        litros = request.POST.get('txtLitros')
        codigo_clave = request.POST.get('cmbCodigo')
        producto = request.POST.get('cmbProducto')

        # Obtener el objeto codigoPlanta correspondiente a la clave
        codigo = codigoPlanta.objects.get(clave=codigo_clave)
        
        # Validaciones adicionales según tus requisitos
        if litros:
            registro.litros = litros

        # Asignar el objeto codigoPlanta al campo codigo del registro
        registro.codigo = codigo
        registro.producto = producto
        registro.fecha_modificacion = timezone.now()    
        registro.usuario_modificador = request.user

        registro.save()
        return redirect('listar_registros')

    context = {
        'codigo_plantas': plantas,
        'registro': registro,
    }
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