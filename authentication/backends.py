from django.contrib.auth.backends import ModelBackend
from .models import CustomeUser

class PhoneAuthBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = CustomeUser.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except CustomeUser.DoesNotExist:
            return None
