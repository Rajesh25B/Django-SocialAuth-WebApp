from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=125, null=False)
    phone_number = models.CharField(max_length=15, db_index=True)
    email = models.EmailField(max_length=75, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # Email & Password are required by default.
    REQUIRED_FIELDS = []

    
    objects = UserManager()

    # String representation
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/user/%/' % (self.pk)
    
    def set_password(self, password):
        self.password = password
        return