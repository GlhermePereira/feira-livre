# Feira Livre 🥬🧺

Sistema web desenvolvido com Django para gerenciamento e visualização de feiras livres na cidade de Praia Grande.

## 🔧 Funcionalidades Principais

- Cadastro e autenticação de usuários com JWT
- Registro de feiras, barracas e presenças
- Busca de feiras por endereço (via Nominatim)
- Visualização de feiras em mapa com Leaflet.js
- Cadastro de barracas por feirantes
- Visualização de detalhes das feiras
- Autocomplete de nomes de feiras

## 🗂️ Estrutura do Projeto

```
feiras_livres/
├── core/               # Lógica principal do sistema (feiras, barracas, mapas)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/core/
├── usuarios/           # Autenticação e usuários
│   ├── models.py       # Modelo customizado de usuário
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── serializers.py
├── feiras_livres/      # Configuração geral do projeto Django
│   ├── settings.py
│   ├── urls.py
├── manage.py
└── db.sqlite3
```

## 🔐 Autenticação

- Login com email e senha (modelo customizado `Usuario`)
- Autenticação via JWT (`SimpleJWT`)
- Proteção de rotas com `@login_required` (HTML) e `IsAuthenticated` (API)

## 📄 Endpoints de Autenticação

| Método | Endpoint         | Descrição                  |
|--------|------------------|----------------------------|
| POST   | `/api/token/`    | Obter token JWT            |
| POST   | `/api/token/refresh/` | Renovar token JWT      |
| GET    | `/me/`           | Dados do usuário autenticado |

## 📍 Funcionalidade de Mapa

- Mapa interativo com Leaflet.js
- Detecção automática da localização do usuário
- Marcação de feiras e detalhes geográficos
- Autocomplete de nomes de feiras

## 🧪 Como Executar Localmente

```bash
git clone https://github.com/seu-usuario/feiras-livres.git
cd feiras-livres

# Crie e ative um ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Migre o banco de dados
python manage.py migrate

# Crie um superusuário para acessar o admin
python manage.py createsuperuser

# Rode o servidor local
python manage.py runserver
```

## ✅ Tecnologias Utilizadas

- Django 5.x
- Django REST Framework
- SimpleJWT
- Bootstrap 5
- Leaflet.js
- SQLite (desenvolvimento)
- API ViaCEP e Nominatim (geolocalização)

## 📂 Templates

- **base.html**: layout com navbar, footer e blocos
- **dashboard.html**: mapa + busca interativa
- **login.html**: autenticação do usuário
- **register.html**: formulário de cadastro com preenchimento automático de endereço via CEP
- **feira_detalhes.html**: informações detalhadas e mapa da feira

## 📸 Imagens e Layout

O sistema é responsivo e mobile-friendly, com base em Bootstrap 5. Mapa responsivo e interação via JavaScript.

## 🤝 Licença

Projeto acadêmico sem fins comerciais. Todos os direitos reservados © 2025.

---

Desenvolvido por Guilherme Pereira
