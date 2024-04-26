from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manage-books/', views.manage_books, name='manage_books'),
    path('manage-users/', views.manage_users, name='manage_users'),
]
