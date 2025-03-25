from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class ComprasLentes(models.Model):
    descricao = models.TextField(max_length=255, blank=False, null=False)
    nota_fiscal = models.IntegerField(blank=False, null=False)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    data_compra = models.DateField(blank=False, null=False)
    sequencial = models.IntegerField(blank=False, null=False)
    referencia_fabricante = models.TextField(max_length=100, blank=False, null=False)
    observacao = models.TextField(max_length=600, blank=True, null=True)