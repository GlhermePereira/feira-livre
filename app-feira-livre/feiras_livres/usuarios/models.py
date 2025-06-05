# usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager

# Gerenciador de usuário
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo e-mail é obrigatório.')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email.split('@')[0])
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', email.split('@')[0])

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser precisa ter is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Modelo customizado de usuário
class Usuario(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="E-mail")
    first_name = models.CharField(max_length=30, verbose_name="Nome")
    last_name = models.CharField(max_length=30, verbose_name="Sobrenome")
    endereco = models.TextField(blank=True, verbose_name="Endereço")
    telefone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Formato: +5511987654321')],
        verbose_name="Telefone"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UsuarioManager()  # ✅ aqui sim é o lugar correto

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
