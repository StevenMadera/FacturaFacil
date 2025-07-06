from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

Usuario = get_user_model()

class NITOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(username=username)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            try:
                user = Usuario.objects.get(nit=username)
                if user.check_password(password):
                    return user
            except Usuario.DoesNotExist:
                return None
        return None