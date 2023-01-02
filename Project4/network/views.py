from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User,Post

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

# Import Pagination
from django.core.paginator import Paginator

def index(request):
    user = request.user
    posts = Post.objects.order_by("-timestamp").all()

    # # create dict of (post_id, like_users)
    # post_like_user_dict = dict()

    # for post in posts:
    #     post_id = post.id
    #     like_users = post.like_users.all()
    #     # like_number = post.like_users.all().count
    #     post_like_user_dict[post_id] = like_users

    # Paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{
        "posts" : Post.objects.order_by("-timestamp").all(),
        "register_user" : user,
        "page_obj": page_obj,
        # "post_like_user_dict" : post_like_user_dict
    })

@login_required
def new_post(request):
    if request.method == "POST":
        user = request.user
        post_content = request.POST["post_content"]
        new_post = Post(content=post_content, user=user)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))
        
    return render(request, "network/new.html")

def profile(request, user_id):

    user = request.user
    profile_user = User.objects.get(pk=user_id)
    followings_by_user = user.following.all()
    user_posts = profile_user.created_post.order_by("-timestamp").all()

    if request.method == "POST" :
        # if user press follow, then add user to profile_user follower list
        if "follow" in request.POST:
            profile_user.follower.add(user)
            return HttpResponseRedirect(reverse("profile", args=(profile_user.id,)))
        # if user press unfollow, then remove user to profile_user follower list
        elif "unfollow" in request.POST:
            profile_user.follower.remove(user)
            return HttpResponseRedirect(reverse("profile", args=(profile_user.id,)))

    # Paginator
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html",{
        "profile_user" : profile_user,
        "posts" : profile_user.created_post.order_by("-timestamp").all(),
        "post_number": profile_user.created_post.all().count(),
        "follower_number" : profile_user.follower.all().count(),
        "following_number" : profile_user.following.all().count(),
        "is_followed_by_user": profile_user in followings_by_user,
        "page_obj": page_obj
    })

@login_required
def follow(request, user_id):
    user = request.user
    profile_user = User.objects.get(pk=user_id)
    profile_followers = profile_user.follower.all()
    profile_followings = profile_user.following.all()

    followings_user = user.following.all()

    followings_user_id = [object.id for object in followings_user]
    following_user_username_list = [object.username for object in followings_user]

    if request.method == "POST":
        user_id = request.POST["user_id"]
        form_user = User.objects.get(pk=user_id)
        if "follow" in request.POST:
            # follow form_user
            user.following.add(form_user)
            return HttpResponseRedirect(reverse("follow", args=(user.id,)))
        elif "unfollow" in request.POST:
            # unfollow form_user
            user.following.remove(form_user)
            return HttpResponseRedirect(reverse("follow", args=(user.id,)))


    return render(request, "network/follow.html",{
        "profile_user" : profile_user,
        "profile_followers" : profile_followers,
        "profile_followings" : profile_followings,
        "profile_follower_number" : profile_followers.count(),
        "profile_following_number" : profile_followings.count(),
        "non_followings_user" : User.objects.exclude(id__in=followings_user_id),
        "following_user_usernames" : following_user_username_list,
    })
    
@login_required
def following(request, user_id):

    user = request.user
    user_followings = user.following.all()
    post_of_user_following = Post.objects.filter(user__in = user_followings)

    # Paginator
    paginator = Paginator(post_of_user_following, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html",{
        "posts": Post.objects.all(),
        "page_obj": page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
@csrf_exempt
def post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "post not found."}, status=404)
    
    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether post content is change
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    
    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    post.like_users.add(user)
    like_numbers = post.like_users.all().count()
    post.like_numbers = like_numbers
    post.save()
    return JsonResponse({"message": "Post successfully like."}, status=200)   

@login_required
def unlike(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    post.like_users.remove(user)
    like_numbers = post.like_users.all().count()
    post.like_numbers = like_numbers
    post.save()
    return JsonResponse({"message": "Post successfully unliked."}, status=200) 


