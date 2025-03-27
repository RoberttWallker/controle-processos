from django.urls import path
from .views import gerar_senha, validar_senha

urlpatterns = [
    path('gerar-senha/', gerar_senha, name='gerar_senha'),
    path('validar-senha/', validar_senha, name='validar_senha'),
]