from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorator import allowed_users

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
@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def createReminder(request, account_id):
       form = ReminderForm()
       account = Account.objects.get(pk=account_id)

       # check that the logged in user is tied to the account the reminder is being created for
       if request.user.id == account.user.id:
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
                     return redirect('index')
       
              context = {'form': form}
              return render(request, 'reminder_app/reminder_form.html', context)

# update an existing reminder
@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def updateReminder(request, account_id, reminder_id):
       # get desired reminder from the database
       reminder = Reminder.objects.get(pk=reminder_id)

       # check that the logged in user is the owner of the reminder
       if request.user == reminder.account.user:
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def deleteReminder(request, account_id, reminder_id):
       # get the desired reminder from the database
       reminder = Reminder.objects.get(pk=reminder_id)

       # check that the logged in user is the owner of the reminder
       if request.user == reminder.account.user:
              # if user selects the delete button, delete the reminder
              if request.method == "POST":
                     reminder.delete()

                     # redirect user to the detail page for the user
                     return redirect('account-detail', account_id)
              
              # add info about the project to the HTML context
              context = {'reminder': reminder}
              return render(request, 'reminder_app/reminder_delete.html', context)

# user registration page
def registerPage(request):
      form = CreateUserForm()

      if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                  user = form.save()
                  username = form.cleaned_data.get('username')
                  group = Group.objects.get(name='user')
                  user.groups.add(group)
                  account = Account.objects.create(user=user,)
                  account.save()

                  messages.success(request, 'Account was created for ' + username)
                  return redirect('login')
       
      context = {'form': form}
      return render(request, 'registration/register.html', context)

# user info page
@login_required(login_url='login')
@allowed_users(allowed_roles=['user'])
def userPage(request):
       account = request.user.account
       form = AccountForm(instance = account)
       print('account', account)
       reminders = Reminder.objects.all()

       if request.method == 'POST':
            form = AccountForm(request.POST, request.FILES, instance=account)
            if form.is_valid():
                  form.save()
       context = {'form': form}
       return render(request, 'reminder_app/user.html', context)
        

# home page
def index(request):
    reminders = Reminder.objects.all()
    context = {'reminders': reminders}
    return render( request, 'reminder_app/index.html', context)