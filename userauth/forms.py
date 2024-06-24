from django import forms
from django.forms import ModelForm

from .models import Cuisine
from .models import MenuItem


class MenuForm(ModelForm):
    # nested class
    class Meta:  # connects the model to the form
        model = MenuItem
        fields= "__all__"

        # fields = ('name', 'img')  # form built based on the specified fields

        labels = {
            'name': 'Enter menu name',
            'desc' : 'Describe the menu',
            'img' : 'Upload an image'
        }

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'menu name'}),  # form-control is  bootstrap class 
            'desc' : forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Details'}),
        }

class CuisineForm(ModelForm):
    # nested class
    class Meta:  # connects the model to the form
        model = Cuisine
        fields= "__all__"

        # fields = ('name', 'img')  # form built based on the specified fields

        labels = {
            'name': 'Enter cuisine name',
            'desc' : 'Describe the cuisine',
            'img' : 'Upload an image'
        }

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'cuisine name'}),  # form-control is  bootstrap class 
            'desc' : forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Details'}),
        }

        


       