from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("listing/<int:id>" , views.listing , name = "listing"),
    path("watchlist/<int:id>" , views.watchlist , name = "watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist_view"),
    path("comment/<int:id>", views.add_comment, name="comment"),
    path("close/<int:id>", views.close_listing, name="close_listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.category_page, name="category_page"),
    path("create", views.create_listing, name="create_listing"),
]
