from django.urls import path

from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("planner", views.planner, name="planner"),
    path("diary", views.diary, name="diary"),
    path("add_schedule", views.add_new_schedule, name="add_schedule"),
    path("add_todo", views.add_todo, name="add_todo"),
    path("add_note", views.add_note, name="add_note"),
    path("all_diaries", views.all_diaries, name="all_diaries"),
    path("remove_event/<int:event_id>", views.remove_event, name="remove_event"),
    path("delete_diary/<int:diary_id>", views.delete_diary, name="delete_diary"),

    # API Routes
    path("schedule/<int:schedule_id>", views.schedule, name="schedule"),
    path("todo/<int:todo_id>", views.todo, name="todo"),
    path("note/<int:note_id>", views.note, name="note"),
    path("event/<int:event_id>", views.event, name="note"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)