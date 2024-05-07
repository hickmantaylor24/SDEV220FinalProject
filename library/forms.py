from django import forms
from .models import Customer, Book, BookCopy
from django.contrib.auth.forms import AuthenticationForm


#Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=63, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Form for adding a new customer
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
    Form for removing an existing customer.
    Uses a dropdown to select the customer to remove.
    """
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), label="Select a customer to remove")

# Form for adding a new book
class BookForm(forms.ModelForm):
    """
    Form for adding a new book.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre']

# Form for adding a new book copy
class BookCopyForm(forms.ModelForm):
    """
    Form for adding a new book copy.
    Includes a dropdown to select which book the copy belongs to.
    """
    class Meta:
        model = BookCopy
        fields = ['book', 'copy_id', 'is_available']

# Form for removing an existing book copy
class RemoveBookCopyForm(forms.Form):
    """
    Form for removing an existing book copy.
    Includes a dropdown to select from available book copies.
    """
    book_copy = forms.ModelChoiceField(queryset=BookCopy.objects.all(), label="Select Book Copy to Remove")