from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import ArticleForm, ArticleUpdateForm, CustomUserCreationForm
from .models import Article, User


# ----------------------------
# Home Page
# ----------------------------
def home(request):
    return render(request, 'news/home.html')


# ----------------------------
# User Registration
# ----------------------------
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()          # create user
            login(request, user)        # log user in
            return redirect("dashboard")

    else:
        form = CustomUserCreationForm()

    return render(request, "news/register.html", {"form": form})


# ----------------------------
# Dashboard
# ----------------------------
@login_required
def dashboard(request):
    role = request.user.role
    articles = Article.objects.all()

    # Publisher sees only their articles
    if role == 'publisher':
        articles = articles.filter(created_by=request.user)
    # Editor sees all pending approval articles
    elif role == 'editor':
        articles = articles.filter(approved=False)
    # Reader sees all approved articles
    elif role == 'reader':
        articles = articles.filter(approved=True)

    return render(request, 'news/dashboard.html', {'role': role, 'articles': articles})


# ----------------------------
# Create Article (Publisher)
# ----------------------------
@login_required
def create_article(request):
    if request.user.role != 'publisher':
        messages.error(request, "Only publishers can create articles.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user
            article.save()
            messages.success(request, "Article created successfully!")
            return redirect('dashboard')
    else:
        form = ArticleForm()
    return render(request, 'news/create_article.html', {'form': form})


# ----------------------------
# Update Article (Publisher/Editor)
# ----------------------------
@login_required
def update_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # Only publisher who created or editor can update
    if request.user.role == 'publisher' and article.created_by != request.user:
        messages.error(request, "You cannot edit this article.")
        return redirect('dashboard')
    if request.user.role not in ['publisher', 'editor']:
        messages.error(request, "You cannot edit this article.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ArticleUpdateForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('dashboard')
    else:
        form = ArticleUpdateForm(instance=article)

    return render(request, 'news/update_article.html', {'form': form, 'article': article})


# ----------------------------
# Delete Article (Publisher/Editor)
# ----------------------------
@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # Only publisher who created or editor can delete
    if request.user.role == 'publisher' and article.created_by != request.user:
        messages.error(request, "You cannot delete this article.")
        return redirect('dashboard')
    if request.user.role not in ['publisher', 'editor']:
        messages.error(request, "You cannot delete this article.")
        return redirect('dashboard')

    article.delete()
    messages.success(request, "Article deleted successfully!")
    return redirect('dashboard')


# ----------------------------
# Approve Article (Editor)
# ----------------------------
@login_required
def approve_article(request, article_id):
    if request.user.role != 'editor':
        messages.error(request, "Only editors can approve articles.")
        return redirect('dashboard')

    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.save()
    messages.success(request, "Article approved successfully!")
    return redirect('dashboard')


# ----------------------------
# Subscribe to Author (Reader)
# ----------------------------
@login_required
def subscribe_article(request, article_id):
    if request.user.role != 'reader':
        messages.error(request, "Only readers can subscribe to authors.")
        return redirect('dashboard')

    article = get_object_or_404(Article, id=article_id)
    if not hasattr(request.user, 'subscriptions') or request.user.subscriptions is None:
        request.user.subscriptions = []
    if article.created_by.id not in request.user.subscriptions:
        request.user.subscriptions.append(article.created_by.id)
        request.user.save()
        messages.success(request, f"Subscribed to {article.created_by.username}")
    else:
        messages.info(request, "Already subscribed to this author.")

    return redirect('dashboard')
