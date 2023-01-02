from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follower = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="following")

    def __str__(self):
        return f"{self.id} {self.username}"

class Post(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    # link to number of like by counting this
    like_numbers = models.IntegerField(default=0)
    like_users = models.ManyToManyField(User, blank=True, related_name="liked_post")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_post")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "like_numbers" : self.like_users.count(),
            "like_users" : [user.usename for user in self.like_users.all()],
            "user" : self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

    def __str__(self):
        return f"{self.id} {self.user}: {self.content}"


