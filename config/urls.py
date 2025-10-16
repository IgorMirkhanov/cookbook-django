from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('recipes/', include('recipes.urls')),      # HTML страницы
    path('api/', include('recipes.api_urls')),      # ← API endpoints (НОВЫЙ файл)
    path('', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)