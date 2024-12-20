from unittest import TestCase

from django.contrib.auth import get_user_model

from library.models import Genre, Condition
from library.serializers import BookInputSerializer

User = get_user_model()


class BookInputSerializerTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction")
        self.condition = Condition.objects.create(description="Good")
        self.user = User.objects.create_user(username="testuser", password="pass123")

        self.valid_data = {
            "title": "Test Book",
            "description": "Test Description",
            "author": "Author1, Author2",
            "genre": self.genre.name,
            "condition": self.condition.description,
            "location": {
                "address": "123 Test Street",
                "city": "Test City",
                "state": "Test State",
                "zip_code": "12345"
            },
            "is_available": True
        }

    def test_valid_serializer(self):
        serializer = BookInputSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save(owner=self.user)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.location.city, "Test City")
        self.assertEqual(book.author.count(), 2)
