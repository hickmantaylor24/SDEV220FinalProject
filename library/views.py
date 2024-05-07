from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddCustomerForm, RemoveCustomerForm, BookForm, BookCopyForm, RemoveBookCopyForm, LoginForm
from .models import Book, BookCopy, Customer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

def home(request):
    return render(request, 'home.html')


def library_management_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # Use the custom LoginForm
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_dashboard')
                elif user.is_staff:
                    login(request, user)
                    return redirect('staff_dashboard')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()  # Instantiate an empty LoginForm for GET requests
    return render(request, 'login.html', {'form': form})

#admin dashboard
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def manage_customers(request):
    if request.method == 'POST':
        if 'add_customer' in request.POST:
            add_form = AddCustomerForm(request.POST)
            if add_form.is_valid():
                add_form.save()
                messages.success(request, 'Customer added successfully!')
                return redirect('manage_customers')
        elif 'remove_customer' in request.POST:
            remove_form = RemoveCustomerForm(request.POST)
            if remove_form.is_valid():
                customer = remove_form.cleaned_data['customer']
                customer.delete()
                messages.success(request, 'Customer removed successfully!')
                return redirect('manage_customers')
    else:
        add_form = AddCustomerForm()
        remove_form = RemoveCustomerForm()

    return render(request, 'manage_customers.html', {
        'add_form': add_form,
        'remove_form': remove_form
    })

def manage_books(request):
    book_form = BookForm()
    book_copy_form = BookCopyForm()
    remove_book_copy_form = RemoveBookCopyForm()

    if request.method == 'POST':
        if 'add_book' in request.POST:
            book_form = BookForm(request.POST)
            if book_form.is_valid():
                book_form.save()
                messages.success(request, 'Book added successfully!')
                return redirect('manage_books')
        elif 'add_book_copy' in request.POST:
            book_copy_form = BookCopyForm(request.POST)
            if book_copy_form.is_valid():
                book_copy_form.save()
                messages.success(request, 'Book copy added successfully!')
                return redirect('manage_books')
        elif 'remove_book_copy' in request.POST:
            remove_book_copy_form = RemoveBookCopyForm(request.POST)
            if remove_book_copy_form.is_valid():
                book_copy = remove_book_copy_form.cleaned_data['book_copy']
                book_copy.delete()
                messages.success(request, 'Book copy removed successfully!')
                return redirect('manage_books')

    return render(request, 'manage_books.html', {
        'book_form': book_form,
        'book_copy_form': book_copy_form,
        'remove_book_copy_form': remove_book_copy_form
    })