from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers

from .models import Account


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'password', 'datetime')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if Account.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password is too short.")
        if len(value) > 32:
            raise serializers.ValidationError("Password must be less than 32 characters.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class AccountVerifySerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)

    def validate(self, data):
        try:
            account = Account.objects.get(username=data['username'])
        except Account.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        if not check_password(data['password'], account.password):
            raise serializers.ValidationError("Incorrect password.")
        return data
