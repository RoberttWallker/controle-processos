from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ComprasLentes

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Autenticar o usuário
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return render(request, 'frontend_site/auth/login.html')
        else:
            messages.error(request, "E-mail ou senha inválidos.")
            return render(request, 'frontend_site/auth/login.html')

    return render(request, 'frontend_site/auth/login.html')

def register_view(request):
    # Verifica se a senha foi validada na sessão
    if not request.session.get('senha_validada'):
        # Se a senha não foi validada, redireciona para a página de validação
        messages.error(request, "Para se registar, você precisa primeiro solicitar a senha temporária ao administrador e validá-la.")
        return redirect('validar_senha')
    
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        confirm_senha = request.POST['confirm_senha']

        if senha != confirm_senha:
            messages.error(request, "Senhas não conferem, tente novamente!")
            return render(request, 'frontend_site/auth/register.html', {'nome': nome, 'email': email})
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Este e-mail já está cadastrado!")
            return redirect("register")
        
        user = User.objects.create_user(
            username=nome,
            email=email,
            password=senha
        )

        user.save()

        # Remove a variável de sessão após o registro
        del request.session['senha_validada']

        messages.success(request, "Usuário registrado com sucesso!")
        return render(request, 'frontend_site/auth/register.html')

    return render(request, 'frontend_site/auth/register.html')

@login_required
def admin_panel_view(request):
    return render(request, 'frontend_site/admin_panel/admin_panel.html')

@login_required
def lanc_lentes_view(request):
    if request.method == 'POST':
        descricao = request.POST['descricao']
        nota_fiscal = request.POST['nota_fiscal']
        valor_custo = request.POST['valor_custo']
        data_compra = request.POST['data_compra']
        sequencial_prod = request.POST['sequencial_prod']
        ref_fabricante = request.POST['ref_fabricante']
        observacao = request.POST['observacao']

        # Criar objeto e salvar no banco
        compra = ComprasLentes.objects.create(
            descricao=descricao,
            nota_fiscal=nota_fiscal,
            valor_custo=valor_custo,
            data_compra=data_compra,
            sequencial=sequencial_prod,
            referencia_fabricante=ref_fabricante,
            observacao=observacao
        )

        if compra:
            messages.success(request, "Entrada efetuada com sucesso.")
            return redirect('compras_de_lentes')

    return render(request, 'frontend_site/estoque/lancamento_de_lentes.html')
    