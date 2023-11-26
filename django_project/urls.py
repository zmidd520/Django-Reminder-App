"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reminder_app import views

urlpatterns = [
    # admin pages
    path('admin/', admin.site.urls),

    # home page
    path('', include('reminder_app.urls')),

    # account pages
    path('users/', views.AccountListView.as_view(), name= 'accounts'),
    path('users/<int:pk>', views.AccountDetailView.as_view(), name= 'account-detail'),

    # reminder pages
    path('reminders/<int:pk>', views.ReminderDetailView.as_view(), name= 'reminder-detail'),
    path('users/<int:account_id>/create_reminder/', views.createReminder, name= 'create_reminder'),
    path('users/<int:account_id>/update_reminder/<int:reminder_id>', views.updateReminder, name= 'update_reminder'),
    path('users/<int:account_id>/delete_reminder/<int:reminder_id>', views.deleteReminder, name= 'delete_reminder'),

    # registration pages
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.registerPage, name='register_page'),
    path('accounts/profile/', views.userPage, name='user-page'),
]
