from django.forms import ModelForm
from .models import *

class ReminderForm(ModelForm):
    class Meta: 
        model = Reminder 
        fields = ('title', 'date', 'description')