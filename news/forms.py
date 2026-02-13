from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Article

User = get_user_model()


# ----------------------------
# Article Form (Create / Publisher)
# ----------------------------
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


# ----------------------------
# Article Update Form (Editor/Publisher)
# ----------------------------
class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'approved']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ----------------------------
# User Registration Form
# ----------------------------
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('journalist', 'Journalist'),
        ('editor', 'Editor'),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, widget=forms.Select(
            attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
