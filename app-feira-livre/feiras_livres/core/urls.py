from django.urls import path
from core import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('feiras/', views.feiras_view, name='feiras'),
    path('feiras/', views.feiras_view, name='feiras'),
    path('feiras/<int:feira_id>/', views.feira_detalhes_view, name='feira_detalhes'),

]
