from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import ArticleForm, ArticleUpdateForm, CustomUserCreationForm
from .models import Article, Publisher, User, Subscription


# ======================
# Home
# ======================
def home(request):
    return render(request, "news/home.html")


# ======================
# Register (redirects to login)
# ======================
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "news/register.html", {"form": form})


# ======================
# Login
# ======================
def login_view(request):
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
def logout_view(request):
    logout(request)
    return redirect("home")


# ======================
# Dashboard (ROLE-BASED)
# ======================
@login_required
def dashboard(request):
    role = request.user.role

    if role == "reader":
        articles = Article.objects.filter(approved=True)

        # 🔥 Add subscription tracking
        subscriptions = Subscription.objects.filter(reader=request.user)

        subscribed_journalists = subscriptions.values_list(
            "journalist_id", flat=True
        )

        subscribed_publishers = subscriptions.values_list(
            "publisher_id", flat=True
        )

    elif role == "journalist":
        articles = Article.objects.filter(created_by=request.user)
        subscribed_journalists = []
        subscribed_publishers = []

    elif role == "editor":
        articles = Article.objects.filter(approved=False)
        subscribed_journalists = []
        subscribed_publishers = []

    else:
        articles = Article.objects.none()
        subscribed_journalists = []
        subscribed_publishers = []

    return render(request, "news/dashboard.html", {
        "role": role,
        "articles": articles,
        "subscribed_journalists": subscribed_journalists,
        "subscribed_publishers": subscribed_publishers,
    })


# ------------------
# Read_Artivle
# ------------------
@login_required
def read_article(request, article_id):
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

    if request.user.role != "journalist":
        messages.error(request, "Only journalists can create articles.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user
            article.approved = False
            article.save()

            messages.success(
                request,
                "Article created successfully! Waiting for editor approval."
            )
            return redirect("dashboard")
    else:
        form = ArticleForm()

    return render(request, "news/create_article.html", {"form": form})


# ======================
# Update Article
# ======================
@login_required
def update_article(request, article_id):
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

    if request.user.role != "editor":
        messages.error(request, "Only editors can approve articles.")
        return redirect("dashboard")

    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.save()

    messages.success(request, "Article approved successfully!")
    return redirect("dashboard")


# ======================
# Subscribe to Journalist
# ======================
@login_required
def subscribe_journalist(request, journalist_id):
    if request.user.role != "reader":
        messages.error(request, "Only readers can subscribe.")
        return redirect("dashboard")

    journalist = get_object_or_404(User, id=journalist_id, role="journalist")

    # Prevent duplicate subscription
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
    if request.user.role != "reader":
        messages.error(request, "Only readers can unsubscribe.")
        return redirect("dashboard")

    Subscription.objects.filter(
        reader=request.user,
        publisher_id=publisher_id
    ).delete()

    messages.success(request, "Unsubscribed successfully.")
    return redirect("dashboard")
