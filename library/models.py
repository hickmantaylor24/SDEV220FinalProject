from django.db import models
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return {self.title} - {self.author}

# Represents a specific copy of a book in the library.
class BookCopy(models.Model):
    book = models.ForeignKey(Book, related_name='copies', on_delete=models.CASCADE)
    copy_id = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)  # Indicates if the copy is available for checkout.

    def __str__(self):
        return f'{self.book.title} - {self.book.author} - Copy {self.copy_id}'

    # Toggles the availability of the book copy.
    def toggle_availability(self):
        self.is_available = not self.is_available
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new instance
            # Assign the next copy number based on the existing copies
            last_copy = BookCopy.objects.filter(book=self.book).order_by('copy_id').last()
            self.copy_id = (last_copy.copy_id + 1) if last_copy else 1
        super(BookCopy, self).save(*args, **kwargs)

# Represents a customer of the library.
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    borrowed_book_copies = models.ManyToManyField(BookCopy, blank=True)  # Links to book copies that the customer has borrowed.

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # Checks out a book copy to the customer if it is available.
    def check_out_book(self, book_copy):
        if book_copy.is_available:
            Transaction.objects.create(book_copy=book_copy, customer=self)  # Create a new transaction record.
            book_copy.toggle_availability()  # Mark the book as checked out.
            return True
        return False

    # Handles the return of a borrowed book copy.
    def return_book(self, book_copy):
        transaction = Transaction.objects.filter(book_copy=book_copy, customer=self, return_date__isnull=True).first()
        if transaction:
            transaction.return_date = timezone.now()
            transaction.save()
            book_copy.toggle_availability()  # Mark the book as returned.
            return True
        return False

# A model for managing collections of books.
class BookList(models.Model):
    books = models.ManyToManyField(Book)  # Many-to-many relationship to Book.

    def add_book_to_list(self, book):
        self.books.add(book)  # Adds a book to the list.

    def remove_book_from_list(self, book):
        self.books.remove(book)  # Removes a book from the list.

    # Searches books based on title, author, or genre.
    def search_books(self, title=None, author=None, genre=None):
        queryset = self.books.all()
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        return queryset

    def __str__(self):
        return f'Book List with {self.books.count()} books'

# Represents a transaction record of a book copy being checked out or returned.
class Transaction(models.Model):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='transactions')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)  # Automatically set to now when the transaction is created.
    return_date = models.DateTimeField(null=True, blank=True)  # Set when the book is returned.
