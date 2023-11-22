from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ReminderForm(ModelForm):
    class Meta: 
        model = Reminder 
        fields = ('title', 'date', 'description')

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['user']