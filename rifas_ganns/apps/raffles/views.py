from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .permissions import IsOwnerOnly
from .models import Raffle
from .serializers import RaffleSerializer, RaffleDetailSerializer, RaffleQuotaCountSerializer
from .filters import RaffleFilter
from apps.configurations.serializers import RaffleConfigurationSerializer
from apps.configurations.models import RaffleConfiguration

class RafflePagination(PageNumberPagination):
    page_size = 10  # itens por página
    page_size_query_param = 'page_size'  # permite o front mudar o tamanho via query param
    max_page_size = 50

class RaffleViewSet(viewsets.ModelViewSet):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = RafflePagination
    ordering_fields = ["draw_date"]
    filterset_class = RaffleFilter
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return RaffleDetailSerializer
        if self.action == "quota_count":
            return RaffleQuotaCountSerializer
        return super().get_serializer_class()
    
    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def quota_count(self, request, pk=None):
        raffle = self.get_object()
        serializer = RaffleQuotaCountSerializer(instance=raffle)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "put"], permission_classes=[IsAdminUser|IsOwnerOnly])
    def configuration(self, request, pk=None):
        raffle = self.get_object()
        try:
            config = raffle.configuration
        except RaffleConfiguration.DoesNotExist:
            return Response({"detail": "Configuration not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RaffleConfigurationSerializer(instance=config)
        return Response(serializer.data)