# Django imports.
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
# DRF imports.
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer,CharField, \
                                        IntegerField, ValidationError


# App imports.
from core.models import User


class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ('id', 'name', 'phone_number', 'email')


class UserLoginSerializer(Serializer):
    id_ = IntegerField(read_only=True)
    name = CharField(read_only=True)
    phone_number = CharField(max_length=15, required=False)
    email = CharField(max_length=255, required=True)
    password = CharField(max_length=128, write_only=True)

    def validate(self, data):        
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if email is not provided.
        if not email:
            raise ValidationError("Email is required to log in")

        # Raise an exception if the password is not provided.
        if not password:
            raise ValidationError("Password is required to log in")

        user = authenticate(username=email, password=password)

        if not user:
            raise ValidationError(
                'user with this email and password was not found'
            )

        return dict(
            id_=user.id, name=user.name,
            phone_number=user.phone_number, email=user.email, 
        )
