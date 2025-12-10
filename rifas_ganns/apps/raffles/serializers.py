from rest_framework import serializers
from .models import Raffle, Quota, RafflePicture, Prize, PrizePicture
from rifas_ganns.apps.configurations.models import RaffleConfiguration
from rifas_ganns.apps.configurations.serializers import RaffleConfigurationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class RafflePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RafflePicture
        fields = ['id', 'image', 'main']

class QuotaSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = Quota
        fields = ['id', 'number', 'owner', 'bought_at', 'is_winner']
        
class UserQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        exclude = ["owner"]

class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = "__all__"

class RaffleSerializer(serializers.ModelSerializer):
    pictures = RafflePictureSerializer(many=True, read_only=True)
    prizes = PrizeSerializer(read_only=True, many=True)
    created_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Raffle
        fields = [
            'id', 'title', 'description','draw_date', 'prizes', 'quota_value', 'pictures', 'created_at', 'created_by'
        ]
        
class RaffleDetailSerializer(serializers.ModelSerializer):
    pictures = RafflePictureSerializer(many=True, read_only=True)
    prizes = PrizeSerializer(read_only=True, many=True)
    class Meta:
        model = Raffle
        fields = [
            "title", "description", "created_at", "draw_date", "prizes",
            "quota_value", "winner", "awarded_at", "quota_count", "pictures"
        ]
        
class RaffleQuotaCountSerializer(serializers.ModelSerializer):
    used_quotas = serializers.IntegerField(source="quotas.count", read_only=True)
    available_quotas = serializers.IntegerField()
    class Meta:
        model = Raffle
        fields = ["quota_count", "used_quotas", "available_quotas"]
        
class PrizePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrizePicture
        fields = "__all__"


