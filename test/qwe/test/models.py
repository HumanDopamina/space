from django.db import models

# Create your models here.



class Author(models.Model):
    name = models.CharField(max_length=200)
    birthday = models.DateField(null=True, blank=True)  
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
        title = models.CharField(max_length=200)
        isbn = models.CharField(max_length=13, unique=True)
        publication_date = models.DateField()
        pages = models.PositiveIntegerField()
        author = models.ForeignKey(Author, on_delete=models.CASCADE)
        is_available = models.BooleanField(default=True)

        def __str__(self):
            return self.title

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower_name = models.CharField(max_length=200)
    loan_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.borrower_name} - {self.book.title}"


