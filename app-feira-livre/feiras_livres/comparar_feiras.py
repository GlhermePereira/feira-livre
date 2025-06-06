import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feiras_livres.settings')
import django
django.setup()
from core.models import Feira
# Lista de feiras fornecida
feiras_fornecidas = [
    # Terça-feira
    {"nome": "Feira Sítio do Campo - Terça-Feira", "bairro": "Sítio do Campo", "dias_funcionamento": "ter", "endereco": "Rua Prof. Olavo Paula Borges"},
    {"nome": "Feira Solemar - Terça-Feira", "bairro": "Solemar", "dias_funcionamento": "ter", "endereco": "Rua Júlio Secco de Carvalho"},
    {"nome": "Feira Antártica - Terça-Feira", "bairro": "Antártica", "dias_funcionamento": "ter", "endereco": "Av João Batista de Siqueira"},
    {"nome": "Feira Maracanã - Terça-Feira", "bairro": "Maracanã", "dias_funcionamento": "ter", "endereco": "Rua Paulino Borrelli"},
    # Quarta-feira
    {"nome": "Feira Canto do Forte - Quarta-Feira", "bairro": "Canto do Forte", "dias_funcionamento": "qua", "endereco": "Av. Maurício José Cardoso"},
    {"nome": "Feira Tupi - Quarta-Feira", "bairro": "Tupi", "dias_funcionamento": "qua", "endereco": "Rua Guaicurus"},
    {"nome": "Feira Mirim - Quarta-Feira", "bairro": "Mirim", "dias_funcionamento": "qua", "endereco": "Rua Martiniano Jose das Neves"},
    # Quinta-feira
    {"nome": "Feira Quietude - Quinta-Feira", "bairro": "Quietude", "dias_funcionamento": "qui", "endereco": "Rua Alvaro Silva Junior"},
    {"nome": "Feira Samambaia - Quinta-Feira", "bairro": "Samambaia", "dias_funcionamento": "qui", "endereco": "Rua Dos Ipês"},
    # Sexta-feira
    {"nome": "Feira Canto do Forte - Sexta-Feira", "bairro": "Canto do Forte", "dias_funcionamento": "sex", "endereco": "Rua Xixová"},
    {"nome": "Feira Guilhermina - Sexta-Feira", "bairro": "Guilhermina", "dias_funcionamento": "sex", "endereco": "Rua Argentina"},
    {"nome": "Feira Vila Sônia - Sexta-Feira", "bairro": "Vila Sônia", "dias_funcionamento": "sex", "endereco": "Rua Arnaldo Augusto Baptista"},
    # Sábado
    {"nome": "Feira Boqueirão - Sábado", "bairro": "Boqueirão", "dias_funcionamento": "sab", "endereco": "Rua José Carlos de Oliveira"},
    {"nome": "Feira Mirim - Sábado", "bairro": "Mirim", "dias_funcionamento": "sab", "endereco": "Rua Astério Genário"},
    {"nome": "Feira Real - Sábado", "bairro": "Real", "dias_funcionamento": "sab", "endereco": "Rua Azaléia"},
    {"nome": "Feira Tupiry - Sábado", "bairro": "Tupiry", "dias_funcionamento": "sab", "endereco": "Rua Ariovaldo Augusto de Oliveira"},
    # Domingo
    {"nome": "Feira Sítio do Campo - Domingo", "bairro": "Sítio do Campo", "dias_funcionamento": "dom", "endereco": "Av. Trabalhadores"},
    {"nome": "Feira Anhanguera - Domingo", "bairro": "Anhanguera", "dias_funcionamento": "dom", "endereco": "Rua Clovis Batista dos Santos"},
    {"nome": "Feira Caiçara - Domingo", "bairro": "Caiçara", "dias_funcionamento": "dom", "endereco": "Rua Flausina de Oliveira Rosa"},
    {"nome": "Feira Samambaia - Domingo", "bairro": "Samambaia", "dias_funcionamento": "dom", "endereco": "Rua Dos Ipês"},
    {"nome": "Feira Ribeirópolis - Domingo", "bairro": "Ribeirópolis", "dias_funcionamento": "dom", "endereco": "Av. Dr. Esmeraldo S. Tarquínio C. Filho"}
]

# Comparação com as feiras do banco de dados
from core.models import Feira

for feira in feiras_fornecidas:
    # Tentar localizar a feira no banco com o nome e o bairro
    try:
        feira_banco = Feira.objects.get(nome=feira['nome'], bairro=feira['bairro'])
        print(f"A feira '{feira['nome']}' já existe no banco.")
    except Feira.DoesNotExist:
        # Criar nova feira
        nova_feira = Feira.objects.create(
            nome=feira['nome'],
            endereco=feira['endereco'],
            bairro=feira['bairro'],
            cidade='Praia Grande',
            dias_funcionamento=feira['dias_funcionamento'],
            horario_abertura='06:00',
            horario_fechamento='13:00',
            ativa=True
        )
        print(f"Feira '{feira['nome']}' criada com sucesso.")
