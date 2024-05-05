from django.urls import path
from .views import home, manage_customers, manage_books

urlpatterns = [
    path('', home, name='home'),  # Home URL pointing to the home view
    path('manage-books/', manage_books, name='manage_books'),  # Correct and unified URL for managing books
    path('manage-customers/', manage_customers, name='manage_customers'),  # Unified URL for managing customers
]

