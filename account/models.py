from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class EstoreUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name,  phone, password=None):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        if not first_name:
            raise ValueError(_('please provide your first name'))
        if not last_name:
            raise ValueError(_('please provide your last name'))
        if not phone:
            raise ValueError(_('please provide an active phone number'))

        user = self.model(email=email, first_name=first_name, last_name=last_name,  phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name,last_name,  phone, password=None):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
        

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username=None
    email=models.EmailField(_('email address'), unique=True)
    first_name=models.CharField(max_length=255, blank=False, null=False)
    last_name=models.CharField(max_length=255, blank=False, null=False) 
    phone=models.CharField(max_length=12)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name', 'last_name',  'phone']

    objects=EstoreUserManager()

    def __str__(self): 
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    
