from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from library.managers import UserManager
from datetime import timedelta, datetime
from django.utils import timezone
import json



class CustomUser(AbstractBaseUser):
    MEMBERSHIP_NORMAL = 'N'
    MEMBERSHIP_VIP = 'V'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_NORMAL,'Normal'),
        (MEMBERSHIP_VIP,'VIP'),
    ]
    full_name = models.CharField(max_length=100,unique=True,null=True)
    email = models.EmailField(unique=True)
    expiration_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices= MEMBERSHIP_CHOICES, default= MEMBERSHIP_NORMAL)
    phone = models.CharField(max_length=11, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    wallet = models.PositiveIntegerField(default=0)


    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email','password','full_name',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class OtpCode(models.Model):
    phone = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now= True)
    created2 = models.DateTimeField(null=True)


    def __str__(self):
        return f'{self.phone} - {self.code} - {self.created}'
    
class OtpBanStatus(models.Model):
    sms_function = models.CharField(max_length=30)
    blocked_time = models.DateTimeField()
    ban_statuse = models.BooleanField(default=False)
    #error_list = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.sms_function} - {self.blocked_time} - {self.ban_statuse}'
    
class ErrorList(models.Model):
    error_list = models.CharField(max_length=200,null=True)