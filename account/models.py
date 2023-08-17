from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from library.managers import UserManager
from datetime import timedelta, datetime


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
    #choice field
    membership = models.CharField(max_length=1, choices= MEMBERSHIP_CHOICES, default= MEMBERSHIP_NORMAL)
    phone = models.CharField(max_length=11, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = ['phone','email']#['email',] #required fields when making a user in shell by createsuper user

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
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now= True)
    created2 = datetime.now()


    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'