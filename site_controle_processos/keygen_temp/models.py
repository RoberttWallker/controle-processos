import hashlib

from django.conf import settings
from django.core.exceptions import EmptyResultSet
from django.db import models
from django.db import DatabaseError, OperationalError
from django.core.exceptions import ValidationError
from django.utils import timezone


class SenhaTemporaria(models.Model):
    palavra_secreta = models.CharField(max_length=100)
    chave_temporal = models.CharField(max_length=255, unique=True)  # A senha gerada
    validade = models.DateTimeField()  # Tempo até a senha expirar
    ativo = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Verifica se a senha ainda é válida
        return timezone.now() < self.validade
    
    def clean(self):
        if self.palavra_secreta not in settings.SECRET_WORDS:
            raise ValidationError('Palavra secreta inválida!')
        super().clean()
    
    def save(self, *args, **kwargs):
        # Gera a chave temporal com base na SECRET_KEY e palavra secreta

        if not self.chave_temporal:
            # Usa isoformat() para garantir precisão nos milissegundos
            timestamp = timezone.now().isoformat()
            secret = settings.SECRET_KEY.encode('utf-8')
            palavra_completa = (self.palavra_secreta + timestamp + secret.decode('utf-8')).encode('utf-8')
            self.chave_temporal = hashlib.sha256(palavra_completa).hexdigest()  # Gerando hash seguro
            self.validade = timezone.now() + timezone.timedelta(minutes=20)  # Validade de 20 minutos
        
            self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def invalidate_expireds(cls):
        try:
            """Marca todas as senhas expiradas como inativas."""
            senhas_expiradas = cls.objects.filter(
                ativo=True,
                validade__lt=timezone.now()
            )
            senhas_expiradas.update(ativo=False)
            return True, "Senhas inativadas"
        
        except EmptyResultSet:
            return True, "Nenhuma senha ativa encontrada para invalidar"
        
        except OperationalError as e:
            return False, f"Erro de conexão com o banco de dados: {str(e)}"
        
        except DatabaseError as e:
            return False, f"Erro no banco de dados: {str(e)}"
        
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"

    def __str__(self):
        return f"Senha Temporária ({self.chave_temporal})"