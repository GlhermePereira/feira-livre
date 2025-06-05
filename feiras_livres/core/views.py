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
def feiras_view(request):
    feiras = Feira.objects.filter(ativa=True)  # Só mostrar feiras ativas
    feira_filter = FeiraFilter(request.GET, queryset=feiras)
    return render(request, 'core/feiras.html', {
        'filter': feira_filter,
        'feiras': feira_filter.qs,
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


