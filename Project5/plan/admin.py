from django.contrib import admin
from .models import User, Schedule, todo_list, Note, Diary, Event

# Register your models here.

admin.site.register(User)
admin.site.register(Schedule)
admin.site.register(todo_list)
admin.site.register(Note)
admin.site.register(Diary)
admin.site.register(Event)
