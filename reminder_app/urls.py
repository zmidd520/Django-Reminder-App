from django.urls import path
from . import views

urlpatterns = [
    # path function defines a url pattern
    # '' is empty to represent based path to app
    # views.index is the function defined in views.py
    # name='index' parameter is to dynamically create url
    path('', views.index, name='index'),
]