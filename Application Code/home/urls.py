from django.urls import path

from . import views

urlpatterns = [
   path('',views.home,name="home"),  #home
   path('signin', views.signin, name="signin"),  # home
   path('signup', views.signup, name="signup"),  # home
   # path('chat/', views.chat, name="chat"),
   # path('chat/python_file', views.python_file, name="python_file"),
]