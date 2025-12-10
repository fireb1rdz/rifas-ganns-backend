from rest_framework import serializers
from .models import UserConfiguration
from rifas_ganns.apps.configurations.models import RaffleConfiguration

class UserConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfiguration
        exclude = ["user"]
        
class RaffleConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaffleConfiguration
        exclude = ["raffle"]