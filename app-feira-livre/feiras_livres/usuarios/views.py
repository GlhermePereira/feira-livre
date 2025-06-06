from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UsuarioSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioCreateForm

Usuario = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "email": request.user.email,
            "nome": f"{request.user.first_name} {request.user.last_name}",
            "telefone": request.user.telefone,
            "endereco": request.user.endereco,
        })
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")

        user = authenticate(request, username=email, password=senha)  # <- CORRIGIDO AQUI
        if user:
            login(request, user)
            return redirect('/dashboard/')  # ou outra view
        else:
            messages.error(request, "E-mail ou senha inválidos.")

    return render(request, 'usuarios/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'usuarios/dashboard.html')



def cadastro_view(request):
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios:login')
    else:
        form = UsuarioCreateForm()

    return render(request, 'usuarios/register.html', {'form': form})

