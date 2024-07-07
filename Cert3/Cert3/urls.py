"""
URL configuration for Cert3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path ('login/', views.login_view, name="login_view"),  
    path('accounts/',  include('django.contrib.auth.urls')),  
    path('logout/', views.exit, name="exit" ),
    path('nuevoRegistro/', views.crear_registro, name="crear_registro"),
    path('editarRegistro/<int:pk>/', views.editar_registro, name='editar_registro'),
    path('eliminarRegistro/<int:pk>/', views.eliminar_registro, name='eliminar_registro'),
    path('home/', views.listar_registros, name='listar_registros' ),   
    path('api/', include('restAPI.urls')),
]
