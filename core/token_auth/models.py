from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


# Create your models here.
class TokenAuth(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokenauth")
    token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user


class DeviceInfo(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    auth_token = models.ForeignKey(TokenAuth, on_delete=models.CASCADE, related_name='device')
    device_hash = models.CharField(max_length=255, blank=True, null=True)
    device_ip = models.CharField(max_length=50, blank=True, null=True)
    device_user_agent = models.TextField(default="")
    device_language = models.TextField(max_length=50, blank=True, null=True)
    device_accept_encoding = models.TextField(max_length=50, blank=True, null=True)
    device_type = models.TextField(max_length=50, blank=True, null=True)
    device_name = models.TextField(max_length=50, blank=True, null=True)
    device_version = models.TextField(max_length=50, blank=True, null=True)
    device_country = models.TextField(max_length=50, blank=True, null=True)
    device_state = models.TextField(max_length=50, blank=True, null=True)
    device_city = models.TextField(max_length=50, blank=True, null=True)
    device_zip = models.TextField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.device_hash
