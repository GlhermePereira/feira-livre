import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "feiras_livres.settings")
import requests

import django
django.setup()

from core.models import Feira  # Agora, importa o modelo de Feira corretamente
def obter_coordenadas(endereco):
    endereco_completo = f"{endereco}, Praia Grande, SP, Brasil"
    url = "https://nominatim.openstreetmap.org/search"
    params = {'q': endereco_completo, 'format': 'json', 'limit': 1}
    
    try:
        resposta = requests.get(url, params=params, headers={'User-Agent': 'feira-livre'})
        dados = resposta.json()
        
        if resposta.status_code == 200 and dados:
            lat = float(dados[0]['lat'])
            lon = float(dados[0]['lon'])
            return lat, lon
        else:
            print(f"Erro ao buscar coordenadas para {endereco_completo}: {dados}")
            return None, None
    except Exception as e:
        print(f"Erro ao processar a requisição para {endereco_completo}: {e}")
        return None, None

# Função para cadastrar as feiras no banco de dados
def criar_feiras():
    feiras = [
        # Terça-feira
        {'nome': 'Feira Sítio do Campo - Terça-Feira', 'endereco': 'Rua Prof. Olavo Paula Borges', 'bairro': 'Sítio do Campo', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Solemar - Terça-Feira', 'endereco': 'Rua Júlio Secco de Carvalho', 'bairro': 'Solemar', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Antártica - Terça-Feira', 'endereco': 'Av João Batista de Siqueira', 'bairro': 'Antártica', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Maracanã - Terça-Feira', 'endereco': 'Rua Paulino Borrelli', 'bairro': 'Maracanã', 'cidade': 'Praia Grande'},

        # Quarta-feira
        {'nome': 'Feira Canto do Forte - Quarta-Feira', 'endereco': 'Av. Maurício José Cardoso', 'bairro': 'Canto do Forte', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Tupi - Quarta-Feira', 'endereco': 'Rua Guaicurus', 'bairro': 'Tupi', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Mirim - Quarta-Feira', 'endereco': 'Rua Martiniano Jose das Neves', 'bairro': 'Mirim', 'cidade': 'Praia Grande'},

        # Quinta-feira
        {'nome': 'Feira Quietude - Quinta-Feira', 'endereco': 'Rua Alvaro Silva Junior', 'bairro': 'Quietude', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Samambaia - Quinta-Feira', 'endereco': 'Rua Dos Ipês', 'bairro': 'Samambaia', 'cidade': 'Praia Grande'},

        # Sexta-feira
        {'nome': 'Feira Canto do Forte - Sexta-Feira', 'endereco': 'Rua Xixová', 'bairro': 'Canto do Forte', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Guilhermina - Sexta-Feira', 'endereco': 'Rua Argentina', 'bairro': 'Guilhermina', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Vila Sônia - Sexta-Feira', 'endereco': 'Rua Arnaldo Augusto Baptista', 'bairro': 'Vila Sônia', 'cidade': 'Praia Grande'},

        # Sábado
        {'nome': 'Feira Boqueirão - Sábado', 'endereco': 'Rua José Carlos de Oliveira', 'bairro': 'Boqueirão', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Mirim - Sábado', 'endereco': 'Rua Astério Genário', 'bairro': 'Mirim', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Real - Sábado', 'endereco': 'Rua Azaléia', 'bairro': 'Real', 'cidade': 'Praia Grande'},

        # Domingo
        {'nome': 'Feira Sítio do Campo - Domingo', 'endereco': 'Av. Trabalhadores', 'bairro': 'Sítio do Campo', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Anhanguera - Domingo', 'endereco': 'Rua Clovis Batista dos Santos', 'bairro': 'Anhanguera', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Caiçara - Domingo', 'endereco': 'Rua Flausina de Oliveira Rosa', 'bairro': 'Caiçara', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Samambaia - Domingo', 'endereco': 'Rua Dos Ipês', 'bairro': 'Samambaia', 'cidade': 'Praia Grande'},
        {'nome': 'Feira Ribeirópolis - Domingo', 'endereco': 'Av. Dr. Esmeraldo S. Tarquínio C. Filho', 'bairro': 'Ribeirópolis', 'cidade': 'Praia Grande'},
    ]

    for feira in feiras:
        # Buscar as coordenadas do endereço da feira
        lat, lon = obter_coordenadas(feira['endereco'])
        
        # Se encontrou as coordenadas, cria a feira no banco
        if lat and lon:
            Feira.objects.create(
                nome=feira['nome'],
                endereco=feira['endereco'],
                bairro=feira['bairro'],
                cidade=feira['cidade'],
                latitude=lat,
                longitude=lon,
                dias_funcionamento='ter,qua,qui,sex,sab,dom',  # Exemplo de dias de funcionamento (pode ser ajustado conforme necessário)
                horario_abertura='06:00',
                horario_fechamento='13:00'
            )
            print(f"Feira {feira['nome']} criada com sucesso!")
        else:
            print(f"Erro ao buscar coordenadas para {feira['nome']}")

# Executar a função para criar as feiras
criar_feiras()

