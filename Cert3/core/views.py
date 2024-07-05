from django.contrib.auth import logout
from .models import nuevo_proyecto, combustible
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
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

def new_proyecto(request):
    if(request.POST):
        #capturar datos desde el formulario
        estudiante = request.POST['txtEstudiante']
        proy = request.POST['txtProyecto']
        tema = request.POST['txtTema']

        #validaciones de reglas de negocio

        #construir y cargar el objeto con los datos del form
        proyecto = nuevo_proyecto(estudiante=estudiante, proy=proy, tema=tema)


        proyecto.save()
    return render(request, 'core/proyecto.html')

def listar_proyectos(request):
    # Obtener todos los proyectos de la base de datos
    data = nuevo_proyecto.objects.all()
    context = {'proyectos': data}
    # Pasar los proyectos al contexto para que estén disponibles en la plantilla
    return render(request, 'core/home.html', context)

def crear_registro(request):
    codigo = request.POST[]
    litros = request.POST[]
    fecha_hora = request.POST[]
    operario = request.POST[]
    turno = request.POST[]
    nuevo_registro = combustible(codigo=codigo,litros=litros,fecha_hora=fecha_hora,operario=operario,tuno=turno)
    nuevo_registro.save()
    return render(render, 'core/proyecto.html')