# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 02:57:18 2018

@author: AdeolaOlalekan
"""
from django import forms 
from .models import Post, Profile, Students
from django.contrib.auth.models import User
class PostForm(forms.ModelForm):
 
    class Meta:
        model = Post
        fields = ('title', 'text',)
######################################################################
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'website', 'bio', 'phone', 'city', 'country', 'organization', 'location', 'birth_date', 'department')
###############################################################################        

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required: a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1', 'password2')
        
from django.contrib.auth.models import User
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]

################################################################################       
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ('first_name', 'last_name', 'birth', 'address', 'country', 'phone_number', 'email')