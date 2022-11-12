import uuid
from django.utils import timezone
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, phone=None,  password=None, first_name=None, last_name=None,  **extra_fields):
        if not email:
            raise ValueError('Email required')

        if not first_name:
            raise ValueError('First Name required')

        if not last_name:
            raise ValueError('Last Name required!')

        if not phone:
            raise ValueError('Phone Number required!')

        user = self.model(email=self.normalize_email(email), first_name=first_name,last_name=last_name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name, phone, **extra_fields):
        user = self.create_user(email=email, password=password, first_name=first_name,last_name=last_name, phone=phone)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4(), unique=True, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Invalid phone number")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_identity_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    joined_date = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_email(self):
        return self.email

    def get_username(self):
        return self.email

     

    def get_phone(self):
        return self.phone

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def send_email(self, subject, message, from_email=None, silentError=None, **kwargs):
        if not silentError:
            silentError = True

        send_mail(subject, message, from_email, [
                  self.email], fail_silently=silentError, **kwargs)