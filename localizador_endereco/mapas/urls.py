from django.urls import path
from . import views

urlpatterns = [
    path('', views.localizar_endereco, name='localizar_endereco'),
]
