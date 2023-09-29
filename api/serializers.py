from rest_framework import serializers
from .models import TelegramBotToken, TelegramMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")
    

class TelegramBotTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramBotToken
        fields = ('token', 'user')

class TelegramMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramMessage
        fields = ( 'date_sent', 'message_body')
