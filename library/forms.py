from django import forms
from .models import Customer, Book, BookCopy, Transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Set the user as a staff member
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=63, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AddCustomerForm(forms.ModelForm):
    """
    Form for adding a new customer.
    """
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email']

class RemoveCustomerForm(forms.Form):
    """
    Form for removing an existing customer.
    Uses a dropdown to select the customer to remove.
    """
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), label="Select a customer to remove")

class BookForm(forms.ModelForm):
    """
    Form for adding a new book.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre']

class BookCopyForm(forms.ModelForm):
    """
    Form for adding a new book copy.
    """
    class Meta:
        model = BookCopy
        fields = ['book', 'is_available']
    
    def __init__(self, *args, **kwargs):
        super(BookCopyForm, self).__init__(*args, **kwargs)
        self.fields['book'].label_from_instance = lambda obj: f"{obj.title} - {obj.author}"

class RemoveBookCopyForm(forms.Form):
    """
    Form for removing an existing book copy.
    Includes a dropdown to select from available book copies.
    """
    book_copy = forms.ModelChoiceField(queryset=BookCopy.objects.all(), label="Select Book Copy to Remove")

class CheckoutForm(forms.Form):
    """
    Form for checking out a book copy.
    Includes dynamic dropdowns to select the book copy and the customer.
    """
    copy_id = forms.ModelChoiceField(queryset=BookCopy.objects.filter(is_available=True), label='Select Book Copy')
    customer_id = forms.ModelChoiceField(queryset=Customer.objects.all(), label='Select Customer')

class ReturnForm(forms.Form):
    customer_id = forms.ModelChoiceField(queryset=Customer.objects.all(), label='Select Customer')
    copy_id = forms.ModelChoiceField(queryset=BookCopy.objects.none(), required=False, label='Select Book Copy')

    def __init__(self, *args, **kwargs):
        super(ReturnForm, self).__init__(*args, **kwargs)
        if 'customer_id' in self.data:
            try:
                customer_id = int(self.data.get('customer_id'))
                # Filter book copies based on whether they are currently associated with an active transaction for the selected customer
                self.fields['copy_id'].queryset = BookCopy.objects.filter(
                    transactions__customer_id=customer_id,
                    transactions__return_date__isnull=True,
                    is_available=False  #show books that are currently checked out (not available)
                )
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty BookCopy queryset