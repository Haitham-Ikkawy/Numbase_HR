from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.http import HttpResponse


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError('Email Address is Required')

        if not username:
            raise ValueError('Username is Required')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        try:
            user.save(using=self._db)

        except Exception as e:
            return HttpResponse(e)
            
        return user

    def create_superuser(self, email, username, password):
        try:
            user = self.create_user(
                email=self.normalize_email(email),
                password=password,
                username=username,
            )

            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)

            return user

        except Exception as e:

            return HttpResponse(e)


class Account(AbstractBaseUser):

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.IntegerField(default=False)
    job_description = models.CharField(max_length=20, null=True)
    hour_rate = models.FloatField(default=0)
    department = models.ForeignKey('hr.Department', on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email + " ," + self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
