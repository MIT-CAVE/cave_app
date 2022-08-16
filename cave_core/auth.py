from django.contrib.auth.backends import ModelBackend, UserModel


class EmailThenUsernameModelBackend(ModelBackend):
    """
    Overwrites functionality for ModelBackend related to authenticate function
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Check if passed username matches an email on record
            If so: override the email with the username on record
            Else: pass the username as is
        """
        user = UserModel._default_manager.filter(email=username).first()
        if user:
            username = user.username
        return super().authenticate(request, username, password, **kwargs)
