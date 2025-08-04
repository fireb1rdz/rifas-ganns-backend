from rest_framework import serializers
from .models import Raffle, Quota, RafflePicture
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Exemplo básico, pode expandir

class RafflePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RafflePicture
        fields = ['id', 'image', 'uploaded_at', 'main']

class QuotaSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = Quota
        fields = ['id', 'number', 'owner', 'bought_at', 'is_winner']

class RaffleSerializer(serializers.ModelSerializer):
    winner = UserSimpleSerializer(read_only=True)
    quotas = QuotaSerializer(many=True, read_only=True)
    pictures = RafflePictureSerializer(many=True, read_only=True)

    class Meta:
        model = Raffle
        fields = [
            'id', 'title', 'description', 'created_at', 'draw_date', 'prize_value', 'quota_value',
            'winner', 'awarded_at', 'quotas', 'pictures'
        ]
