from django.urls import path
from .views import home, login_view, register_view, admin_panel_view, lanc_lentes_view

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('admin-panel/', admin_panel_view, name='admin_panel'),
    path('lancamento-lentes/', lanc_lentes_view, name='lancamento_lentes'),
]