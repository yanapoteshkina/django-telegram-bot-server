import random
import string
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TelegramBotToken, TelegramMessage
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from .serializers import TelegramBotTokenSerializer, TelegramMessageSerializer, UserSerializer, UserLoginSerializer



def generate_token(length=10):
    characters = string.ascii_letters
    token = ''.join(random.choice(characters) for _ in range(length))
    return token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False)
    def register(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = User.objects.create_user(
                username=serialized.data['username'],
                password=serialized.data['password'],
                email=serialized.data['email']
            )
            user.save()
            return Response('user registered', status=status.HTTP_201_CREATED)
        return Response('invalid data', status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)

            # Проверьте, существует ли запись с user_id
            user_id = user.id 
            token_user_code = generate_token()
            token, created = TelegramBotToken.objects.get_or_create(user_id=user_id, defaults={'token': token_user_code})
            
            return Response({'message': 'Аутентификация успешна, ваш токен:', 'token': token.token})
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Выход выполнен успешно'})


class TelegramBotTokenViewSet(viewsets.ModelViewSet):
    queryset = TelegramBotToken.objects.all()
    serializer_class = TelegramBotTokenSerializer
 

class TelegramMessageViewSet(viewsets.ModelViewSet):
    queryset = TelegramMessage.objects.all()
    serializer_class = TelegramMessageSerializer

    @action(detail=False, methods=['POST'])
    def create_message(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Устанавливаем user_id на основе аутентифицированного пользователя
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['GET'])
    def user_messages(self, request):
            user_id = request.query_params.get('user_id')
            if user_id is not None:
                messages = TelegramMessage.objects.filter(user_id=user_id)
                serializer = self.get_serializer(messages, many=True)
                return Response(serializer.data)
            return Response({"user_id": "User ID parameter is required."}, status=400)
