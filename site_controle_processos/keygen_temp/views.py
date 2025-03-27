from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import SenhaTemporaria
from django.http import JsonResponse

# Create your views here.


def gerar_senha(request):
    senha_gerada = None
    if request.method == "POST":
        palavra_secreta = request.POST.get('palavra_secreta')
        if palavra_secreta:
            try:
                senha = SenhaTemporaria.objects.create(palavra_secreta=palavra_secreta)
                senha_gerada = senha.chave_temporal
                messages.success(request, "Senha gerada com sucesso!")
            except IntegrityError:
                messages.error(request, "Palavra secreta usada nos últimos 20 minutos.")
        else:
            messages.error(request, "Palavra secreta não fornecida.")
    return render(request, 'admin_temp_key/gerar_senha.html', {'senha_gerada': senha_gerada})

def validar_senha(request):
    if request.method == "POST":
        senha_inserida = request.POST.get('senha_inserida')
        try:
            senha_temporaria = SenhaTemporaria.objects.get(chave_temporal=senha_inserida)
            if senha_temporaria.is_valid():
                # Define uma variável de sessão para indicar que a senha foi validada
                request.session['senha_validada'] = True
                return redirect('register')
            else:
                messages.error(request, "A senha expirou.")
        except SenhaTemporaria.DoesNotExist:
            messages.error(request, "Senha inválida.")
    return render(request, 'admin_temp_key/validar_senha.html')