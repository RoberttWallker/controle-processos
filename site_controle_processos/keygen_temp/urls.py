from django.urls import path

from .views import CreatePassword, ValidatePassword

urlpatterns = [
    path('gerar-senha/', CreatePassword, name='gerar_senha'),
    path('validar-senha/', ValidatePassword, name='validar_senha'),
]