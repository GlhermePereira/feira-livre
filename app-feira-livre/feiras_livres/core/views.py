from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UsuarioCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from .models import Feira
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
logger = logging.getLogger(__name__)


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


@csrf_exempt
def buscar_feiras_por_endereco(request):
    endereco = request.GET.get('endereco', '').strip()
    if not endereco:
        return JsonResponse({"erro": "Endereço não fornecido."}, status=400)

    if "Praia Grande" not in endereco:
        endereco += ", Praia Grande"

    try:
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': endereco,
            'format': 'json',
            'limit': 1,
        }

        response = requests.get(url, params=params, headers={'User-Agent': 'feira-livre-django'})
        data = response.json()

        if response.status_code != 200 or not data:
            return JsonResponse({"erro": "Endereço não encontrado."}, status=400)

        print("🔎 Consulta Nominatim:", data)  # <- CORRIGIDO AQUI

        geo = data[0]
        lat = float(geo['lat'])
        lon = float(geo['lon'])

        feiras = Feira.objects.filter(cidade__iexact="Praia Grande", ativa=True)

        resultado = []
        for feira in feiras:
            if feira.latitude and feira.longitude:
                resultado.append({
                    'id': feira.id,
                    'nome': feira.nome,
                    'endereco': feira.endereco,
                    'bairro': feira.bairro,
                    'latitude': float(feira.latitude),
                    'longitude': float(feira.longitude),
                })

        return JsonResponse(resultado, safe=False)

    except Exception as e:
        logger.exception("Erro ao buscar feiras por endereço")
        return JsonResponse({"erro": "Erro interno no servidor."}, status=500)


def feiras_view(request):
    # exemplo simples
    return render(request, 'core/feiras.html')

def buscar_feiras(request):
    termo = request.GET.get('q', '')
    feiras = Feira.objects.filter(nome__icontains=termo)[:10]
    resultados = [{'id': feira.id, 'nome': feira.nome, 'endereco': feira.endereco} for feira in feiras]
    return JsonResponse(resultados, safe=False)


# views.py
def listar_todas_feiras(request):
    feiras = Feira.objects.filter(ativa=True)
    return JsonResponse([
        {
            'id': f.id,
            'nome': f.nome,
            'endereco': f.endereco,
            'bairro': f.bairro,
            'latitude': float(f.latitude),
            'longitude': float(f.longitude),
        } for f in feiras if f.latitude and f.longitude
    ], safe=False)
