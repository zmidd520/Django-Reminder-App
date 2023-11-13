from django.db import models
from django.urls import reverse

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('account-detail', args=[str(self.id)])

class Reminder(models.Model):
    # choices for date/time-related fields

    title = models.CharField(max_length=100)
    date = models.DateField(default=None)
    description = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('reminder-detail', args=[str(self.id)])
