from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # sem 'usuarios/' prefixado
    path('', include('core.urls')),
    # redirecionar raiz para login (Django templates)
    path('', lambda request: redirect('usuarios:login')),
    
    ]
