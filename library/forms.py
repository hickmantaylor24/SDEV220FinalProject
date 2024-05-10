from django import forms
from .models import Customer, Book, BookCopy, Transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Form to create a staff member
class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] #password2 verifies password1

    def save(self, commit=True):
        user = super().save(commit=False) # The staff is not a superuser
        user.is_staff = True  # Set the user as a staff member
        if commit:
            user.save()
        return user

# Form for the login page
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=63, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Form for adding a customer
class AddCustomerForm(forms.ModelForm):
    """
    Form for adding a new customer.
    """
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email']

# Form for removing an existing customer
class RemoveCustomerForm(forms.Form):
    """
    Uses a dropdown to select the customer to remove.
    """
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), label="Select a customer to remove")


# Form for adding a new book
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre']


# Form for adding a new book copy to an existing book
class BookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['book', 'is_available'] # Select "is_available" if the book copy is available to be checked out
    
    def __init__(self, *args, **kwargs):
        super(BookCopyForm, self).__init__(*args, **kwargs)
        self.fields['book'].label_from_instance = lambda obj: f"{obj.title} - {obj.author}" # Pulls the book title and author from the Book


# Form for removing an exciting book copy
class RemoveBookCopyForm(forms.Form):
    """
    Includes a dropdown to select from available book copies.
    """
    book_copy = forms.ModelChoiceField(queryset=BookCopy.objects.all(), label="Select Book Copy to Remove")

# Form for checking out a book copy
class CheckoutForm(forms.Form):
    """
    Includes dynamic dropdowns to select the book copy and the customer.
    """
    copy_id = forms.ModelChoiceField(queryset=BookCopy.objects.filter(is_available=True), label='Select Book Copy') # Checks if book copy is available
    customer_id = forms.ModelChoiceField(queryset=Customer.objects.all(), label='Select Customer') # Select an existing customer

# Form for returning a checked out book copy
class ReturnForm(forms.Form):
    customer_id = forms.ModelChoiceField(queryset=Customer.objects.all(), label='Select Customer') # Select existing customer
    copy_id = forms.ModelChoiceField(queryset=BookCopy.objects.none(), required=False, label='Select Book Copy') # Select a current checked out book copy

    def __init__(self, *args, **kwargs):
        super(ReturnForm, self).__init__(*args, **kwargs)
        if 'customer_id' in self.data:
            try:
                customer_id = int(self.data.get('customer_id'))
                # Filter book copies based on whether they are currently associated with an active transaction for the selected customer
                self.fields['copy_id'].queryset = BookCopy.objects.filter(
                    transactions__customer_id=customer_id,
                    transactions__return_date__isnull=True,
                    is_available=False  # Show books that are currently checked out (not available)
                )
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to empty BookCopy queryset
