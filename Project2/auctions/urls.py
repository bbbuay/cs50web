from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watch", views.watch, name="watch"),
    path("categories", views.categories, name="categories"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("category/<int:category_id>", views.category, name="category"),
    path("auction/<int:auction_id>/add", views.add, name="add"),
    path("auction/<int:auction_id>/remove", views.remove, name="remove"),
    path("auction/<int:auction_id>/close", views.close, name="close")
]
