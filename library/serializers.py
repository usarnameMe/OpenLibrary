from rest_framework import serializers
from .models import Author, Genre, Condition, Location, BookRequest
import logging
from book.models import Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
        ref_name = "LibraryAuthor"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        ref_name = "LibraryGenre"


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['id', 'description']
        ref_name = "LibraryCondition"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'address', 'city', 'state', 'zip_code']
        ref_name = 'LibraryLocation'


class BookInputSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    location = LocationSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'genre', 'condition', 'location', 'is_available']
        ref_name = "LibraryBookInput"


class BookOutputSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)
    genre = GenreSerializer()
    condition = ConditionSerializer()
    location = LocationSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'genre', 'condition', 'location', 'is_available']
        ref_name = "LibraryBookOutput"


logger = logging.getLogger(__name__)


class BookRequestSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookRequest
        fields = ['id', 'book_id', 'borrower', 'owner', 'status', 'created_at']

    def validate_book_id(self, value):
        logger.debug(f"Validating book ID: {value}")
        try:
            book = Book.objects.get(id=value)
            logger.debug(f"Book found: {book.title} (ID: {book.id})")
        except Book.DoesNotExist:
            logger.error(f"Book with ID {value} does not exist.")
            raise serializers.ValidationError("This book does not exist.")
        if not book.is_available:
            logger.error(f"Book with ID {value} is not available.")
            raise serializers.ValidationError("This book is currently not available.")
        return value

    def create(self, validated_data):
        book_id = validated_data.pop('book_id')
        book = Book.objects.get(id=book_id)
        if book.owner == self.context['request'].user:
            raise serializers.ValidationError("You cannot request your own book.")
        book_request = BookRequest.objects.create(book=book, **validated_data)
        return book_request
