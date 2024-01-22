from django.urls import path

from .views import user_register_view, login_handler, logout_handler, user_info_handler

urlpatterns = [
    path('register/', user_register_view, name='register'),
    path('login/', login_handler, name='login'),
    path('logout/', logout_handler, name='logout'),
    path('user/<int:pk>/', user_info_handler, name='user-detail'),
]
