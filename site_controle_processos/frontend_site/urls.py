from django.contrib.auth import views as auth_views
from django.urls import path

# Views de registro e autenticação
from .views import (
    LoginView,
    LogoutView,
    RegisterView
    )

# Views de telas
from .views import (
    AdminPanelView,
    LancamentoLentesCreateView,
    LancamentoLentesListView
    )

# Views de CRUD
from .views import (
    LancamentoLentesDeleteView
    )

urlpatterns = [

    # URLs de registro e autenticação
    path('', LoginView, name='home'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView, name='register'),

    # Página de reset de senha
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='frontend_site/registration/password_reset.html'),
        name='password_reset'
    ),
    
    # Página informando que o e-mail foi enviado
    path(
        'password-reset-msg/',
        auth_views.PasswordResetDoneView.as_view(template_name='frontend_site/registration/password_reset_msg.html'),
        name='password_reset_done'
    ),
    
    # Página onde o usuário redefine a senha (com token)
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='frontend_site/registration/new_password.html'),
        name='password_reset_confirm'
    ),
    
    # Página de sucesso após redefinir a senha
    path(
        'reset-complete',
        auth_views.PasswordResetCompleteView.as_view(template_name='frontend_site/registration/password_reset_complete.html'),
        name='password_reset_complete'
    ),

    # URLs de telas
    path('admin-panel/', AdminPanelView, name='admin_panel'),
    path('lancamento-de-lentes/', LancamentoLentesCreateView, name='lancamento_de_lentes'),
    path('listagem-lancamentos/', LancamentoLentesListView, name='listagem_lancamentos'),
    
    # URLs de CRUD
    path('excluir-lancamento-de-lentes/', LancamentoLentesDeleteView, name='excluir_lancamento_de_lentes')
]