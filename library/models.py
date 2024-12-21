from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Condition(models.Model):
    description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.description


class Location(models.Model):
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        state_part = f", {self.state}" if self.state else ""
        return f"{self.address}, {self.city}{state_part}, {self.zip_code}"


class BookRequest(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    book = models.ForeignKey('book.Book', on_delete=models.CASCADE,
                             related_name='requests')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library_borrowed_requests')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library_owned_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def approve_request(self):
        if self.status != self.PENDING:
            raise ValueError("Only pending requests can be approved.")
        self.status = self.APPROVED
        self.book.is_available = False
        self.book.save()
        self.save()
        BookRequest.objects.filter(book=self.book, status=self.PENDING).exclude(pk=self.pk).update(status=self.REJECTED)

    def __str__(self):
        return f"Request for {self.book.title} by {self.borrower.username} ({self.status})"
