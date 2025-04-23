from django.shortcuts import render
from django.shortcuts import render
import requests

def localizar_endereco(request):
    endereco = request.GET.get('endereco', '')
    coordenadas = None

    if endereco:
        cidade = 'Praia Grande, SP'
        consulta = f"{endereco}, {cidade}"
        url = f"https://nominatim.openstreetmap.org/search"
        params = {
            'q': consulta,
            'format': 'json',
            'limit': 1,
        }

        response = requests.get(url, params=params, headers={'User-Agent': 'localizador-django'})
        dados = response.json()

        if dados:
            coordenadas = {
                'lat': dados[0]['lat'],
                'lon': dados[0]['lon'],
                'endereco': dados[0]['display_name']
            }

    return render(request, 'mapas/mapa.html', {'coordenadas': coordenadas})
