from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StaffUserCreationForm, AddCustomerForm, RemoveCustomerForm, BookForm, BookCopyForm, RemoveBookCopyForm, LoginForm, CheckoutForm, ReturnForm
from .models import Book, BookCopy, Customer, Transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.utils import timezone
from django.http import HttpResponse, JsonResponse


def home(request):
    context = {'on_home_page': True}  # Context variable for home page
    return render(request, 'home.html', context)

def manage_staff(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied: You do not have permission to view this page.")
        return redirect('access_denied')  # Redirect non-superusers to an access denied page (make sure this route exists)

    if request.method == 'POST':
        if 'create' in request.POST:  # Check if this is a create request
            form = StaffUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Staff member added successfully.')
                return redirect('manage_staff')  # Reload the page after creation
            else:
                # If the form is not valid, render the page again with the form to show validation errors
                messages.error(request, 'Failed to add staff member. Please check the form for errors.')
        elif 'delete' in request.POST:  # Check if this is a delete request
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(id=user_id, is_staff=True, is_superuser=False)  # Ensure only staff users can be deleted
                user.delete()
                messages.success(request, 'Staff member deleted successfully.')
            except User.DoesNotExist:
                messages.error(request, 'Failed to delete staff member: User does not exist.')
            return redirect('manage_staff')  # Reload the page after deletion

    else:
        form = StaffUserCreationForm()

    staff_members = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'manage_staff.html', {'form': form, 'staff_members': staff_members})

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
                    return redirect('home')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()  # Instantiate an empty LoginForm for GET requests
    return render(request, 'login.html', {'form': form})

#admin dashboard
def admin_dashboard(request):
    context = {'on_admin_dashboard': True}  # Context variable for admin dashboard
    return render(request, 'admin_dashboard.html', context)


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


def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            book_copy = form.cleaned_data['copy_id']  # This should directly provide a BookCopy instance
            customer = form.cleaned_data['customer_id']  # This should directly provide a Customer instance

            if book_copy.is_available:
                # method in the Customer model check_out_book handles the logic.
                if customer.check_out_book(book_copy):  # This method would also update 'is_available' within it.
                    messages.success(request, "Book checked out successfully!")
                    return redirect('checkout')  
                else:
                    messages.error(request, "This book is currently not available.")
            else:
                messages.error(request, "This book is currently not available.")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})

def return_book(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            # Directly use the BookCopy and Customer instances provided by the form
            book_copy = form.cleaned_data['copy_id']
            customer = form.cleaned_data['customer_id']

            # Call a method in the Customer model that handles the logic of returning a book
            if customer.return_book(book_copy):
                messages.success(request, "Book returned successfully!")
            else:
                messages.error(request, "This book was not checked out by this customer or has already been returned.")
        else:
            # Collect and show all form errors if the form is not valid
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ReturnForm()

    return render(request, 'return.html', {'form': form})

def get_books(request):
    customer_id = request.GET.get('customer_id')
    action = request.GET.get('action')

    if not customer_id or not action:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)

    if action == 'return':
        # Fetching book copies that are currently checked out by the customer and not yet returned
        transactions = Transaction.objects.filter(
            customer=customer,
            return_date__isnull=True
        ).select_related('book_copy').filter(book_copy__is_available=False)

        book_list = [{'id': txn.book_copy.id, 'title': f"{txn.book_copy.book.title} - Copy {txn.book_copy.copy_id}"} for txn in transactions]
    else:
        return JsonResponse({'error': 'Invalid action specified'}, status=400)

    return JsonResponse({'books': book_list})