from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
"""
Usando o modelo generico do Django "AbstractUser" criamos um User Model com as melhores praticas possiveis e 
evitamos reimplementar autenticação do zero, oque poderia trazer vulnerabilidade e complexidade desnecessária.
"""
