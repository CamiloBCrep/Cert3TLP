from django.contrib.auth import logout
from .models import nuevo_proyecto, combustible
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import datetime
# Create your views here.
def home(request):
    title = "inicio"
    data={
        "title":title
    }
    return render(request, 'core/home.html', data)
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir a la página deseada después de iniciar sesión
            return redirect('registration/home.html')
        else:
            # Mostrar un mensaje de error si las credenciales son incorrectas
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'registration/login.html')

def exit(request):
    logout(request)
    return redirect('home')

def crear_registro(request):
    if request.method == 'POST':

        codigo = request.POST.get('cmbCodigo')
        litros = request.POST.get('txtLitros')
        
        now = datetime.datetime.now()

        if now.hour < 6:
            turno = 'MM'
        elif now.hour < 12:
            turno = 'MM'
        else:
            turno = 'PM'

        if not name or not category_type:
            messages.error(request, 'Por favor completa todos los campos del formulario.')
        else:
            combustible.objects.Create(
                codigo=codigo,litros=litros,
                fecha_hora=fecha_hora,
                operario=operario,
                tuno=turno
            )
            
            messages.success(request, '¡La el registro se ha creado exitosamente!')
            return redirect('core/home.html')
    return render(render, 'core/formulario.html')

def listar_registros(request):
    # Obtener todos los proyectos de la base de datos
    data = combustible.objects.all()
    context = {'registros': data}
    # Pasar los proyectos al contexto para que estén disponibles en la plantilla
    return render(request, 'core/home.html', context)