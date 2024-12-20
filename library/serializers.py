from rest_framework import serializers
from .models import Author, Genre, Condition, Location, Book, BookRequest
import logging


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
        try:
            book = Book.objects.get(id=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("This book does not exist.")
        return value

    def create(self, validated_data):
        book_id = validated_data.pop('book_id')
        book = Book.objects.get(id=book_id)
        book_request = BookRequest.objects.create(book=book, **validated_data)
        return book_request
