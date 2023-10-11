from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
import uuid
# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    profile_image = models.ImageField(
        upload_to='profile_image', max_length=10000)
    is_verified = models.BooleanField(default=True)
    country = CountryField()
    otp = models.CharField(max_length=6, blank=True,null=True)
    is_private = models.BooleanField(default=False,null=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    class Meta:
        db_table = 'user'
