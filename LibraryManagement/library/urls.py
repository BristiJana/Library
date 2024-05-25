from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BorrowerViewSet, BorrowBookViewSet, ReturnBookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrowers', BorrowerViewSet)
router.register(r'borrow', BorrowBookViewSet, basename='borrow')
router.register(r'return', ReturnBookViewSet, basename='return')

urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve'}), name='book-detail'),
]