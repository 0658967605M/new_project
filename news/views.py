from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import ArticleForm, ArticleUpdateForm, CustomUserCreationForm
from .models import Article, Publisher, User, Subscription, Newsletter, Notification, Article
from django.core.mail import send_mail
from .forms import NewsletterForm
from rest_framework import generics
from .serializers import ArticleSerializer


# =========================
# API VIEWS
# =========================
class ArticleListAPIView(generics.ListAPIView):
    """
    API view that returns a list of all approved articles.
    """
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(approved=True)


class ArticleDetailAPIView(generics.RetrieveAPIView):
    """
    API view that returns details of a single approved article.
    """
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(approved=True)


# ======================
# Home
# ======================
def home(request):
    """
    Render the home page.
    """
    return render(request, "news/home.html")


# ======================
# Register (redirects to login)
# ======================
def register(request):
    """
    Handle user registration. 
    On successful registration, redirect user to login page.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "news/register.html", {"form": form})


# ======================
# Login
# ======================
def login_view(request):
    """
    Authenticate and log in a user.
    Redirects to the next page if provided, otherwise to dashboard.
    """
    next_url = request.GET.get("next")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(next_url or "dashboard")

        messages.error(request, "Invalid username or password")

    return render(request, "news/login.html")


# ======================
# Logout
# ======================
@login_required
def logout_views(request):
    """
    Log out the currently authenticated user
    and redirect to the home page.
    """
    logout(request)
    return redirect("home")


# ---------------
# Dashboard
# ---------------
@login_required
def dashboard(request):
    """
    Display dashboard based on user role:
    - Journalist: shows own articles
    - Editor: shows pending articles
    - Reader: shows subscribed content feed
    """
    user = request.user

    publishers = Publisher.objects.all()

    user_subscriptions = Subscription.objects.filter(
        reader=user,
        publisher__isnull=False
    ).values_list("publisher_id", flat=True)

    notifications = Notification.objects.filter(
        recipient=user
    ).order_by("-created_at")

    if user.role == "journalist":
        articles = Article.objects.filter(created_by=user)

        return render(request, "news/journalist_dashboard.html", {
            "articles": articles,
            "publishers": publishers,
            "user_subscriptions": list(user_subscriptions),
            "notifications": notifications
        })

    elif user.role == "editor":
        pending_articles = Article.objects.filter(approved=False)

        publishers = Publisher.objects.all()

        user_subscriptions = Subscription.objects.filter(
            reader=user,
            publisher__isnull=False
        ).values_list("publisher_id", flat=True)

        notifications = Notification.objects.filter(
            recipient=user
        ).order_by("-created_at")

        return render(request, "news/editor_dashboard.html", {
            "pending_articles": pending_articles,
            "publishers": publishers,
            "user_subscriptions": list(user_subscriptions),
            "notifications": notifications
        })

    else:
        journalist_subs = Subscription.objects.filter(
            reader=user,
            journalist__isnull=False
        ).values_list("journalist", flat=True)

        publisher_subs = Subscription.objects.filter(
            reader=user,
            publisher__isnull=False
        ).values_list("publisher", flat=True)

        if journalist_subs or publisher_subs:
            articles = (
                Article.objects.filter(
                    approved=True,
                    created_by__in=journalist_subs
                )
                |
                Article.objects.filter(
                    approved=True,
                    publisher__in=publisher_subs
                )
            )
        else:
            articles = Article.objects.filter(approved=True)

        articles = articles.distinct().order_by("-created_at")

        return render(request, "news/reader_dashboard.html", {
            "articles": articles,
            "notifications": notifications
        })


# ------------------
# Read Article
# ------------------
@login_required
def read_article(request, article_id):
    """
    Display a single article.
    Readers cannot access unapproved articles.
    """
    article = get_object_or_404(Article, id=article_id)

    if not article.approved and request.user.role == "reader":
        messages.error(request, "Article not approved yet.")
        return redirect("dashboard")

    return render(request, "news/read_article.html", {"article": article})


# ======================
# Create Article (Journalist)
# ======================
@login_required
def create_article(request):
    """
    Allow journalists to create a new article.
    Sends notifications to subscribers after creation.
    """
    if request.user.role != "journalist":
        return redirect("dashboard")

    subscribed_publisher_ids = Subscription.objects.filter(
        reader=request.user,
        publisher__isnull=False
    ).values_list("publisher_id", flat=True)

    publishers = Publisher.objects.filter(
        id__in=subscribed_publisher_ids
    )

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        publisher_id = request.POST.get("publisher")

        publisher = None
        if publisher_id:
            publisher = get_object_or_404(Publisher, id=publisher_id)

        article = Article.objects.create(
            title=title,
            content=content,
            created_by=request.user,
            publisher=publisher
        )

        journalist_followers = Subscription.objects.filter(
            journalist=request.user
        )

        for sub in journalist_followers:
            Notification.objects.create(
                recipient=sub.reader,
                message=f"{request.user.username} uploaded a new article: {article.title}"
            )

        if publisher:
            publisher_followers = Subscription.objects.filter(
                publisher=publisher
            )

            for sub in publisher_followers:
                Notification.objects.create(
                    recipient=sub.reader,
                    message=f"New article under {publisher.name}: {article.title}"
                )

        return redirect("dashboard")

    return render(request, "news/create_article.html", {
        "publishers": publishers
    })


# ======================
# Update Article
# ======================
@login_required
def update_article(request, article_id):
    """
    Allow journalists (owners) and editors to update an article.
    """
    article = get_object_or_404(Article, id=article_id)

    if request.user.role not in ["journalist", "editor"]:
        return redirect("dashboard")

    if request.user.role == "journalist" and article.created_by != request.user:
        return redirect("dashboard")

    if request.method == "POST":
        form = ArticleUpdateForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully.")
            return redirect("dashboard")
    else:
        form = ArticleUpdateForm(instance=article)

    return render(request, "news/update_article.html", {"form": form})


# ======================
# Delete Article
# ======================
@login_required
def delete_article(request, article_id):
    """
    Allow journalists (owners) and editors to delete an article.
    """
    article = get_object_or_404(Article, id=article_id)

    if request.user.role not in ["journalist", "editor"]:
        return redirect("dashboard")

    if request.user.role == "journalist" and article.created_by != request.user:
        return redirect("dashboard")

    article.delete()
    messages.success(request, "Article deleted successfully.")
    return redirect("dashboard")


# ======================
# Approve Article (Editor)
# ======================
@login_required
def approve_article(request, article_id):
    """
    Allow editors to approve submitted articles.
    """
    if request.user.role != "editor":
        messages.error(request, "Only editors can approve articles.")
        return redirect("dashboard")

    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.save()

    messages.success(request, "Article approved successfully!")
    return redirect("dashboard")


# -----------------
# Create Newsletter
# -----------------
@login_required
def create_newsletter(request):
    """
    Allow journalists to create a newsletter
    linked to their assigned publisher.
    """
    if request.user.role != "journalist":
        return HttpResponseForbidden("Only journalists can create newsletters")

    form = NewsletterForm(request.POST or None)

    form.fields['publisher'].queryset = Publisher.objects.filter(
        id=request.user.publisher_profile_id
    )

    if form.is_valid():
        newsletter = form.save(commit=False)
        newsletter.author = request.user
        newsletter.publisher = request.user.publisher_profile
        newsletter.save()
        return redirect('dashboard')

    return render(request, 'newsletter/create.html', {'form': form})


@login_required
def approve_newsletter(request, pk):
    """
    Allow editors to approve newsletters
    and send email notifications to subscribers.
    """
    if request.user.role != "editor":
        return HttpResponseForbidden()

    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.approved = True
    newsletter.save()

    send_notification(newsletter)

    messages.success(request, "Newsletter approved and emails sent.")
    return redirect('dashboard')


# ======================
# Subscribe to Journalist
# ======================
@login_required
def subscribe_journalist(request, journalist_id):
    """
    Allow readers to subscribe to a journalist.
    Prevents duplicate subscriptions.
    """
    if request.user.role != "reader":
        messages.error(request, "Only readers can subscribe.")
        return redirect("dashboard")

    journalist = get_object_or_404(User, id=journalist_id, role="journalist")

    subscription, created = Subscription.objects.get_or_create(
        reader=request.user,
        journalist=journalist
    )

    if created:
        messages.success(request, "Subscribed successfully.")
    else:
        messages.info(request, "Already subscribed.")

    return redirect("dashboard")


@login_required
def unsubscribe_journalist(request, journalist_id):
    """
    Allow readers to unsubscribe from a journalist.
    """
    if request.user.role != "reader":
        messages.error(request, "Only readers can unsubscribe.")
        return redirect("dashboard")

    Subscription.objects.filter(
        reader=request.user,
        journalist_id=journalist_id
    ).delete()

    messages.success(request, "Unsubscribed successfully.")
    return redirect("dashboard")


# ======================
# Subscribe to Publisher
# ======================
@login_required
def subscribe_publisher(request, publisher_id):
    """
    Allow readers to subscribe to a publisher.
    Prevents duplicate subscriptions.
    """
    if request.user.role != "reader":
        messages.error(request, "Only readers can subscribe.")
        return redirect("dashboard")

    publisher = get_object_or_404(Publisher, id=publisher_id)

    subscription, created = Subscription.objects.get_or_create(
        reader=request.user,
        publisher=publisher
    )

    if created:
        messages.success(request, "Subscribed successfully.")
    else:
        messages.info(request, "Already subscribed.")

    return redirect("dashboard")


@login_required
def unsubscribe_publisher(request, publisher_id):
    """
    Allow readers to unsubscribe from a publisher.
    """
    if request.user.role != "reader":
        messages.error(request, "Only readers can unsubscribe.")
        return redirect("dashboard")

    Subscription.objects.filter(
        reader=request.user,
        publisher_id=publisher_id
    ).delete()

    messages.success(request, "Unsubscribed successfully.")
    return redirect("dashboard")


def send_notification(newsletter):
    """
    Send email notifications to all subscribers
    of the newsletter's publisher.
    """
    subscriptions = Subscription.objects.filter(
        publisher=newsletter.publisher
    )

    emails = [sub.reader.email for sub in subscriptions if sub.reader.email]

    if emails:
        send_mail(
            subject=f"New Newsletter: {newsletter.title}",
            message=newsletter.content,
            from_email="admin@news.com",
            recipient_list=emails,
            fail_silently=False,
        )


@login_required
def manage_publishers(request):
    """
    Allow editors to view and create publishers.
    """
    if request.user.role != "editor":
        return redirect("dashboard")

    publishers = Publisher.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Publisher.objects.create(
                name=name,
                owner=request.user
            )
            return redirect("manage_publishers")

    return render(request, "news/manage_publishers.html", {
        "publishers": publishers
    })
