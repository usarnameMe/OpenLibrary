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
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = BookRequest
        fields = ['id', 'book', 'borrower', 'owner', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

    def validate(self, data):
        logger.debug(f"Validating data for BookRequest: {data}")
        if 'book' not in data:
            logger.error("Book field is missing.")
            raise serializers.ValidationError({"book": "This field is required."})
        if not data['book'].is_available:
            logger.error(f"Book with ID {data['book'].id} is not available.")
            raise serializers.ValidationError({"book": "This book is not available."})
        return data
