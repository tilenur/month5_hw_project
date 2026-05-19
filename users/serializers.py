from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate_username(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("Username already exists")


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    code = serializers.IntegerField(min_value=100000, max_value=999999)

    def validate_username(self, username):
        try:
            user = User.objects.get(username=username)
        except:
            raise ValidationError("Username does not exist")
        return username
