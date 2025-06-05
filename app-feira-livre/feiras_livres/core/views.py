from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UsuarioCreateForm
from django.contrib import messages

def cadastro_view(request):
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect('login')  # URL do login
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = UsuarioCreateForm()
    return render(request, 'core/cadastro.html', {'form': form})

@login_required
def feira_detalhes_view(request, feira_id):
    feira = get_object_or_404(Feira, id=feira_id)
    barracas = feira.barracas.all()  # usando related_name 'barracas'

    return render(request, 'core/feira_detalhes.html', {
        'feira': feira,
        'barracas': barracas,
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feiras')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})



def feiras_view(request):
    # exemplo simples
    return render(request, 'core/feiras.html')


