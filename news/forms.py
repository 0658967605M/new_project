"""
Forms module for the News application.

This module defines Django forms used for creating and updating
articles, registering users, and managing newsletters.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Article, Newsletter
from django.contrib.auth.models import User

User = get_user_model()


class ArticleForm(forms.ModelForm):
    """
    Form for creating a new Article.

    Used by journalists to submit articles for publication.
    """

    class Meta:
        """
        Metadata for ArticleForm.

        Specifies the associated model, included fields,
        and custom Bootstrap widgets.
        """
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ArticleUpdateForm(forms.ModelForm):
    """
    Form for updating an existing Article.

    Used by editors or publishers to modify article content
    and approve articles before publication.
    """

    class Meta:
        """
        Metadata for ArticleUpdateForm.

        Includes title, content, and approval status.
        """
        model = Article
        fields = ['title', 'content', 'approved']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form.

    Extends Django's built-in UserCreationForm by adding:
    - Email field
    - Role selection (reader, journalist, editor)
    """

    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        """
        Metadata for CustomUserCreationForm.

        Defines the user model and fields required
        during registration.
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        """
        Validate that the email address is unique.

        Raises:
            ValidationError: If the email is already registered.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email


class NewsletterForm(forms.ModelForm):
    """
    Form for creating and managing newsletters.

    Used by editors to send newsletter content
    to subscribed users.
    """

    class Meta:
        """
        Metadata for NewsletterForm.

        Defines the associated model and included fields.
        """
        model = Newsletter
        fields = ['title', 'content']
