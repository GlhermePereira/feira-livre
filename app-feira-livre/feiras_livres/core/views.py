from django.shortcuts import render, redirect, get_object_or_404
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
from django.db.models import Q
logger = logging.getLogger(__name__)



@login_required
def feira_detalhes_view(request, feira_id):
    # Recupera a feira com o ID fornecido
    feira = get_object_or_404(Feira, id=feira_id)
    return render(request, 'core/feira_detalhes.html', {'feira': feira})
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

from django.http import JsonResponse
from .models import Feira


def autocomplete_feiras(request):
    termo = request.GET.get('q', '').strip()
    if not termo:
        return JsonResponse([])  # Retorna uma lista vazia se o termo estiver vazio

    # Filtra as feiras pelo nome, endereço ou bairro
    feiras = Feira.objects.filter(
        nome__icontains=termo
    ) | Feira.objects.filter(
        endereco__icontains=termo
    ) | Feira.objects.filter(
        bairro__icontains=termo
    )

    resultados = []
    for feira in feiras:
        resultados.append({
            'nome': feira.nome,
            'endereco': feira.endereco,
            'bairro': feira.bairro,
        })

    return JsonResponse(resultados, safe=False)

def feiras_view(request):
    # exemplo simples
    return render(request, 'core/feiras.html')


def buscar_feiras(request):
    logger.info("Iniciando busca por feiras...")

    # Obtém o parâmetro 'q' da URL (ex: /api/feiras/autocomplete/?q=Boqueirão)
    termo = request.GET.get('q', '').strip()
    logger.debug(f"Termo recebido na query: '{termo}'")

    if not termo:
        logger.warning("Nenhum termo foi informado na busca.")
        return JsonResponse({'erro': 'Parâmetro de busca ausente'}, status=400)

    try:
        # Busca feiras cujo bairro corresponda exatamente (ignorando maiúsculas/minúsculas)
        feiras = Feira.objects.filter(
        Q(nome__icontains=termo) | Q(bairro__icontains=termo) | Q(endereco__icontains=termo)
        )       
        logger.info(f"{feiras.count()} feira(s) encontradas para o bairro '{termo}'.")

        resultados = [
            {'id': feira.id, 'nome': feira.nome, 'endereco': feira.endereco}
            for feira in feiras
        ]

        logger.debug(f"Resultados formatados: {resultados}")

        return JsonResponse(resultados, safe=False)

    except Exception as e:
        logger.error(f"Erro durante a busca: {e}")
        return JsonResponse({'erro': 'Erro interno do servidor'}, status=500)



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

    def todas_feiras(request):
     termo = request.GET.get('q', '').strip()

    # Se o termo for vazio, retorna todas as feiras
    if not termo:
        feiras = Feira.objects.all()
    else:
        # Filtra as feiras pelo nome, endereço ou bairro
        feiras = Feira.objects.filter(
            nome__icontains=termo
        ) | Feira.objects.filter(
            endereco__icontains=termo
        ) | Feira.objects.filter(
            bairro__icontains=termo
        )

    resultados = [
        {
            'nome': feira.nome,
            'endereco': feira.endereco,
            'bairro': feira.bairro
        }
        for feira in feiras
    ]

    return JsonResponse(resultados, safe=False)

