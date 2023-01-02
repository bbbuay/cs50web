from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    pass

class Schedule(models.Model):
    '''
    contain each schedule of all user
    '''
    name = models.TextField(max_length=64)
    date = models.DateField(auto_now=False, auto_now_add=False)
    start_hours = models.CharField(max_length=2)
    end_hours = models.CharField(max_length=2)
    start_mins = models.CharField(max_length=2)
    end_mins = models.CharField(max_length=2)
    bg_hex_color = models.CharField(max_length=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedule")

    def __str__(self):
        return f"{self.id} {self.user} at {self.date} : {self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "start_hours": self.start_hours,
            "end_hours": self.end_hours,
            "start_mins": self.start_mins,
            "end_mins": self.end_mins,
            "bg_hex_color": self.bg_hex_color,
            "user": [user.username for user in self.user.all()],
        }

class todo_list(models.Model):
    '''
    contain each todo list of all user 
    '''
    name = models.TextField(max_length=64)
    date = models.DateField(auto_now=False, auto_now_add=False)
    is_toppriorities = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_list")

    def __str__(self):
        return f"{self.id} {self.user} at {self.date} : {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "is_toppriorities" : self.is_toppriorities,
            "is_done": self.is_done,
        }

class Note(models.Model):
    '''
    Contain each planner note of all user
    '''
    content = models.TextField(max_length=512)
    date = models.DateField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note")

    def __str__(self):
        return f"{self.id} {self.user}: {self.content}"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "date": self.date,
        }

class Diary(models.Model):
    '''
    Contain all user diary 
    '''
    title = models.TextField(max_length=128)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    mood = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diary")

    def __str__(self):
        return f"{self.id} {self.user}: {self.title} at {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "content": self.content,
            "image": self.image,
            "mood": self.mood,
        }


class Event(models.Model):
    '''
    Contain all events
    '''
    name = models.CharField(max_length=128)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    
    def __str__(self):
        return f"{self.name} : on {self.date} from {self.start_time} to {self.end_time}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "start_time": self.start_time.strftime('%H:%M'),
            "end_time": self.end_time.strftime('%H:%M'),
        }
