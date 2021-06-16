from django import forms
from django.forms import fields
from . import models

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['profile_picture']
    
class CoverPictureForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['cover_picture']

class ProfileUpdate(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    class Meta:
        model = models.UserProfile
        fields = ['bio','gender','birthday','relationship_status','first_name','last_name','email']
    