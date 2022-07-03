from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *


class UserAuthentication(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'placeholder': 'Password'}))


class UserRegister(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Login'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'fadeIn third', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fadeIn third', 'placeholder': 'Repeat you password'}))
    policy_agree = forms.BooleanField(widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'policy_agree')


class AddProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'description', 'actual_price', 'image', 'category')


class MakeDiscountForm(forms.Form):
    new_price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Новая цена'}))
    make_discount = forms.BooleanField(widget=forms.CheckboxInput(), required=False)


class AddCommentaryForm(ModelForm):

    class Meta:
        model = Commentary
        fields = ('content', )


class MyCabinetChangeForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(), required=False)
    last_name = forms.CharField(widget=forms.TextInput(), required=False)
    email = forms.EmailField(widget=forms.EmailInput(), required=False)
    image = forms.ImageField(required=False)
    username = forms.CharField(widget=forms.TextInput())


class BonusInputForm(forms.Form):
    bonus_count = forms.IntegerField(widget=forms.TextInput(attrs={'min': 0,
                                                                   'value': 0,
                                                                   'type': 'number',
                                                                   'style': 'max-width: 50px'
                                                                   }), label='Оплатить бонусами')
