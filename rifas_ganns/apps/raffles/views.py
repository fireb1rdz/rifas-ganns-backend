from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Raffle
from .serializers import RaffleSerializer

class RafflePagination(PageNumberPagination):
    page_size = 10  # itens por página
    page_size_query_param = 'page_size'  # permite o front mudar o tamanho via query param
    max_page_size = 50

class RaffleViewSet(viewsets.ModelViewSet):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = RafflePagination