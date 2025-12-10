from rifas_ganns.apps.users.serializers import UserCreateSerializer
from rifas_ganns.apps.users.models import User
from rifas_ganns.apps.finances.services.gateways.factory import GatewayFactory
from rifas_ganns.apps.configurations.models import GatewayConfiguration

class UserCreationService:
    @staticmethod
    def create_user_and_sync_gateway(data: dict):
        user = UserCreationService.validate(data)
        config = GatewayConfiguration.objects.filter(active=True).first()
        gateway_class = GatewayFactory.create_instance(config.name)
        gateway = gateway_class()
        customer_id_in_gateway = gateway.create_customer(**data)
        user.gateway_id = customer_id_in_gateway
        user = user.save()
        return user
    
    @staticmethod
    def validate(data: dict) -> User:
        serializer = UserCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return user