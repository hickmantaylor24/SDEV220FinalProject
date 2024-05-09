from django.urls import path
from .views import manage_staff, home, return_book, manage_customers, manage_books, library_management_login, admin_dashboard, checkout, get_books
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', home, name='home'),  # URL for the staff dashboard
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),  # URL for the admin dashboard
    path('manage-books/', manage_books, name='manage_books'),  # Correct and unified URL for managing books
    path('manage-customers/', manage_customers, name='manage_customers'),  # Unified URL for managing customers
    path('', library_management_login, name='login'),  # Set this as the root URL
    path('checkout/', checkout, name='checkout'),  # for the checkout page,
    path('return/', return_book, name='return_book'),  # URL for returning books
    path('ajax/get_books/', get_books, name='get_books'),  # Example for AJAX URL,
    path('manage_staff/', manage_staff, name='manage_staff'),  # Correct and unified URL for managing staff
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]

