from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MinLengthValidator
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


class ConsumerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)    
    phone = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f'{self.user.username}'
    
    def get_full_name(self):
        return f'{self.fname} {self.lname}'

class Merchant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username}'

class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    issuerId = models.CharField(unique=True, max_length=3, validators=[MinLengthValidator(3)])
    
    def __str__(self):
        return f'{self.user.username}'