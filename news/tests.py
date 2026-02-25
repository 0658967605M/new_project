from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Article, Publisher, Subscription, Newsletter

User = get_user_model()


class BaseTestSetup(TestCase):
    """
    Base test class that sets up users and common test data.
    """

    def setUp(self):
        # Create users WITH UNIQUE EMAILS (IMPORTANT for MariaDB)
        self.reader = User.objects.create_user(
            username="reader1",
            email="reader1@test.com",
            password="pass123",
            role="reader"
        )

        self.journalist = User.objects.create_user(
            username="journalist1",
            email="journalist1@test.com",
            password="pass123",
            role="journalist"
        )

        self.editor = User.objects.create_user(
            username="editor1",
            email="editor1@test.com",
            password="pass123",
            role="editor"
        )

        # Create publisher
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            owner=self.editor
        )

        # Create article
        self.article = Article.objects.create(
            title="Test Article",
            content="Test Content",
            created_by=self.journalist,
            publisher=self.publisher,
            approved=False
        )


# ===============================
# Authentication Tests
# ===============================

class AuthenticationTests(BaseTestSetup):

    def test_login(self):
        response = self.client.post(reverse("login"), {
            "username": "reader1",
            "password": "pass123"
        })
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username="reader1", password="pass123")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"))


# ===============================
# Dashboard Tests
# ===============================

class DashboardTests(BaseTestSetup):

    def test_reader_dashboard_access(self):
        self.client.login(username="reader1", password="pass123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_journalist_dashboard_access(self):
        self.client.login(username="journalist1", password="pass123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_editor_dashboard_access(self):
        self.client.login(username="editor1", password="pass123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)


# ===============================
# Article Tests
# ===============================

class ArticleTests(BaseTestSetup):

    def test_journalist_can_create_article(self):
        self.client.login(username="journalist1", password="pass123")

        response = self.client.post(reverse("create_article"), {
            "title": "New Article",
            "content": "Content here",
            "publisher": self.publisher.id
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Article.objects.filter(title="New Article").exists()
        )

    def test_editor_can_approve_article(self):
        self.client.login(username="editor1", password="pass123")

        response = self.client.get(
            reverse("approve_article", args=[self.article.id])
        )

        self.article.refresh_from_db()
        self.assertTrue(self.article.approved)
        self.assertEqual(response.status_code, 302)

    def test_journalist_can_delete_own_article(self):
        self.client.login(username="journalist1", password="pass123")

        response = self.client.get(
            reverse("delete_article", args=[self.article.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Article.objects.filter(id=self.article.id).exists()
        )


# ===============================
# Subscription Tests
# ===============================

class SubscriptionTests(BaseTestSetup):

    def test_reader_can_subscribe_journalist(self):
        self.client.login(username="reader1", password="pass123")

        response = self.client.get(
            reverse("subscribe_journalist", args=[self.journalist.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Subscription.objects.filter(
                reader=self.reader,
                journalist=self.journalist
            ).exists()
        )

    def test_reader_can_subscribe_publisher(self):
        self.client.login(username="reader1", password="pass123")

        response = self.client.get(
            reverse("subscribe_publisher", args=[self.publisher.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Subscription.objects.filter(
                reader=self.reader,
                publisher=self.publisher
            ).exists()
        )


# ===============================
# Newsletter Tests
# ===============================

class NewsletterTests(BaseTestSetup):

    def setUp(self):
        super().setUp()
        self.newsletter = Newsletter.objects.create(
            title="Test Newsletter",
            content="Newsletter content",
            author=self.journalist,
            publisher=self.publisher,
            approved=False
        )

    def test_editor_can_approve_newsletter(self):
        self.client.login(username="editor1", password="pass123")

        response = self.client.get(
            reverse("approve_newsletter", args=[self.newsletter.id])
        )

        self.newsletter.refresh_from_db()
        self.assertTrue(self.newsletter.approved)
        self.assertEqual(response.status_code, 302)
