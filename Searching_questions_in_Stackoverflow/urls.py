from django.urls import path
from StackOverflow import views

urlpatterns = [
    path('search_result.html', views.search, name='search_result'),

]
