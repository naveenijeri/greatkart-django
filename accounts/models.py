from operator import truediv
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password

# Create your models here.
class MyAccountManager(BaseUserManager):
    def cretate_user(self, email, username, first_name, last_name, password=None, **other_fields):
        if not email:
            raise ValueError("User must have an email address")
        
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.password=make_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):
        user = self.cretate_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            is_staff=True,
            is_admin=True
        )
        user.is_admin = True
        user.is_activae = True
        user.is_staff = True
        user.is_superadmin = True
        user.password=make_password(password)
        user.save(using=self.db)
        return user
class Account(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)

    #required fileds
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def hash_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True


