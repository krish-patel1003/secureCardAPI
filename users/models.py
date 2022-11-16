from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    
    ROLE_OPTIONS = [
        ['CONSUMER', 'CONSUMER'],
        ['MERCHANT', 'MERCHANT'],
        ['BANK', 'BANK'],
        ['ADMIN', 'ADMIN']
    ]

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    role = models.CharField(choices=ROLE_OPTIONS, max_length=255)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    objects = UserManager()

    def __str__(self):
        return f'{self.role} - {self.email}'
    
    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh_token),
            'access':str(refresh_token.access_token)
        }