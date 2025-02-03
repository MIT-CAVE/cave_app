from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from cave_core.models import CustomUser
from datetime import datetime, timezone


class AuthModelBackend(ModelBackend):
    """
    Overwrites functionality for ModelBackend related to authenticate function
    """

    def lockout_check(self, user_obj):
        """
        Check if user is locked out
        """
        if user_obj.locked_out_until is not None:
            if datetime.now(timezone.utc) < user_obj.locked_out_until:
                lockout_minutes = int((user_obj.locked_out_until - datetime.now(timezone.utc)).total_seconds()//60+1)
                raise ValidationError(f"Due to too many unsuccessful login attempts this account has been locked for the next {lockout_minutes} minute{'s' if lockout_minutes > 1 else ''}.")

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Allow for username or email on login
        Handle lockout logic
        """
        user_obj = CustomUser.objects.filter(Q(username=username) | Q(email=username)).first()
        if user_obj is None:
            return None
        # If there is a current lockout, check if it has expired before attempting to authenticate
        self.lockout_check(user_obj)
        auth_user = super().authenticate(request, user_obj.username, password, **kwargs)
        user_obj.login_attempt(success = auth_user!=None)
        # After an authentication attempt, check if the user was just locked out
        self.lockout_check(user_obj)
        return auth_user
