from rest_framework import generics
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book, Author, Genre, Condition
from .serializers import (
    BookInputSerializer,
    BookOutputSerializer,
    AuthorSerializer,
    GenreSerializer,
    ConditionSerializer,
)
from rest_framework.serializers import ValidationError


class BookFilter(FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    author = filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    genre = filters.CharFilter(field_name="genre__name", lookup_expr="icontains")
    condition = filters.CharFilter(field_name="condition__description", lookup_expr="icontains")
    is_available = filters.BooleanFilter(field_name="is_available")

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'condition', 'is_available']


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name', 'genre__name']
    ordering_fields = ['title', 'genre', 'condition']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookInputSerializer
        return BookOutputSerializer

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            raise ValidationError({"detail": "Authentication required to create a book."})
        serializer.save(owner=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BookInputSerializer
        return BookOutputSerializer


# Author Views
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Genre Views
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ConditionListCreateView(generics.ListCreateAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ConditionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FilteredBookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookOutputSerializer
    filterset_class = BookFilter
