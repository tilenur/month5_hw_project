from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserConfirmSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode

import random

@api_view(['POST'])
def authorization_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    code = random.randint(100000, 999999)
    ConfirmationCode.objects.create(user=user, code=code)



    return Response(
        status=status.HTTP_201_CREATED,
        data={'user_id': user.id}
    )


@api_view(['POST'])
def confirm_api_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    code = serializer.validated_data['code']

    user = User.objects.get(username=username)
    try:
        ConfirmationCode.objects.get(user=user, code=code)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user.is_active = True
    user.save()


    return Response(
        status=status.HTTP_201_CREATED,
        data={'user_id': user.id}
    )