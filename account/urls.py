from django.urls import path
from account import views

urlpatterns = [
    path('create', views.CreateAccount.as_view()),
    path('delete', views.DeleteAccount.as_view())
]
