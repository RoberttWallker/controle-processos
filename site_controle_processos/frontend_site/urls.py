from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    logout_view,
    login_view,
    register_view,
    admin_panel_view,
    lanc_lentes_view
    )

urlpatterns = [
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
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

    path('admin-panel/', admin_panel_view, name='admin_panel'),
    path('register/', register_view, name='register'),
    path('lancamento-de-lentes/', lanc_lentes_view, name='lancamento_de_lentes'),
]