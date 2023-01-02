from django.contrib import admin
from .models import Auction, Bid, Comment, Category

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "start_bid", "current_bid", "user", "is_active", "date", "time")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid", "auction", "user")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "auction", "user")


# Register your models here.
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)