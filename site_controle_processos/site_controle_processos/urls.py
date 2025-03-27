from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend_site.urls')),
    path('keygen_temp/', include('keygen_temp.urls')),
]
