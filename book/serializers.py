from rest_framework import serializers
from .models import Author, Genre, Condition, Location, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
        ref_name = "BookAuthor"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']
        ref_name = "BookGenre"


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['description']
        ref_name = "BookCondition"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['address', 'city', 'state', 'zip_code']
        ref_name = 'BookLocation'


class BookInputSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    genre = serializers.CharField()
    condition = serializers.CharField()
    location = LocationSerializer()

    class Meta:
        model = Book
        fields = ['title', 'description', 'author', 'genre', 'condition', 'location', 'is_available']
        ref_name = "BookInput"

    def handle_authors(self, authors_data=None):
        author_names = authors_data.split(',')
        authors_objs = [Author.objects.get_or_create(name=name.strip())[0] for name in author_names]
        return authors_objs

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)

        authors_data = validated_data.pop('author')
        authors_objs = self.handle_authors(authors_data=authors_data)

        genre_name = validated_data.pop('genre')
        genre, _ = Genre.objects.get_or_create(name=genre_name)

        condition_description = validated_data.pop('condition')
        condition, _ = Condition.objects.get_or_create(description=condition_description)

        book = Book.objects.create(location=location, genre=genre, condition=condition, **validated_data)
        book.author.set(authors_objs)

        return book

    def update(self, instance, validated_data):
        location_data = validated_data.pop("location", None)
        if location_data:
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()

        authors_data = validated_data.pop("author", None)
        if authors_data:
            authors_objs = self.handle_authors(authors_data=authors_data)
            instance.author.set(authors_objs)

        genre_data = validated_data.pop("genre", None)
        if genre_data:
            genre, _ = Genre.objects.get_or_create(name=genre_data)
            instance.genre = genre

        condition_data = validated_data.pop("condition", None)
        if condition_data:
            condition, _ = Condition.objects.get_or_create(description=condition_data)
            instance.condition = condition

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class BookOutputSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)
    genre = GenreSerializer()
    condition = ConditionSerializer()
    location = LocationSerializer()
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'author', 'genre', 'condition',
            'location', 'owner', 'owner_name', 'is_available'
        ]
        ref_name = "BookOutput"
