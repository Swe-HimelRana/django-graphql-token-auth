from .models import TokenAuth, DeviceInfo
from django.contrib.auth import get_user_model
import uuid
import hashlib
import json
from django.db import transaction

User = get_user_model()


def generate_device_hash(request):
    user_agent = request.META['HTTP_USER_AGENT']
    user_ip = request.META.get('REMOTE_ADDR')

    context = {
        "user_agent": user_agent,
        "ip": user_ip
    }
    string_context = json.dumps(context)
    encoded_context = str.encode(string_context, 'utf8')
    res = hashlib.md5(encoded_context)
    return res.hexdigest()


def validate_device_hash(request, token):
    if not DeviceInfo.objects.filter(token=token).exists():
        print("Token is invalid")
    current_device_hash = generate_device_hash(request)
    saved_device_hash = DeviceInfo.objects.filter(auth_token=token).first()['device_hash']

    if current_device_hash == saved_device_hash:
        return True

    return False


def get_or_create_token(user_id, request):
    print("Get or create function called!")
    if not User.objects.filter(pk=user_id).exists():
        print("User not found")

    user = User.objects.get(pk=user_id)

    if TokenAuth.objects.filter(user=user).exists():
        print("user Exists called")
        token = TokenAuth.objects.filter(user=user).first()
        return token.token

    else:
        token = uuid.uuid4()
        token = hashlib.sha3_256(str(token).encode()).hexdigest()

        with transaction.atomic():
            new_token = TokenAuth()
            new_token.user = user
            new_token.token = token
            new_token.save()
            return token


def revoke_token(token):
    if TokenAuth.objects.filter(token=token).exists():
        TokenAuth.objects.filter(token=token).delete()
        return True
    else:
        return False
