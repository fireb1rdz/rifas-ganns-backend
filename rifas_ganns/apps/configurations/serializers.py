from rest_framework import serializers
from .models import UserConfiguration

class UserConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfiguration
        exclude = ["user"]
        
