from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from apps.finances.stripe_handler import Stripe

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
        serializer = self.get_serializer_class()
        serialized_data = serializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        user = serialized_data.save()
        user_name = serialized_data.validated_data["username"]
        user_email = serialized_data.validated_data["email"]
        stripe = Stripe()
        response = stripe.create_customer(name=user_name, email=user_email)
        user.stripe_id = response.id
        user.save()
        return Response(serializer(user).data)

    
    # Endpoint customizado para o usuário logado
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
