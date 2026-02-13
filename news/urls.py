from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Articles
    path("read/<int:article_id>/", views.read_article, name="read_article"),
    path("create/", views.create_article, name="create_article"),
    path(
        "update/<int:article_id>/", views.update_article,
        name="update_article"
        ),
    path(
        "delete/<int:article_id>/", views.delete_article,
        name="delete_article"
        ),
    path(
        "approve/<int:article_id>/", views.approve_article,
        name="approve_article"
        ),
    path("subscribe/journalist/<int:journalist_id>/",
         views.subscribe_journalist, name="subscribe_journalist"),
    path("subscribe/publisher/<int:publisher_id>/",
         views.subscribe_publisher, name="subscribe_publisher"),
    path("unsubscribe/journalist/<int:journalist_id>/",
         views.unsubscribe_journalist, name="unsubscribe_journalist"),
    path("unsubscribe/publisher/<int:publisher_id>/",
         views.unsubscribe_publisher, name="unsubscribe_publisher"),

]
