# Django imports
from django.contrib.auth import authenticate, login

# DRF imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

# Local imports
from core.models import User
from users.seralizers import UserSerializer, UserLoginSerializer
from django.decorators import login_required

# Create your views here.

class UserLoginView(APIView):
    '''API to login a registered user.'''

    permission_classes = (AllowAny,)

    def post(self, request):
        
        login_serializer = UserLoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=request.data.get('email'),
            password=request.data.get('password')
        )
        login(request, user)

        return Response(data=login_serializer.data, status=status.HTTP_200_OK)


class SetPasswordView(APIView):
    '''Set the password for user'''

    @login_required
    def put(self, request):

        email = request.data.get('email', None)

        if not email:
            return Response(
                dict(message='Email is required to set password'),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        password = request.data.get('password', None)

        if not password:
            return Response(
                dict(message='Provide password'),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        try:
            user_obj = User.objects.get(email=email)
        except Exception as e:
            return Response(
                dict(message='Invalid email id, no user found'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_obj.set_password(password)
        user_obj.save()

        return Response(dict(message='success'), status=status.HTTP_200_OK)


class UsersListView(APIView):
    ''' List all user details'''
    @login_required
    def get(self, request):
        users_qs = User.objects.all()
        final_data = list()

        for user_obj in users_qs:
            user_serializer = UserSerializer(user_obj)

            data = user_serializer.data

            data['link'] = user_obj.get_absolute_url()

            final_data.append(data)

        return Response(data=final_data, status=status.HTTP_200_OK)


class UserDetailsView(APIView):
    ''' To get a user's details'''
    @login_required
    def get(self, request, user_id=None):
        print(request.user.is_authenticaed)

        try:
            user_obj = User.objects.get(id=user_id)
        
        except Exception as e:
            return Response(
                dict(message='Invalid user id'),
                status=status.HTTP_400_BAD_REQUEST
            )
        user_serializer = UserSerializer(user_obj)

        return Response(data=user_serializer.data, status=status.HTTP_200_OK)


class UserSearchView(APIView):
    '''To search a user based on their phone number'''
    
    @login_required
    def get(self, request):
        phone_number = request.GET.get('phone_number', None)

        user_qs = User.objects.filter(phone_number__iexact=phone_number)

        if user_qs.exists():
            user_obj = user_qs.first()
            user_serializer = UserSerializer(user_obj)

            return Response(
                data=user_serializer.data,
                status=status.HTTP_200_OK
            )