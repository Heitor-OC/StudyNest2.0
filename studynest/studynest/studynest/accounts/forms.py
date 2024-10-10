from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']      


        

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        


class BaralhoForm(forms.ModelForm):
    class Meta:
        model = Baralho
        fields = ['title']

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['frente', 'resposta', 'dificuldade']
