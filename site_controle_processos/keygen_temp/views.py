from django.contrib import messages
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .models import (
    SenhaTemporaria
)

def CreatePassword(request):
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
            except ValidationError:
                messages.error(request, "Palavra secreta inválida!")
        else:
            messages.error(request, "Palavra secreta não fornecida.")
    return render(request, 'keygen_temp/admin_temp_key/gerar_senha.html', {'senha_gerada': senha_gerada})

def ValidatePassword(request):
    if request.method == "POST":
        senha_inserida = request.POST.get('senha_inserida')
        try:

            sucesso, msg = SenhaTemporaria.invalidate_expireds()
            if not sucesso:
                print(msg)

            with transaction.atomic():
                senha_temporaria = SenhaTemporaria.objects.select_for_update().get(
                    chave_temporal = senha_inserida,
                    ativo = True
                )

                if senha_temporaria.is_valid():
                    # Define uma variável de sessão para indicar que a senha foi validada
                    request.session['senha_validada'] = True
                    request.session.set_expiry(300)  # 5 minutos em segundos

                    
                    senha_temporaria.ativo = False
                    senha_temporaria.save()

                    messages.success(request, "Senha validada!")
                    return redirect('register')
                
                
                if not senha_temporaria.ativo:
                    messages.error(request, "A senha já foi usada ou expirou.")
                
        except SenhaTemporaria.DoesNotExist:
            messages.error(request, "Senha inválida.")
    return render(request, 'keygen_temp/admin_temp_key/validar_senha.html')