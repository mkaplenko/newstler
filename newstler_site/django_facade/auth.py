"""Customizing of django authenticate"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.http.request import HttpRequest


class EmailBackend(ModelBackend):
    """
    Authenticate against email addresses.
    """
    def authenticate(self, request: HttpRequest, email: str=None, password: str=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except (User.MultipleObjectsReturned, User.DoesNotExist):
            return None
        else:
            if user.check_password(password):
                return user
