from rest_framework import viewsets, status,mixins
from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse("Welcome to the Home Page")
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        borrower = self.get_object()
        books = request.data.get('borrowed_books')
        if books:
            borrower.borrowed_books.set(books)
        return super().update(request, *args, **kwargs)

class BorrowBookViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = BorrowBookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrower_id = serializer.validated_data['borrower_id']
        book_ids = serializer.validated_data['book_ids']
        try:
            borrower = Borrower.objects.get(pk=borrower_id)
            for book_id in book_ids:
                book = Book.objects.get(pk=book_id)
                if book.available:
                    book.available = False
                    book.save()
                    borrower.borrowed_books.add(book)
                else:
                    return Response({'error': f'Book with id {book_id} is not available'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_200_OK)
        except (Book.DoesNotExist, Borrower.DoesNotExist):
            return Response({'error': 'Book or Borrower not found'}, status=status.HTTP_404_NOT_FOUND)
    def update(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            borrower_id = request.data.get('borrower_id')
            borrower = Borrower.objects.get(pk=borrower_id)
            if book.available:
                book.available = False
                book.save()
                borrower.borrowed_books.add(book)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except (Book.DoesNotExist, Borrower.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

class ReturnBookViewSet(viewsets.ViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        borrower_id = request.data.get('borrower_id')
        try:
            book = Book.objects.get(pk=book_id)
            borrower = Borrower.objects.get(pk=borrower_id)
            
            if book.available:
                return Response({"error": "Book is already available"}, status=status.HTTP_400_BAD_REQUEST)
            
            book.available = True
            book.save()
            borrower.borrowed_books.remove(book)
            borrower.save()
            
            return Response(status=status.HTTP_200_OK)
        
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except Borrower.DoesNotExist:
            return Response({"error": "Borrower not found"}, status=status.HTTP_404_NOT_FOUND)