from django.urls import reverse
from rest_framework.test import APITestCase
from library.models import User, Genre, Condition


class BookListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.genre = Genre.objects.create(name="Fiction")
        self.condition = Condition.objects.create(description="Good")
        self.valid_payload = {
            "title": "Test Book",
            "description": "Description",
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

    def test_create_book(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-list-create")
        response = self.client.post(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data["title"], "Test Book")
        self.assertEqual(response.data["location"]["city"], "Test City")
        self.assertTrue(response.data["is_available"])

    def test_create_book_unauthenticated(self):
        url = reverse("book-list-create")
        response = self.client.post(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, 403)
        self.assertIn("You must be authenticated", str(response.data))

