from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.views import LoginView

class AuthBackend(BaseBackend):
    """
    Custom Auth Backend to perform authentication via email and username
    """

    def authenticate(self, request, username=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(Q(email=username) | Q(username=username))
            if user.check_password(password):  # check valid password
                return user  # return user to be authenticated
        except user_model.DoesNotExist:  # no matching user exists
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
