from django.urls import path
from core import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('feiras/', views.feiras_view, name='feiras'),
    path('feiras/<int:feira_id>/', views.feira_detalhes_view, name='feira_detalhes'),

    # Busca por nome (autocomplete)
    path('api/feiras/autocomplete/', views.buscar_feiras, name='buscar_feiras'),

    # Busca por geolocalização (endereço)
    path('api/feiras/geolocalizacao/', views.buscar_feiras_por_endereco, name='buscar_feiras_geolocalizacao'),
    path('api/feiras/todas/', views.listar_todas_feiras, name='listar_todas_feiras'),

]
