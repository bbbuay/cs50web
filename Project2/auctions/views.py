from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .models import User, Auction, Bid, Category, Comment
from django.db.models import Max
from django.contrib.auth.decorators import login_required


class CreateForm(forms.Form):
    # name, description, img, startbid(, user)
    name = forms.CharField(label="Name", max_length=64)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    img = forms.ImageField(label="Image", required=False)
    startbid = forms.FloatField(label="Starting Bid")

class CategoryForm(forms.Form):
    # name, img
    name = forms.CharField(label="Name", max_length=64)
    img = forms.ImageField(label="Image", required=False)

def index(request):
    return render(request, "auctions/index.html", {
        "auctions" : Auction.objects.all()
    })

@login_required
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            startbid = form.cleaned_data["startbid"]
            user_id =  request.POST["user_id"]
            user = User.objects.get(pk=user_id)
            category_id = request.POST["auc-category"]
            category = Category.objects.get(pk=category_id)
            if 'img' in request.FILES:
                img = request.FILES["img"]
                auction = Auction(name=name, description=description, img=img, start_bid=startbid, user=user, category=category)
            else :
                auction = Auction(name=name, description=description, start_bid=startbid, user=user, category=category)
            auction.save()
            return HttpResponseRedirect(reverse("index"))

            
    return render(request, "auctions/create.html", {
        "form": CreateForm(),
        "categories" : Category.objects.all()
    })

@login_required
def auction(request, auction_id):

    auction = Auction.objects.get(pk=auction_id)
    user = request.user

    if request.method == "POST":

        if "bid" in request.POST:
            user_bid = float(request.POST["bid"])
            max_bid = auction.bids.all().aggregate(Max('bid')) # {'bid__max': 35.0}
            #  max_bid['bid__max'] get output = 35.0
            #  if doesn't have any bids yet, max_bid['bid__max'] return "None"

            first_condition = (max_bid['bid__max'] is not None) and (user_bid > max_bid['bid__max'])
            second_condition = (max_bid['bid__max'] is None) and (user_bid > auction.start_bid)
            
            if first_condition or second_condition:
                auction.save()
                bid = Bid(bid=user_bid, auction=auction, user=user)
                bid.save()
                auction.current_bid = auction.bids.last().bid
                auction.save()
                HttpResponseRedirect(reverse("auction", args=(auction.id,)))
            else :
                if max_bid['bid__max'] is None:
                    message = f"Your bid must greater than {auction.start_bid} dollars."
                else : 
                    message = f"Your bid must greater than {max_bid['bid__max']} dollars."
                return render(request, "auctions/auction.html",{
                    "message" : message,
                    "auction": Auction.objects.get(pk=auction_id),
                    "bids": Auction.objects.get(pk=auction_id).bids.all()
                })

        elif "comment" in request.POST :
            user_comment = request.POST["comment"]
            comment = Comment(comment=user_comment, auction=auction, user=user)
            comment.save()
            HttpResponseRedirect(reverse("auction", args=(auction.id,)))  
    
    if auction.is_active == False:
        return render(request, "auctions/auction.html", {
        "auction": auction,
        "bids": auction.bids.all(),
        "comments" : auction.comments.all(),
        "user_watchlists" : user.watchlist_auctions.all(),
        "lastest_bid": auction.bids.last()
    })
      
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "bids": auction.bids.all(),
        "comments" : auction.comments.all(),
        "user_watchlists" : user.watchlist_auctions.all()
    })

def add(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    user = request.user
    if request.method == "POST": 
        auction.watch_users.add(user)
        return redirect("auction", auction_id=auction_id)

def remove(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    user = request.user
    if request.method == "POST": 
        auction.watch_users.remove(user)
        return redirect("auction", auction_id=auction_id)

def close(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    user = request.user
    created_user = auction.user
    if request.method == "POST" and user == created_user:
        auction.is_active = False
        auction.save()
        return redirect("auction", auction_id=auction_id)

@login_required
def watch(request):
    user = request.user
    watch_auctions = user.watchlist_auctions.all()
    return render(request, "auctions/watch.html",{
        "watch_auctions": watch_auctions
    })

def categories(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            
            if 'img' in request.FILES:
                img = request.FILES["img"]
                category = Category(name=name, img=img)
            else :
                category = Category(name=name)
            category.save()
            return HttpResponseRedirect(reverse("categories"))

    return render(request, "auctions/categories.html",{
        "form" : CategoryForm(),
        "categories" : Category.objects.all()
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    auctions = category.auctions.all()
    return render(request, "auctions/category.html",{
        "category": category,
        "auctions" : auctions
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
