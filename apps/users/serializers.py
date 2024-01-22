from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    '''
       Сериализатор регистрации пользователей (без авто авторизации)
    '''
    password2 = serializers.CharField()

    class Meta:
        """
            Модель для регистрации
        """
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        """
            Проверка пароля
        """
        password = attrs['password']
        password2 = attrs['password2']

        if password != password2:
            raise serializers.ValidationError({'password': "Пароль не совпадает"})

        return attrs

    def save(self, *args, **kwargs):
        user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    """
      Сериализатор для валидации данных входа пользователя.
    """
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
              Проверяет введенные данные email и пароля пользователя.
        """
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if user and user.is_active:
                data['user'] = user
            else:
                raise serializers.ValidationError('Неверный email или пароль')
        else:
            raise serializers.ValidationError('Email и пароль обязательны')

        return data


class UserSerializer(serializers.ModelSerializer):
    """
      Сериализатор для модели пользователей.
    """
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']