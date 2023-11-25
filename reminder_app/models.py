from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    about = models.TextField(blank=True)

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('account-detail', args=[str(self.id)])

class Reminder(models.Model):
    # choices for reminder color
    COLORS = (
        ('bg-black text-white', 'Black'),
        ('list-group-item-primary', 'Blue'),
        ('list-group-item-success', 'Green'),
        ('list-group-item-danger', 'Red'),
        ('list-group-item-warning', 'Yellow')
    )

    title = models.CharField(max_length=100)
    date = models.DateField(default=None)
    color = models.CharField(max_length=100, choices=COLORS, default='bg-black text-white')
    description = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('reminder-detail', args=[str(self.id)])
