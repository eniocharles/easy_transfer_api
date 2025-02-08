from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Wallet, Transaction

User = get_user_model()

class WalletSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'timestamp']
        read_only_fields = ['timestamp']

    def validate(self, data):
        sender = data['sender']
        receiver = data['receiver']
        amount = data['amount']

        if sender == receiver:
            raise serializers.ValidationError("O remetente e o destinatário não podem ser o mesmo usuário.")

        if amount <= 0:
            raise serializers.ValidationError("O valor da transação deve ser positivo.")

        if not hasattr(sender, 'wallet'):
            raise serializers.ValidationError("O remetente não possui uma carteira ativa.")

        if sender.wallet.balance < amount:
            raise serializers.ValidationError("Saldo insuficiente para realizar a transação.")

        return data

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)