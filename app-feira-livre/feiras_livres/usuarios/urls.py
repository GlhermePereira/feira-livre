from django.urls import path
from .views import RegisterView, MeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import login_view, dashboard_view

app_name = 'usuarios' 
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    #path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', login_view, name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
