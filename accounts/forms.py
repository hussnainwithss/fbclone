from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for handling CustomUser Object Creation
    Makes sure first and last names are provided as
    they are mandatory
    Raises:
        ValidationError: if either first or last name isnt provided
        validationError is raised
    """
    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_first_name(self):
        """Called by form on validating form data
        also provides the calling view with firstname

        Raises:
            ValidationError: if firstname iisnt provided

        Returns:
            str: FirstName from submitted form data
        """
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        """
        Called by form on validating form data
        also provides the calling view with lastname

        Raises:
            ValidationError: if lastname iisnt provided

        Returns:
            str: lastname from submitted form data
        """
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]


class CustomUserChangeForm(UserChangeForm):
    """Form for handling CustomUser Object Update
    Makes sure first and last names are provided as
    they are mandatory
    Raises:
        ValidationError: if either first or last name isnt provided
        validationError is raised
    """
    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_first_name(self):
        """Called by form on validating form data
        also provides the calling view with firstname

        Raises:
            ValidationError: if firstname iisnt provided

        Returns:
            str: FirstName from submitted form data
        """
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        """Called by form on validating form data
        also provides the calling view with lastname

        Raises:
            ValidationError: if lastname iisnt provided

        Returns:
            str: lastname from submitted form data
        """
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]
