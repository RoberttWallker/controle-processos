from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class ComprasLentes(models.Model):
    data_compra = models.DateField(blank=False, null=False)
    ordem_de_servico = models.TextField(max_length=50, blank=False, null=False)
    sequencial_savwin = models.IntegerField(
        blank=False,
        null=False,
        validators=[
            MinValueValidator(1, message="O valor mínimo é 1"),
            MaxValueValidator(99999999, message="O valor máximo é 99.999.999")
        ],
        help_text="Número entre 1 e 99.999.999"
    )
    num_loja = models.IntegerField(blank=False, null=False)
    codigo = models.IntegerField(blank=False, null=False)
    descricao_lente = models.TextField(max_length=255, blank=False, null=False)
    referencia_fabricante = models.TextField(max_length=100, blank=True, null=True)
    num_pedido = models.IntegerField(blank=False, null=False)
    custo_site = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    data_liberacao_blu = models.DateField(blank=True, null=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    custo_tabela = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    nota_fiscal = models.IntegerField(blank=False, null=False)
    custo_nota_fiscal = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    duplicata = models.IntegerField(blank=False, null=False)
    observacao = models.TextField(max_length=600, blank=True, null=True)
    usuario_criacao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras_criadas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario_atualizacao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras_atualizadas')
    data_atualizacao = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if 'request' in kwargs:
            request = kwargs.pop('request')
            if request.user.is_authenticated:
                if not self.pk:  # Se for um novo registro
                    self.usuario_criacao = request.user
                self.usuario_atualizacao = request.user  # Sempre atualiza o último usuário que alterou
        super().save(*args, **kwargs)