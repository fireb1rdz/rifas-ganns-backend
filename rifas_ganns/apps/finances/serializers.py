from rest_framework import serializers
from rifas_ganns.apps.finances.models import UserBalance

class UserBalanceSerializer(serializers.Serializer):
    class Meta:
        model = UserBalance
        exclude = ["user"]
        
