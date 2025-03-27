from django.urls import path
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
    path('admin-panel/', admin_panel_view, name='admin_panel'),
    path('register/', register_view, name='register'),
    path('lancamento-de-lentes/', lanc_lentes_view, name='lancamento_de_lentes'),
]