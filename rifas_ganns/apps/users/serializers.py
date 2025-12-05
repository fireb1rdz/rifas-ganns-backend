from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Address, SocialMedia
from apps.configurations.serializers import UserConfigurationSerializer
from apps.finances.serializers import UserBalanceSerializer
from apps.raffles.serializers import UserQuotaSerializer


User = get_user_model()

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["user"] 
class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        exclude = ["user"]

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    social_medias = SocialMediaSerializer(read_only=True)
    configuration = UserConfigurationSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "cpf", "birth_date", "lucky_number",
            "profile_picture", "bio", "is_verified",
            "addresses", "social_medias", "configuration"
        ]
        read_only_fields = ["id", "balance", "is_verified"]
        
class UserDetailSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    social_medias = SocialMediaSerializer(read_only=True)
    configuration = UserConfigurationSerializer(read_only=True)
    balance = UserBalanceSerializer(read_only=True)
    quotas = UserQuotaSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "cpf", "birth_date", "lucky_number",
            "balance", "profile_picture", "bio", "is_verified",
            "addresses", "social_medias", "configuration", "balance", "quotas", "stripe_id"
        ]
        read_only_fields = ["id", "balance", "is_verified", "quotas"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    addresses = AddressSerializer(many=True, required=False)
    social_medias = SocialMediaSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "username", "email", "cpf", "birth_date", "lucky_number",
            "balance", "profile_picture", "bio", "is_verified",
            "password", "password2",
            "addresses", "social_medias", "scope"
        ]
        read_only_fields = ["balance", "is_verified"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs

    def create(self, validated_data):
        addresses_data = validated_data.pop("addresses", [])
        social_media_data = validated_data.pop("social_medias", None)
        validated_data.pop("password2")

        user = User.objects.create_user(**validated_data)

        for addr in addresses_data:
            Address.objects.create(user=user, **addr)

        if social_media_data:
            SocialMedia.objects.create(user=user, **social_media_data)

        return user