from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class BookCopy(models.Model):
    book = models.ForeignKey(Book, related_name='copies', on_delete=models.CASCADE)
    copy_id = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.book.title} - Copy {self.copy_id}'

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    borrowed_book_copies = models.ManyToManyField(BookCopy, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class BookList(models.Model):
    books = models.ManyToManyField(Book)

    def add_book_to_list(self, book):
        self.books.add(book)

    def remove_book_from_list(self, book):
        self.books.remove(book)

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
