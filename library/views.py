from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddCustomerForm, RemoveCustomerForm, BookForm, BookCopyForm, RemoveBookCopyForm
from .models import Book, BookCopy, Customer

def home(request):
    return render(request, 'home.html')

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

