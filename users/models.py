from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
    
    def __str__(self):
        return self.email

"""
Usando o modelo generico do Django "AbstractUser" criamos um User Model com as melhores praticas possiveis e 
evitamos reimplementar autenticação do zero, oque poderia trazer vulnerabilidade e complexidade desnecessária.
"""
