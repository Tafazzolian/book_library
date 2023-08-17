from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, phone, email, full_name, password):
        if not phone:
            raise ValueError('User must have phone number')
        if not email:
            raise ValueError('User must have Email')
        if not full_name:
            raise ValueError('User must have first name')


        user = self.model(phone=phone, email=self.normalize_email(email), full_name=full_name,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone,email,full_name, password):
        user = self.create_user(phone,email,full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user