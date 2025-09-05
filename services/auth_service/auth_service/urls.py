# services/auth_service/auth_service/urls.py
from django.contrib import admin
from django.urls import path, include

# Если используешь drf‑spectacular для автодокументации
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ------------------------------
    # Приложение users (в нём уже есть:
    #   - health/
    #   - token/ и token/refresh/
    #   - profile/ (router)
    # ------------------------------
    path('api/', include('users.urls')),

    # ------------------------------
    # Swagger / Redoc (опционально)
    # ------------------------------
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]