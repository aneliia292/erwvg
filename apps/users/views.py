from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserRegisterSerializer, LoginSerializer, UserSerializer


@api_view(['POST'])
def user_register_view(request, *args, **kwargs):
    """
    Функция регистрации (без авто авторизации)
    """
    serializer = UserRegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {'message': 'Регистрация прошла успешно', 'data': serializer.data},
            status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_handler(request):
    """
    Обработчик для входа в аккаунт
    """
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'message': 'Вход успешно завершен'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_handler(request):
    """
    Обработчик для выхода из аккаунта
    """
    logout(request)
    return Response({'message': 'Выход успешно завершен'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_info_handler(request, pk):
    """
    Обработчик для получения информации о пользователе
    """
    user = get_object_or_404(CustomUser, pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)