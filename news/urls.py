from django.urls import path
from .views import dashboard, register, create_article, approve_article, delete_article
from .api_views import ReaderArticlesAPI
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'), 
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('subscribe/<int:article_id>/', views.subscribe_article, name='subscribe_article'),
    path('create/', create_article, name='create_article'),
    path('approve/<int:article_id>/', approve_article),
    path('delete/<int:article_id>/', delete_article),
    path('api/articles/', ReaderArticlesAPI.as_view()),
]
