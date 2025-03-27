from django.db import models
from django.utils import timezone
from django.conf import settings
import hashlib
import os

# Create your models here.

class SenhaTemporaria(models.Model):
    palavra_secreta = models.CharField(max_length=100)
    chave_temporal = models.CharField(max_length=255, unique=True)  # A senha gerada
    validade = models.DateTimeField()  # Tempo até a senha expirar
    criada_em = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Verifica se a senha ainda é válida
        return timezone.now() < self.validade
    
    def save(self, *args, **kwargs):
        # Gera a chave temporal com base na SECRET_KEY e palavra secreta
        if not self.chave_temporal:
            secret = settings.SECRET_KEY.encode('utf-8')
            palavra_completa = (self.palavra_secreta + secret.decode('utf-8')).encode('utf-8')
            self.chave_temporal = hashlib.sha256(palavra_completa).hexdigest()  # Gerando hash seguro
            self.validade = timezone.now() + timezone.timedelta(minutes=20)  # Validade de 20 minutos
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Senha Temporária ({self.chave_temporal})"