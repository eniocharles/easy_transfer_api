from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD de usuários.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]  # Permitir cadastro sem autenticação
        return [permissions.IsAuthenticated()]  # Restringir outras ações para usuários autenticados

class CustomLoginView(APIView):
    """
    Endpoint para login e obtenção de tokens JWT.
    """
    permission_classes = [permissions.AllowAny]  # Permitir login sem autenticação prévia

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
