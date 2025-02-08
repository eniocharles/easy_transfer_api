from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas dos apps
    path('api/', include('users.urls')),
    path('api/', include('wallet.urls')),

    # Autenticação com JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (retorna access e refresh token)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Atualiza token de acesso
]