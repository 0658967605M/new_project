from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================
# Publisher (Publishing House)
# =========================
class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# =========================
# Custom User
# =========================
class User(AbstractUser):

    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Journalists & Editors can belong to a Publisher
    publisher_profile = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members"
    )

    # Readers subscribe to journalists
    subscriptions_journalists = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="subscribers",
        limit_choices_to={'role': 'journalist'}
    )

    # Readers subscribe to publishers
    subscriptions_publishers = models.ManyToManyField(
        Publisher,
        blank=True,
        related_name="publisher_subscribers"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


# =========================
# Article
# =========================
class Article(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    approved = models.BooleanField(default=False)

    # Journalist who created it
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    # OPTIONAL publisher
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ======================
# Reader Subscriptions
# ======================
class Subscription(models.Model):
    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions"
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

    def __str__(self):
        if self.journalist:
            return f"{self.reader.username} → {self.journalist.username}"
        if self.publisher:
            return f"{self.reader.username} → {self.publisher.name}"
