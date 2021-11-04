from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("view_listing/<int:id>", views.view_listing, name="view_listing"),
    path("watchlist_action/<int:id>", views.watchlist_action, name="watchlist_action"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category")
]
