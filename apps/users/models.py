from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    """
      Менеджер пользователей приложения.
      Отвечает за создание и управление пользователями.
      """
    def _create_user(self, email, username, password, **extra_field):
        """
        Создает и сохраняет обычного пользователя с заданным email, username и password.
        """
        if not email:
            raise ValueError('Нет почты')
        if not username:
            raise ValueError('Не задано имя пользователя')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_field
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password):
        return self._create_user(email, username, password)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя.
    Расширяет AbstractBaseUser и PermissionsMixin от Django.
    """
    email = models.EmailField(max_length=30, unique=True, verbose_name='Email')
    username = models.CharField(max_length=30, verbose_name='Username')
    is_active = models.BooleanField(default=True, verbose_name='Пользователь активен?')
    is_staff = models.BooleanField(default=False, verbose_name='Пользователь админимтратор?')
    is_superuser = models.BooleanField(default=False, verbose_name='Пользователь superuser?')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
