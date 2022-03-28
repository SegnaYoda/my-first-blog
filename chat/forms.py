from django import forms
from django.forms import Textarea, fields
import re
from django.contrib.auth.models import User
from blog.models import UserProfile





class UserFormChat(forms.ModelForm):
    class Meta:
        model = UserProfile    
        fields = ['user',]  
        widgets = {
            #'username': forms.Select(attrs={"enctype": "multipart/form-data",, "id":"room-name-input"}),
            'user': forms.Select(attrs={"class": "form-control", "id":"room-name-input"}),
        }
        labels = {
            'id': 'room-name-input',}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
