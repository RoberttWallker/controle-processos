from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import time

# Create your views here.
def home(request):
    return render(request, 'frontend_site/home.html')

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
            return render(request, 'frontend_site/login.html')
        else:
            messages.error(request, "E-mail ou senha inválidos.")
            return render(request, 'frontend_site/login.html')

    return render(request, 'frontend_site/login.html')

def register_view(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        confirm_senha = request.POST['confirm_senha']

        if senha != confirm_senha:
            messages.error(request, "Senhas não conferem, tente novamente!")
            return render(request, 'frontend_site/register.html', {'nome': nome, 'email': email})
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Este e-mail já está cadastrado!")
            return redirect("register")
        
        user = User.objects.create_user(
            username=nome,
            email=email,
            password=senha
        )

        user.save()

        messages.success(request, "Usuário registrado com sucesso!")
        return render(request, 'frontend_site/register.html')

    return render(request, 'frontend_site/register.html')

def admin_panel_view(request):
    return render(request, 'frontend_site/admin_panel.html')

def lanc_lentes_view(request):
    return render(request, 'frontend_site/lancamento_lentes.html')
    