from django.forms import ModelForm
from .models import Reminder
from django.contrib.auth.forms import UserCreationForm


class ReminderForm(ModelForm):
    class Meta: 
        model = Reminder 
        fields = ('title', 'date', 'description')

