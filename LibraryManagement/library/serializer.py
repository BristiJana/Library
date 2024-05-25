from rest_framework import serializers
from .models import Book, Borrower

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','title', 'author', 'isbn', 'publication_date', 'available']

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id','name', 'email', 'borrowed_books']

class BorrowBookSerializer(serializers.Serializer):
    borrower_id = serializers.IntegerField()
    book_ids = serializers.ListField(
        child=serializers.IntegerField()
    )