from django.contrib.auth import logout
from .models import combustible,CODIGO_CHOICES
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
import datetime
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
    
    context = {
        'CODIGO_CHOICES': CODIGO_CHOICES,
    }

    if request.method == 'POST':

        codigo = request.POST.get('cmbCodigo')
        litros = request.POST.get('txtLitros')
        
        now = datetime.datetime.now()

        if now.hour < 6:
            turno = 'MM'
        elif now.hour < 12:
            turno = 'AM'
        else:
            turno = 'PM'

        if not codigo or not litros:
            messages.error(request, 'Por favor completa todos los campos del formulario.')
        else:
            combust = combustible(
                codigo=codigo,
                litros=litros,
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

    # Verificar que el usuario actual sea el operario del registro
    if registro.operario != request.user:
        # Puedes manejar el acceso no autorizado como desees
        return redirect('listar_registros')

    if request.method == 'POST':
        litros = request.POST.get('txtLitros')
        codigo = request.POST.get('cmbCodigo')

        # Validaciones adicionales según tus requisitos
        if litros:
            registro.litros = litros
        if codigo:
            registro.codigo = codigo

        registro.save()
        return redirect('listar_registros')

    context = {
        'CODIGO_CHOICES': CODIGO_CHOICES,
        'registro': registro,
    }
    return render(request, 'core/formularioEditarRegistro.html', context)