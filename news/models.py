from django.db import models
from django.contrib.auth.models import AbstractUser


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('publisher', 'Publisher'),
        ('editor', 'Editor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    approved = models.BooleanField(default=False)

    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
