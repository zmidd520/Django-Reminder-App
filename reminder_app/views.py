from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from .forms import *

# Create your views here.
class ReminderListView(generic.ListView):
    model = Reminder

class ReminderDetailView(generic.DetailView):
    model = Reminder

class AccountListView(generic.ListView):
    model = Account

class AccountDetailView(generic.DetailView):
    model = Account

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(AccountDetailView, self).get_context_data(**kwargs)
            # Create any data and add it to the context
            context['account_reminders'] = Reminder.objects.all()
            return context

# create a new reminder that is tied to a specific user
def createReminder(request, account_id):
     form = ReminderForm()
     account = Account.objects.get(pk=account_id)

     if request.method == "POST":
          # make dictionary with user id and reminder data
          reminder_data = request.POST.copy()
          reminder_data['account_id'] = account_id

          # get form data
          form = ReminderForm(reminder_data)

          if form.is_valid():
               reminder = form.save(commit=False)
               reminder.account = account
               reminder.save()
          return redirect('account-detail', account_id)
     
     context = {'form': form}
     return render(request, 'reminder_app/reminder_form.html', context)

# update an existing reminder
def updateReminder(request, account_id, reminder_id):
       # get desired reminder from the database
       reminder = Reminder.objects.get(pk=reminder_id)
       # access the form for the specified reminder
       form = ReminderForm(instance=reminder)

       if request.method == "POST":
              form = ReminderForm(request.POST, instance=reminder)
              
              # save the valid form to the database
              if form.is_valid():
                     form.save()

              return redirect('account-detail', account_id)

       context = {'form': form}
       return render(request, 'reminder_app/reminder_form.html', context)

# deletes an existing reminder
def deleteReminder(request, account_id, reminder_id):
       # get the desired reminder from the database
       reminder = Reminder.objects.get(pk=reminder_id)
       
       # if user selects the delete button, delete the reminder
       if request.method == "POST":
              reminder.delete()

              # redirect user to the detail page for the user
              return redirect('account-detail', account_id)
       
       # add info about the project to the HTML context
       context = {'reminder': reminder}
       return render(request, 'reminder_app/reminder_delete.html', context)
        


def index(request):
    reminders = Reminder.objects.select_related('account').all()
    return render( request, 'reminder_app/index.html', {'reminders':reminders})