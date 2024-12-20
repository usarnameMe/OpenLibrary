from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Book, BookRequest, Author
from .serializers import (
    BookInputSerializer, BookOutputSerializer, BookRequestSerializer, AuthorSerializer
)


class AuthorListView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookInputSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BookInputSerializer
        return BookOutputSerializer


class BookRequestViewSet(viewsets.ModelViewSet):
    queryset = BookRequest.objects.all()  # Temporarily return all requests
    serializer_class = BookRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
