from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, HealthView

# -------- JWT‑эндпоинты ----------
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# --------------------------------

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    # health‑check
    path('health/', HealthView.as_view(), name='health'),

    # JWT токены
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # остальные роуты (router)
    path('', include(router.urls)),
]