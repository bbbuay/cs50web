from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    img = models.ImageField(upload_to='images' ,blank=True)

    def __str__(self):
        return f"{self.id} : {self.name}"

class Auction(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    img = models.ImageField(upload_to='images' ,blank=True)
    start_bid = models.FloatField()
    current_bid = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="auctions", blank=True, default=1) 
    watch_users = models.ManyToManyField(User, blank=True, related_name="watchlist_auctions")
    #default 1 = "No Category Listed"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    is_active = models.BooleanField(default=True)
    # The UTC date and time
    date = models.DateField(auto_now=False, auto_now_add=True, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.id} : {self.name} owned by {self.user}"

class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    
    def __str__(self):
        return f"{self.user} bid ${self.bid} to {self.auction}"

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")

    def __str___(self):
        return f"{self.id} {self.user} : {self.comment}"


    