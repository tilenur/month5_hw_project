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

    # step 1: receive data
    username = request.data.get('username')
    password = request.data.get('password')

    # step 2: authenticate user
    user = authenticate(username=username, password=password)

    if user is not None:
        try:
            # get existing token
            token = Token.objects.get(user=user)

        except:
            # create new token if it does not exist
            token = Token.objects.create(user=user)

        # step 3: return response
        return Response(
            data={'key': token.key}
        )

    return Response(
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
def registration_api_view(request):

    # step 0: Validation (Existing, Typing, Extra)
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # step 1: receive data
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    # step 2: create inactive user
    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    # generate random 6-digit code
    code = random.randint(100000, 999999)

    # create confirmation code object
    ConfirmationCode.objects.create(
        user=user,
        code=code
    )

    # step 3: return response
    return Response(
        status=status.HTTP_201_CREATED,
        data={'user_id': user.id}
    )


@api_view(['POST'])
def confirm_api_view(request):

    # step 0: Validation (Existing, Typing, Extra)
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # step 1: receive data
    username = serializer.validated_data['username']
    code = serializer.validated_data['code']

    # step 2: verify code and activate user
    user = User.objects.get(username=username)

    try:
        ConfirmationCode.objects.get(
            user=user,
            code=code
        )

    except:
        return Response(
            status=status.HTTP_404_NOT_FOUND
        )

    # activate user
    user.is_active = True
    user.save()

    # step 3: return response
    return Response(
        status=status.HTTP_201_CREATED,
        data={'user_id': user.id}
    )