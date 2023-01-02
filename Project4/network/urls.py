
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_post, name="new"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/follow/<int:user_id>", views.follow, name="follow"),
    path("following/<int:user_id>", views.following, name="following"),

    # API Routes
    path("post/<int:post_id>", views.post, name="post"),
    path("post/<int:post_id>/like", views.like, name="like"),
    path("post/<int:post_id>/unlike", views.unlike, name="unlike"),


]
