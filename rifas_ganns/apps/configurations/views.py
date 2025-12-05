from django.shortcuts import render
from rest_framework import viewsets, permissions, pagination
from apps.configurations.models import RaffleConfiguration, UserConfiguration
from apps.configurations.serializers import RaffleConfigurationSerializer, UserConfigurationSerializer
from apps.users.permissions import IsSellerOnly

class RaffleConfigurationPagination(pagination.PageNumberPagination):
    page_size = 10  # itens por página
    page_size_query_param = 'page_size'  # permite o front mudar o tamanho via query param
    max_page_size = 50
class RaffleConfigurationViewSet(viewsets.ModelViewSet):
    queryset = RaffleConfiguration.objects.all()
    serializer_class = RaffleConfigurationSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = RaffleConfigurationPagination

    