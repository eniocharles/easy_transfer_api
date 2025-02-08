from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError


class Wallet(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet')
    balance = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        default= 0)
 
    def credit(self, amount):
        if amount <= 0:
            raise ValidationError('O valor a ser creditado não foi aceito.')
        self.balance += amount
        self.save(update_fields=['balance'])

    def debit(self, amount):
        if amount <= 0:
            raise ValidationError('O valor a ser debitado não foi aceito.')
        if self.balance < amount:
            raise ValidationError('Saldo insuficiente para a operação.')
        self.balance -= amount
        self.save(update_fields=['balance'])

    def __str__(self):
        return f'Carteira de {self.user.username} - Saldo: {self.balance}'
    """
    - Cada usuário tem uma única carteira (relação um pra um com o usuário).
    - Métodos de crédito e de débito para atualizar o saldo de forma que não deixe nada a desejar.
    """    

class Transaction(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'sent_transactions')
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete =  models.CASCADE,
        related_name = 'received_transactions')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,) 
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )
    def clean(self, *args,**kwargs):
        if self.amount <=0:
            raise ValidationError('O valor da transação deve ser positivo')
        if self.sender == self.receiver:
            raise ValidationError('O remetente e o destinatário não podem ser o mesmo usuário')
    
    def save(self, *args, **kwargs):
        self.clean()
        with transaction.atomic():
            sender_wallet = self.sender.wallet
            receiver_wallet = self.receiver.wallet

            sender_wallet.debit(self.amount)
            receiver_wallet.credit(self.amount)

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.sender.username} --> {self.receiver.username}: {self.amount} em {self.timestamp}'
        
    """
    - Cada transação envolve um remetente (sender) e um destinatário (receiver).
    - É registrado o valor transferido e a data/hora da transação.
    - A operação deve ser atômica: se falhar (por exemplo, saldo insuficiente), nenhuma alteração é aplicada.
    """