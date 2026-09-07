from rest_framework import serializers

from .models import Author, Book, Loan


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'birthday', 'country']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'isbn',
            'publication_date',
            'pages',
            'author',
            'is_available',
        ]


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            'id',
            'book',
            'borrower_name',
            'loan_date',
            'due_date',
            'return_date',
        ]
