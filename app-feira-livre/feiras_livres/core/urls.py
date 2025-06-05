from django.urls import path
from core import views

urlpatterns = [
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('feiras/', views.feiras_view, name='feiras'),  # sua view das feiras

]
