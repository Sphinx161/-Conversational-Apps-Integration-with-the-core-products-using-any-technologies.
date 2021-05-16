from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name="chat"),
    #path('python_file/', views.python_file, name="python_file"),
]