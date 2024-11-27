from django.urls import path

from users.apps import UsersConfig
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserCreateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
         name='login'),
    path('token/refresh/',
         TokenRefreshView.as_view(
             permission_classes=(AllowAny,)),
         name='token_refresh'
         ),
    path('register/', UserCreateAPIView.as_view(),
         name='register'),
    path('user/update/<int:pk>/', UserCreateAPIView.as_view(),
         name='user_update'),
    path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(),
         name='user_delete')
]
