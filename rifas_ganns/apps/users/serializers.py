from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Address, Email, Phone, SocialMedia

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["user"] 


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        exclude = ["user"]


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        exclude = ["user"]

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        exclude = ["user"]

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    emails = EmailSerializer(many=True, read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    social_medias = SocialMediaSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "cpf", "birth_date", "lucky_number",
            "balance", "profile_picture", "bio", "is_verified",
            "addresses", "emails", "phones", "social_medias"
        ]
        read_only_fields = ["id", "balance", "is_verified"]

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    addresses = AddressSerializer(many=True, required=False)
    emails = EmailSerializer(many=True, required=False)
    phones = PhoneSerializer(many=True, required=False)
    social_medias = SocialMediaSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "username", "email", "cpf", "birth_date", "lucky_number",
            "balance", "profile_picture", "bio", "is_verified",
            "password", "password2",
            "addresses", "emails", "phones", "social_medias"
        ]
        read_only_fields = ["balance", "is_verified"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs

    def create(self, validated_data):
        addresses_data = validated_data.pop("addresses", [])
        emails_data = validated_data.pop("emails", [])
        phones_data = validated_data.pop("phones", [])
        social_media_data = validated_data.pop("social_medias", None)
        validated_data.pop("password2")

        user = User.objects.create_user(**validated_data)

        for addr in addresses_data:
            Address.objects.create(user=user, **addr)

        for em in emails_data:
            Email.objects.create(user=user, **em)

        for phone in phones_data:
            Phone.objects.create(user=user, **phone)

        if social_media_data:
            SocialMedia.objects.create(user=user, **social_media_data)

        return user