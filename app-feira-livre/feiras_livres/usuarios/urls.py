from django.urls import path
from .views import RegisterView, MeView, login_view, dashboard_view, cadastro_view, logout_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView  # no topo do arquivo
app_name = 'usuarios'
from . import views  
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    # Cadastro via formulário HTML
    path('cadastro/', cadastro_view, name='cadastro'),

    # Login via formulário HTML
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # <- aqui está a URL de logout
    # Login via API JWT (separar em /api/login/ se quiser manter ambos)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
# de:
    path('dashboard/', dashboard_view, name='dashboard'),
]
