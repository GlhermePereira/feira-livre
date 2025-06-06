from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from .models import Feira
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
logger = logging.getLogger(__name__)



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

    try:
        # Verifica se a cidade já foi fornecida no endereço
        if "Praia Grande" not in endereco:
            endereco += ", Praia Grande"  # Adiciona a cidade apenas se não estiver presente

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

        # Pegando os dados geográficos do endereço consultado
        geo = data[0]
        lat = float(geo['lat'])
        lon = float(geo['lon'])

        # Filtrando as feiras dentro da cidade de Praia Grande
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

        if not resultado:
            return JsonResponse({"erro": "Nenhuma feira encontrada."}, status=404)

        return JsonResponse(resultado, safe=False)

    except Exception as e:
        logger.exception("Erro ao buscar feiras por endereço")
        return JsonResponse({"erro": "Erro interno no servidor."}, status=500)


def feiras_view(request):
    # exemplo simples
    return render(request, 'core/feiras.html')

def buscar_feiras(request):
    termo = request.GET.get('q', '')
    # Filtra feiras que contém o termo exato no nome ou no bairro
    feiras = Feira.objects.filter(bairro__iexact=termo)  # Aqui usamos 'iexact' para uma comparação exata
    resultados = [{'id': feira.id, 'nome': feira.nome, 'endereco': feira.endereco} for feira in feiras]
    return JsonResponse(resultados, safe=False)




def listar_todas_feiras(request):
    feiras = Feira.objects.filter(ativa=True)
    resultado = [
        {
            'id': feira.id,
            'nome': feira.nome,
            'endereco': feira.endereco,
            'bairro': feira.bairro,
            'latitude': float(feira.latitude),
            'longitude': float(feira.longitude),
        }
        for feira in feiras if feira.latitude and feira.longitude
    ]
    return JsonResponse(resultado, safe=False)

