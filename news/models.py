"""
Models module for the News Application.

Defines database models including:
- Custom User
- Publisher
- Article
- Subscription
- Newsletter
- Notification
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Adds a role field to distinguish between:
    - Reader
    - Journalist
    - Editor

    Email field is enforced as unique.
    """

    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)

    def __str__(self):
        """
        Return string representation of the user.
        """
        return f"{self.username} ({self.role})"


class Publisher(models.Model):
    """
    Represents a publishing organization.

    A publisher may optionally have an owner (User).
    """

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        """
        Return publisher name.
        """
        return self.name


class Article(models.Model):
    """
    Represents a news article created by a journalist.

    Articles may optionally belong to a publisher
    and require approval before publication.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    approved = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return article title.
        """
        return self.title


class Subscription(models.Model):
    """
    Represents a subscription relationship.

    A reader can subscribe to:
    - A journalist
    - A publisher
    - An editor

    Unique constraints prevent duplicate subscriptions.
    """

    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reader_subscriptions"
    )

    editor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="editor_followers"
    )

    journalist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="journalist_followers"
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="publisher_followers"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Ensure a reader cannot duplicate subscriptions.
        """
        unique_together = (
            ("reader", "journalist"),
            ("reader", "publisher"),
        )

    def __str__(self):
        """
        Return readable subscription description.
        """
        if self.journalist:
            return f"{self.reader.username} → {self.journalist.username}"
        if self.publisher:
            return f"{self.reader.username} → {self.publisher.name}"
        return "Subscription"


class Newsletter(models.Model):
    """
    Represents a newsletter created by an author
    and associated with a publisher.

    Newsletters may require approval before distribution.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return newsletter title.
        """
        return self.title


class Notification(models.Model):
    """
    Represents a system notification sent to a user.

    Used to inform users about events such as:
    - Article approval
    - Newsletter publication
    - Subscription updates
    """

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return readable notification description.
        """
        return f"Notification for {self.recipient.username}"
