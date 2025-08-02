from django.urls import path
from .views import UserCreateView, UserDetailView

urlpatterns = [
    path('registro/', UserCreateView.as_view(), name='usuario_registro'),
    path('perfil/', UserDetailView.as_view(), name='usuario_perfil'),
]
