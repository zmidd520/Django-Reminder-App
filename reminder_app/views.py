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

class UserListView(generic.ListView):
    model = User

class UserDetailView(generic.DetailView):
    model = User

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get the context
            context = super(UserDetailView, self).get_context_data(**kwargs)
            # Create any data and add it to the context
            context['user_reminders'] = Reminder.objects.all()
            return context

# create a new reminder that is tied to a specific user
def createReminder(request, user_id):
     form = ReminderForm()
     user = User.objects.get(pk=user_id)

     if request.method == "POST":
          # make dictionary with user id and reminder data
          reminder_data = request.POST.copy()
          reminder_data['user_id'] = user_id

          # get form data
          form = ReminderForm(reminder_data)

          if form.is_valid():
               reminder = form.save(commit=False)
               reminder.user = user
               reminder.save()
          return redirect('user-detail', user_id)
     
     context = {'form': form}
     return render(request, 'reminder_app/reminder_form.html', context)

# update an existing reminder
def updateReminder(request, user_id, reminder_id):
       # get desired reminder from the database
       reminder = Reminder.objects.get(pk=reminder_id)
       # access the form for the specified reminder
       form = ReminderForm(instance=reminder)

       if request.method == "POST":
              form = ReminderForm(request.POST, instance=reminder)
              
              # save the valid form to the database
              if form.is_valid():
                     form.save()

              return redirect('user-detail', user_id)

       context = {'form': form}
       return render(request, 'reminder_app/reminder_form.html', context)

# deletes an existing reminder
def deleteReminder(request, user_id, reminder_id):
       # get the desired reminder from the database
       reminder = Reminder.objects.get(pk=reminder_id)
       
       # if user selects the delete button, delete the reminder
       if request.method == "POST":
              reminder.delete()

              # redirect user to the detail page for the user
              return redirect('user-detail', user_id)
       
       # add info about the project to the HTML context
       context = {'reminder': reminder}
       return render(request, 'reminder_app/reminder_delete.html', context)
        


def index(request):
    reminders = Reminder.objects.select_related('user').all()
    return render( request, 'reminder_app/index.html', {'reminders':reminders})