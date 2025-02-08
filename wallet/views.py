from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer

class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint para consultar saldo da carteira.
    """
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_balance(self, request):
        """
        Adiciona saldo à carteira do usuário autenticado.
        """
        amount = request.data.get('amount')
        if not amount or float(amount) <= 0:
            return Response({"error": "Valor inválido"}, status=status.HTTP_400_BAD_REQUEST)

        wallet = get_object_or_404(Wallet, user=request.user)
        wallet.credit(float(amount))
        return Response(WalletSerializer(wallet).data)

class TransactionViewSet(viewsets.ModelViewSet):
    """
    Endpoint para transferências financeiras entre usuários.
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(sender=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
