from django import forms
from django.forms import fields
from django.http import request
from . import models, views

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
        fields = ['bio','gender','birthday','relationship_status','first_name','last_name','email','hometown','work','education']
    

class CreatePostForm(forms.ModelForm):
    feed_type = forms.CharField(initial='add_new_text',required=False)
    class Meta:
        model = models.FeedTemplate
        fields = ['content','image','feed_type']

    def clean_feed_type(self):
        if not self['feed_type'].html_name in self.data:
            return self.fields['feed_type'].initial
        if self['image'] in self.data:
            return 'add_new_photo'
        return self.cleaned_data['feed_type']