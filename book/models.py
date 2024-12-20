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


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ManyToManyField(Author, related_name="books")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name="books")
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True, related_name="books")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="books")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_books")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
