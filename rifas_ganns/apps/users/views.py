from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from .services.user_creation import UserCreationService

User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'me' or self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'me':
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        user = UserCreationService.create_user_and_sync_gateway(request.data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    
    # Endpoint customizado para o usuário logado
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
