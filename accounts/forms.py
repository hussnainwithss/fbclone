from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for handling CustomUser Object Creation
    """
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """Form for handling CustomUser Object Update
    """
    class Meta:
        model = CustomUser
        fields = ('email',)
