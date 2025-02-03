from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('register', register_user, name='register_user'),
    path('about', about, name='about'),
    path('platform',platform , name='platform'),
    path('categories', categories, name='categories'),
    path('guide',guide, name='guide'),
    path('testimonals',testimonals, name='testimonals'),

]