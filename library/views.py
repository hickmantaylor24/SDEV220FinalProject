from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StaffUserCreationForm, AddCustomerForm, RemoveCustomerForm, BookForm, BookCopyForm, RemoveBookCopyForm, LoginForm, CheckoutForm, ReturnForm
from .models import Book, BookCopy, Customer, Transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.utils import timezone
from django.http import HttpResponse, JsonResponse

# Home page
def home(request):
    context = {'on_home_page': True}  # Context variable for home page
    return render(request, 'home.html', context)

# Managing staff functions - add/remove staff members
def manage_staff(request):
    if not request.user.is_superuser: # Denies staff to admin (superuser) permissions 
        messages.error(request, "Access denied: You do not have permission to view this page.")
        return redirect('access_denied')  # Redirect staff (non-superusers) to an access denied page (make sure this route exists)

    if request.method == 'POST':
        if 'create' in request.POST:  # Check if this is a create request
            form = StaffUserCreationForm(request.POST)
            if form.is_valid(): # Check if the form is valid
                form.save() # Save the form data to the database
                messages.success(request, 'Staff member added successfully.') # Conformation message
                return redirect('manage_staff')  # Reload the page after creation
            else:
                # If the form is not valid, render the page again with the form to show validation errors
                messages.error(request, 'Failed to add staff member. Please check the form for errors.')
        elif 'delete' in request.POST:  # Check if this is a delete request
            user_id = request.POST.get('user_id')
            try:
                user = User.objects.get(id=user_id, is_staff=True, is_superuser=False)  # Ensure only staff users can be deleted
                user.delete() # Deletes staff member
                messages.success(request, 'Staff member deleted successfully.') # Conformation message
            except User.DoesNotExist: # Checks if staff member exists
                messages.error(request, 'Failed to delete staff member: User does not exist.') # Error message
            return redirect('manage_staff')  # Reload the page after deletion

    else: # If it's not a POST request, instantiate an empty StaffUserCreationForm
        form = StaffUserCreationForm()
    
    staff_members = User.objects.filter(is_staff=True, is_superuser=False) # All staff members who are not superusers
    return render(request, 'manage_staff.html', {'form': form, 'staff_members': staff_members}) # Render the 'manage_staff.html' template with the form and staff members



# Login function
def library_management_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # Use the custom LoginForm
        if form.is_valid(): # Check if the form is valid
            # Extract the username and password from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password) # Authenticate the user
            if user is not None and user.is_active: # Check if user authentication is successful and the user is active
                # If the user is a superuser, redirect to the admin dashboard
                if user.is_superuser: 
                    login(request, user) # login as admin
                    return redirect('admin_dashboard')
                # If the user is a staff member, redirect to the home page
                elif user.is_staff:
                    login(request, user) # login as staff member
                    return redirect('home')
            else: # If authentication fails or user is not active,
                return render(request, 'login.html', {'error_message': 'Invalid credentials'}) # Error message
    else:
        form = LoginForm()  # Instantiate an empty LoginForm for GET requests
    return render(request, 'login.html', {'form': form}) # Render the login.html template with the form

# Admin dashboard
def admin_dashboard(request):
    context = {'on_admin_dashboard': True}  # Context variable for admin dashboard
    return render(request, 'admin_dashboard.html', context)

# Manage customer functions - add/remove customers of the library
def manage_customers(request):
    if request.method == 'POST':
        if 'add_customer' in request.POST: # Check if this is a 'add_customer' request
            add_form = AddCustomerForm(request.POST) # Use AddCustomerForm
            if add_form.is_valid(): # Check if the form is valid
                add_form.save() # Save the customer to the database
                messages.success(request, 'Customer added successfully!') # Conformation message
                return redirect('manage_customers')
        elif 'remove_customer' in request.POST: # Check if this is a 'remove_customer' request
            remove_form = RemoveCustomerForm(request.POST) # Uses RemoveCustomerForm
            if remove_form.is_valid(): # Check if the form is valid
                customer = remove_form.cleaned_data['customer'] # Retrieve the customer to be removed
                customer.delete() # Delete the customer from the database
                messages.success(request, 'Customer removed successfully!') # Conformation message
                return redirect('manage_customers')
    else:
        add_form = AddCustomerForm()
        remove_form = RemoveCustomerForm()
        
    # Render the manage_customers.html template with forms
    return render(request, 'manage_customers.html', {
        'add_form': add_form,
        'remove_form': remove_form
    })

# Manage book functions - add book, add/remove book copy
def manage_books(request):
    book_form = BookForm() # Form for adding a new book
    book_copy_form = BookCopyForm() # Form for adding a new copy of a book
    remove_book_copy_form = RemoveBookCopyForm() # Form for removing an existing book

    if request.method == 'POST':
        if 'add_book' in request.POST: # Check if this is a 'add_book' request
            book_form = BookForm(request.POST) # Uses BookForm
            if book_form.is_valid(): # Check if the form is valid
                book_form.save() # Saves the book to the database
                messages.success(request, 'Book added successfully!') # Conformation message
                return redirect('manage_books')
        elif 'add_book_copy' in request.POST: # Check if this is a 'add_book_copy' request
            book_copy_form = BookCopyForm(request.POST) # Uses BookCopyForm
            if book_copy_form.is_valid(): # Check if book_copy_form is valid
                book_copy_form.save() # Saves the copy to the database
                messages.success(request, 'Book copy added successfully!') # Conformation Message
                return redirect('manage_books')
        elif 'remove_book_copy' in request.POST: # Check if this is a 'remove_book_copy' request
            remove_book_copy_form = RemoveBookCopyForm(request.POST)
            if remove_book_copy_form.is_valid(): # Check if remove_book_copy_form is valid
                book_copy = remove_book_copy_form.cleaned_data['book_copy']
                book_copy.delete()  # Delete the book copy from the database
                messages.success(request, 'Book copy removed successfully!') # Conformation message
                return redirect('manage_books')
    # Render the manage_books.html template with the forms
    return render(request, 'manage_books.html', {
        'book_form': book_form,
        'book_copy_form': book_copy_form,
        'remove_book_copy_form': remove_book_copy_form
    })

# Checkout book copy function
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST) # Uses CheckoutForm
        if form.is_valid(): # Check if the form is valid
            book_copy = form.cleaned_data['copy_id']  # This should directly provide a BookCopy instance
            customer = form.cleaned_data['customer_id']  # This should directly provide a Customer instance

            if book_copy.is_available: # Check if the book copy is available
                # method in the Customer model check_out_book handles the logic.
                if customer.check_out_book(book_copy):  # This method would also update 'is_available' within it.
                    messages.success(request, "Book checked out successfully!") # Conformation message
                    return redirect('checkout')  
                else:
                    messages.error(request, "This book is currently not available.") # Error message if book is not available
            else:
                messages.error(request, "This book is currently not available.") # Error message if book is not available
        else: # Collect and show all form errors if the form is not valid
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CheckoutForm()
    # Render the checkout.html template with the form
    return render(request, 'checkout.html', {'form': form})

# Returning a book copy function
def return_book(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid(): # Check if the form is valid
            # Directly use the BookCopy and Customer instances provided by the form
            book_copy = form.cleaned_data['copy_id']
            customer = form.cleaned_data['customer_id']

            # Call a method in the Customer model that handles the logic of returning a book
            if customer.return_book(book_copy):
                messages.success(request, "Book returned successfully!") # Conformation message
            else:
                messages.error(request, "This book was not checked out by this customer or has already been returned.") # Error message
        else:
            # Collect and show all form errors if the form is not valid
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ReturnForm()
    # Render the return.html template with the form
    return render(request, 'return.html', {'form': form})

# Function for adding book copies to customers
def get_books(request):
    customer_id = request.GET.get('customer_id')
    action = request.GET.get('action')
    # Check if customer_id or action parameters are missing
    if not customer_id or not action:
        return JsonResponse({'error': 'Missing required parameters'}, status=400) # Error message

    try:
        customer = Customer.objects.get(pk=customer_id) # Retrieve the customer object based on the provided customer_id
    except Customer.DoesNotExist: # If customer is not found - error message
        return JsonResponse({'error': 'Customer not found'}, status=404) 

    if action == 'return':
        # Fetching book copies that are currently checked out by the customer and not yet returned
        transactions = Transaction.objects.filter(
            customer=customer,
            return_date__isnull=True
        ).select_related('book_copy').filter(book_copy__is_available=False)
    # Create a list of dictionaries containing book's id, title, and copy id
        book_list = [{'id': txn.book_copy.id, 'title': f"{txn.book_copy.book.title} - Copy {txn.book_copy.copy_id}"} for txn in transactions]
    else:
        return JsonResponse({'error': 'Invalid action specified'}, status=400) # If JSON response is not returned - error message
    # Return JSON response with the list of books
    return JsonResponse({'books': book_list})
