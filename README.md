
# Sistema de Controle de Processos Internos - Django

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python) | ![Django](https://img.shields.io/badge/Django-5.1-green?logo=django)

## Django Python

Um sistema web desenvolvido em Django para gerenciamento de processos internos em empresas, inicialmente adaptado para laboratórios de ótica, mas com arquitetura flexível para outros nichos.

---

## Visão Geral

O projeto consiste em um sistema completo com:

- Autenticação de usuários (login, registro)
- Geração de senhas temporárias com validade controlada
- CRUD para gestão de compras de lentes (modelo atual)
- Controle de permissões por roles
- Templates funcionais para todas as operações básicas

---

## Funcionalidades Principais

### Módulo de Autenticação

- Páginas de login e registro configuradas
- Sistema de senhas temporárias para cadastro
- Validade de 20 minutos (configurável)
- Inativação automática após uso
- Gerenciamento via admin

### Módulo de Processos (Lentes)

- Lançamento de compras de lentes
- Listagem com filtros
- Edição e exclusão de registros
- Modelos adaptáveis para outros nichos

---

## Pré-requisitos

- Python 3.12
- Django 5.1.7
- MySQL (ou outro banco configurável)

---

## Bibliotecas Utilizadas

Lista completa no `requirements.txt`:

```
asgiref==3.8.1
Django==5.1.7
django-livereload-server==0.5.1
django-role-permissions==3.2.0
isort==6.0.1
mysqlclient==2.2.7
python-dateutil==2.9.0.post0
six==1.17.0
sqlparse==0.5.3
tornado==6.4.2
tzdata==2025.1
```

---

## Configuração do Ambiente

### Para Windows

1. Instale Python 3.12 ou superior.

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados no `settings.py`

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o listener livereload:
```bash
python manage.py livereload
```

8. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

### Para Linux

1. Instale Python 3.12 ou superior e pip:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

2. Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Instale dependências do sistema para `mysqlclient`:
```bash
sudo apt install python3-dev default-libmysqlclient-dev build-essential
```

5. Siga os passos 4-8 da configuração para Windows

---

## Configuração para Produção

> Importante: O projeto inclui `django-livereload-server` para desenvolvimento. Para ambientes de produção:

1. Remova a biblioteca:
```bash
pip uninstall django-livereload-server
```

2. Atualize o `requirements.txt` removendo a linha:
```
django-livereload-server==0.5.1
```

3. No `settings.py`, remova:
```python
'livereload',
```
da lista `INSTALLED_APPS` e quaisquer outras configurações relacionadas.

---

## Estrutura do Projeto

```
📦site_controle_processos
├── 📂frontend_site
│   ├── 📂migrations
│   │   ├── 0001_initial.py
│   │   ├── ...
│   ├── 📂static
│   │   └── 📂frontend_site
│   │       ├── 📂css
│   │       │   ├── 📂admin_panel
│   │       │   │   └── admin_panel.css
│   │       │   ├── 📂auth
│   │       │   │   └── registration.css
│   │       │   ├── 📂estoque
│   │       │   │   ├── lancamento_de_lentes.css
│   │       │   │   └── listagem_lancamentos.css
│   │       │   └── global.css
│   │       │
│   │       └── 📂js
│   │           ├── 📂estoque
│   │           │   ├── lancamento_de_lentes.js
│   │           │   └── listagem_lancamentos.js
│   │           └── 📂login_register
│   │               └── login_register.js
│   │
│   ├── 📂templates
│   │   └── 📂frontend_site
│   │       ├── 📂admin_panel
│   │       │   └── admin_panel.html
│   │       ├── 📂auth
│   │       │   ├── login.html
│   │       │   └── register.html
│   │       ├── 📂base
│   │       │   └── base.html
│   │       ├── 📂estoque
│   │       │   ├── lancamento_de_lentes.html
│   │       │   └── listagem_lancamentos.html
│   │       └── 📂registration
│   │           ├── new_password.html
│   │           ├── password_reset.html
│   │           ├── password_reset_complete.html
│   │           └── password_reset_msg.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── aux_function.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
│
├── 📂keygen_temp
│   ├── 📂migrations
│   │   ├── 0001_initial.py
│   │   ├── ...
│   ├── 📂static
│   │   └── 📂keygen_temp
│   │       ├── 📂css
│   │       │   └── 📂admin_temp_key
│   │       │       └── admin_temp_key.css
│   │       └── 📂js
│   │           └── (arquivos JS se existirem)
│   │
│   ├── 📂templates
│   │   └── 📂keygen_temp
│   │       └── 📂admin_temp_key
│   │           ├── gerar_senha.html
│   │           └── validar_senha.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
│
├── 📂site_controle_processos
│   ├── asgi.py
│   ├── roles.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
│
└── manage.py
```

---

## Próximos Passos

O projeto está em desenvolvimento ativo com planos para:

- Aprimorar o sistema de permissões
- Adicionar dashboard analítico
- Implementar API REST
- Expandir modelos para outros nichos

---

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
