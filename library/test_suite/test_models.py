from django.test import TestCase
from library.models import Author, Book, BookRequest, User


class AuthorModelTest(TestCase):
    def test_author_str(self):
        author = Author.objects.create(name="J.K. Rowling")
        self.assertEqual(str(author), "J.K. Rowling")


class BookModelTest(TestCase):
    def test_book_str(self):
        owner = User.objects.create(username="testuser", email="test@example.com")
        book = Book.objects.create(title="Harry Potter", owner=owner)
        self.assertEqual(str(book), "Harry Potter")


class BookRequestModelTest(TestCase):
    def test_book_request_str(self):
        owner = User.objects.create(username="owner", email="owner@example.com")
        borrower = User.objects.create(username="borrower", email="borrower@example.com")
        book = Book.objects.create(title="Book Title", owner=owner)
        book_request = BookRequest.objects.create(book=book, borrower=borrower, owner=owner, status=BookRequest.PENDING)
        self.assertEqual(
            str(book_request),
            f"Request for {book.title} by {borrower.username} ({book_request.status})"
        )
