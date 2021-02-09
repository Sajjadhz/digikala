from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


def validate_email_as_username(email):
    try:
        User.objects.get(email=email)
        print(User.objects.get(email=email))
        raise ValidationError(_("This email already exist!"), code='invalid')
    except User.DoesNotExist:
        pass


def validate_password(password):
    if len(password) < 4:
        raise ValidationError(_("password is too short."), code='invalid')


def validate_passwords(password1, password2):
    if password1 != password2:
        raise ValidationError(_("password don't match"), code='invalid')


def validate_email_login(email):
    try:
        User.objects.get(email=email)
        print(User.objects.get(email=email), 123)
    except User.DoesNotExist:
        raise ValidationError(_("This email does not exist."), code='invalid')
