from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import User, Schedule, todo_list, Note, Diary, Event
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
import json
from django import forms
from django.core.paginator import Paginator
from django.shortcuts import redirect

from datetime import datetime, timedelta
from django.utils import timezone

class DiaryForm(forms.Form):
    # define form fields (title, image, content, mood)
    title = forms.CharField(max_length=255,required=True, error_messages={'required': 'Please enter your title of the day.'})
    image = forms.ImageField(required=False, label="Image(optional)")
    content = forms.CharField(widget=forms.Textarea, required=True, error_messages={'required': 'Please enter your diary content.'})
    mood = forms.ChoiceField(choices=[
    ('&#128512;', 'Happy'), 
    ('&#128532;', 'Sad'), 
    ('&#128548;', 'Angry'), 
    ('&#128522;', 'Relaxed'), 
    ('&#128560;', 'Anxious'), 
    ('&#129321;', 'Excited'), 
    ('&#128528;', 'Bored'), 
    ('&#128555;', 'Tired')],
    required=True, error_messages={'required': 'Please enter your today mood.'})


moods = {
    "happy": "&#128512;",
    "sad": "&#128532;",
    "angry": "&#128548;",
    "relaxed": "&#128522;",
    "anxious": "&#128560;",
    "excited": "&#129321;",
    "bored": "&#128528;",
    "tired": "&#128555;",
}

inverse_moods = {v:k for k, v in moods.items()}


# Create your views here.

def index(request):
    timezone.activate('Asia/Bangkok')

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        user = request.user
        today = date.today().strftime("%Y-%m-%d")
        now = datetime.now() 
        now_date = now.strftime("%Y-%m-%d")

        current_date_header = datetime.now().strftime("%A, %B %d, %Y") 

        #  Get all upcoming events
        events = Event.objects.filter(date__gte=now_date ,user=user).order_by('date')
        # weekly_schedules = Schedule.objects.filter(user=user, date__gte=now_date, date__lte=now_date+7).order_by('date')

        # all schedule in next 7 days from current date
        start_date = timezone.now()
        end_date = start_date + timezone.timedelta(days=7)
        weekly_schedules = Schedule.objects.filter(user=user, date__range=(start_date, end_date)).order_by('date', 'start_hours', 'start_mins')

        # create a dictionary (python) that key: each day
        # create a list of each object ()
        objects_dict = {}
        # value_list = [] this will contain dict of each object in side of that day of week
            # [{object1}, {object2}, ..., {objectn}]
        
        for schedule in weekly_schedules:
            day_of_week = schedule.date.strftime('%A') # Output: Tuesday
            # if this key is already created
            if day_of_week in objects_dict: 
                # get value of key 
                previous_list = objects_dict[day_of_week]
                # create new value dicts to append in value list 
                new_dict = {
                    'name': schedule.name,
                    'date': schedule.date,
                    'start_hours': schedule.start_hours,
                    'start_mins': schedule.start_mins,
                    'end_hours': schedule.end_hours,
                    'end_mins':schedule.end_mins,
                    'bg_hex_color': schedule.bg_hex_color
                }
                # append another object dict and change the value of key 
                objects_dict[day_of_week] = previous_list + [new_dict]
            else:
                value_list = [{
                    'name': schedule.name,
                    'date': schedule.date,
                    'start_hours': schedule.start_hours,
                    'start_mins': schedule.start_mins,
                    'end_hours': schedule.end_hours,
                    'end_mins':schedule.end_mins,
                    'bg_hex_color': schedule.bg_hex_color
                }]
                objects_dict[day_of_week] = value_list

        # output 
        # {'day_of_week': [{
            # 'date': 'schedule date',
            # 'name': 'schedule_name',
            # 'start_hours': '08',
            # 'start_mins':'30',
            # 'end_hours': '09',
            # 'end_mins':'30',
            # 'bg_hex_color': '#111111'
        # },{},...,{}] , 
        # 'day_of_week(current_date + 1day)': [{},{}. . . ], . . .}

        # find the rest day that was not planned
        day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if objects_dict != {}:
            current_day_of_week = list(objects_dict.keys())[0]
            number_of_planned_day = len(objects_dict)
            number_of_unplanned_day = 7 - number_of_planned_day
            index_current_day = day_of_week.index(current_day_of_week)  #Example Output: 2
            # get rest unplanned day with order
            rest_day = []
            n = index_current_day + number_of_planned_day
            for i in range(number_of_unplanned_day):
                next_day = day_of_week[(n)%7]
                rest_day += [next_day]
                n+=1
        else:
            number_of_unplanned_day=7
            rest_day = day_of_week


        if request.method == "POST":
            event_name = request.POST["event-name"]
            event_date = request.POST["event-date"]
            start_time = request.POST["start-time"]
            end_time = request.POST["end-time"]

            # Check if end time is later than start time
            if end_time > start_time :
                 # Create new event and save it
                new_event = Event(name=event_name, date=event_date, start_time=start_time, end_time= end_time, user=user)
                new_event.save()
                return redirect('index')
            else: 
                # Return error message or take some other appropriate action
                error_message =  'The end time of the event <strong>must be later than</strong> the start time.'
                return render(request, "plan/index.html",{
                    'today': today,
                    'events': events,
                    'error_message': error_message,
                    'date_header': current_date_header,
                    'weekly_schedules_dict': objects_dict,
                    'number_of_unplanned_day': number_of_unplanned_day,
                    'rest_day': rest_day,
                })

        return render(request, "plan/index.html",{
            'today': today,
            'events': events,
            'date_header': current_date_header,
            'weekly_schedules_dict': objects_dict,
            'number_of_unplanned_day': number_of_unplanned_day,
            'rest_day': rest_day,
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required
def event(request, event_id):
    # Query for requested event
    try:
        event = Event.objects.get(user=request.user, pk=event_id)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found."}, status=404)

    # Return event contents
    if request.method == "GET":
        return JsonResponse(event.serialize())

    # Update whether schedule is updated
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("event_name") is not None:
            event.name = data["event_name"]
        if data.get("date") is not None:
            event.date = data["date"]
        if data.get("start_time") is not None:
            event.start_time = data["start_time"]
        if data.get("end_time") is not None:
            event.end_time = data["end_time"]
        event.save()
        return HttpResponse(status=204)
    
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def remove_event(request, event_id):
    if request.method == "POST":
        event = Event.objects.get(pk=event_id)
        event.delete()
        return redirect('index')

@login_required
def planner(request):

    user = request.user

    if request.method == "POST":
        if 'date-search' in request.POST:
            # get value from form
            date_search = request.POST['date-search']

            # Convert to readable form
            # Parse the date string
            date_string = datetime.strptime(date_search, '%Y-%m-%d')
            # Convert the date to a new format
            date_search_header = date_string.strftime('%b %d, %Y')
        elif 'pre-day' in request.POST:
            selected_date = request.POST.get('date_from_f1')
            previous_day = datetime.strptime(selected_date, '%Y-%m-%d') - timedelta(days=1)#one_day_before
            # Format the previous day as a string in the '%Y-%m-%d' format
            date_search = previous_day.strftime('%Y-%m-%d')

            date_search_header = previous_day.strftime('%b %d, %Y')

        elif 'today' in request.POST:
            return redirect('planner')
        elif 'next-day' in request.POST:
            selected_date = request.POST.get('date_from_f1')
            next_day = datetime.strptime(selected_date, '%Y-%m-%d') + timedelta(days=1)#one_day_before
            # Format the next day as a string in the '%Y-%m-%d' format
            date_search = next_day.strftime('%Y-%m-%d')

            date_search_header = next_day.strftime('%b %d, %Y')
      
    elif request.method == "GET":
        date_search_header = date.today() # today
        date_search = date.today().strftime("%Y-%m-%d")

    # get user schedule in selected date
    schedules = Schedule.objects.filter(user=user, date=date_search).order_by('start_hours', 'start_mins','end_hours', 'end_mins')

    # get todo list without top priorities
    todo_lists = todo_list.objects.filter(user=user, date=date_search).exclude(is_toppriorities=True)

    # get top priorities from todo lists
    top_priorities = todo_list.objects.filter(user=user, date=date_search, is_toppriorities=True)

    # get user note
    note = Note.objects.filter(user=user, date=date_search).first()

    return render(request, "plan/planner.html",{
        "date": date_search,
        "date_header": date_search_header,
        "schedule_lists" : schedules,
        "todo_lists": todo_lists,
        "top_priorities" : top_priorities,
        "note" : note,
    })

@login_required
def add_new_schedule(request):
    user = request.user

    if request.method == "POST":
        # Get the form data
        name = request.POST['schedule_name']
        start_hours = request.POST['start-hours']
        start_mins = request.POST['start-mins']
        end_hours = request.POST['end-hours']
        end_mins = request.POST['end-mins']
        bg_hex_color = request.POST['color']
        date_selected = request.POST['date-selected']

        # create new schedule
        new_schedule = Schedule(name=name, date=date_selected, start_hours=start_hours, end_hours=end_hours, start_mins=start_mins, end_mins=end_mins, bg_hex_color=bg_hex_color, user=user)
        new_schedule.save()

        return HttpResponseRedirect(reverse("planner"))

@login_required
def add_todo(request):
    user = request.user

    if request.method == "POST":
        # Get the form data
        todo_name = request.POST['todo-task']
        todo_date = request.POST['todo-date']
        is_toppriorities = bool(request.POST.get('is-top-priorities'))

        # create new todo list
        new_todo = todo_list(name=todo_name, date=todo_date,is_toppriorities=is_toppriorities, user=user)
        new_todo.save()

        return HttpResponseRedirect(reverse("planner"))

@login_required
def add_note(request):
    user = request.user

    if request.method == 'POST':
        #  Get data from form
        note_content = request.POST['note_content']
        date = request.POST['note-date']

        # Create Note
        note = Note(content=note_content, date=date, user=user)
        note.save()

        return HttpResponseRedirect(reverse("planner"))

@login_required
def schedule(request, schedule_id):

    # Query for requested schedule
    try:
        schedule = Schedule.objects.get(user=request.user, pk=schedule_id)
    except Schedule.DoesNotExist:
        return JsonResponse({"error": "Schedule not found."}, status=404)

    # Return schedule contents
    if request.method == "GET":
        return JsonResponse(schedule.serialize())
    
    # Update whether schedule is updated
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("schedule_name") is not None:
            schedule.name = data["schedule_name"]
        if data.get("date") is not None:
            schedule.date = data["date"]
        if data.get("start_hours") is not None:
            schedule.start_hours = data["start_hours"]
        if data.get("end_hours") is not None:
            schedule.end_hours = data["end_hours"]
        if data.get("start_mins") is not None:
            schedule.start_mins = data["start_mins"]
        if data.get("end_mins") is not None:
            schedule.end_mins = data["end_mins"]
        if data.get("bg_hex_color") is not None:
            schedule.bg_hex_color = data["bg_hex_color"]
        schedule.save()
        return HttpResponse(status=204)
    
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def todo(request, todo_id):
    # Query for requested todo task
    try:
        todo = todo_list.objects.get(user=request.user, pk=todo_id)
    except todo_list.DoesNotExist:
        return JsonResponse({"error": "Todo task not found."}, status=404)

    # Return todo contents
    if request.method == "GET":
        return JsonResponse(todo.serialize())
    
    # Update whether todo is updated
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("todo_name") is not None:
            todo.name = data["todo_name"]
        if data.get("date") is not None:
            todo.date = data["date"]
        if data.get("is_toppriorities") is not None:
            todo.is_toppriorities = data["is_toppriorities"]
        if data.get("is_done") is not None:
            todo.is_done = data["is_done"]
        todo.save()
        return HttpResponse(status=204)
    
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def note(request, note_id):
    # Query for requested note
    try:
        note = Note.objects.get(user=request.user, pk=note_id)
    except Note.DoesNotExist:
        return JsonResponse({"error": "Note is not found."}, status=404)

    # Return note
    if request.method == "GET":
        return JsonResponse(note.serialize())
    
    # Update whether note is updated
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("note_content") is not None:
            note.content = data["note_content"]
        if data.get("date") is not None:
            note.date = data["date"]
        note.save()
        return HttpResponse(status=204)
    
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def diary(request):

    user = request.user

    if request.method == 'POST':
        # handle form submission
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            # extract the data from the form
            title = form.cleaned_data['title']
            image = form.cleaned_data['image']
            content = form.cleaned_data['content']
            mood = form.cleaned_data['mood']

            # save the form data to the database
            if image :
                new_diary = Diary(title=title, content=content, image=image, mood=mood, user=user)
            else :
                new_diary = Diary(title=title, content=content, mood=mood, user=user)
            new_diary.save()

            # redirect to diary page
            return HttpResponseRedirect(reverse("diary"))
            
    else:
        # For Creating Diary
        # create an empty form
        form = DiaryForm()
        today_header = date.today() # today

        # For show overview of last 5 day
        # get the last 5 diaries of user to display
        last_diaries = Diary.objects.filter(user=user).order_by('-timestamp')[:5]
        # This is for the case if there are no enough diar
        last_diaries_number = last_diaries.count()
    
    return render(request, "plan/diary.html", {
        'form': form,
        'date_header': today_header,
        'last_diaries': last_diaries,
        'last_diaries_number' : last_diaries_number,       
    })

@login_required
def delete_diary(request, diary_id):
    if request.method == "POST":
        diary = Diary.objects.get(pk=diary_id)
        diary.delete()
        return redirect('all_diaries')

@login_required
def all_diaries(request):

    if request.method == "POST":
        # In this case, it will search by date 
        if 'date-search' in request.POST:
            date_search = request.POST["date-search"]
            diaries = Diary.objects.filter(user=request.user,timestamp__date=date_search).order_by('-timestamp')
            diary_header = f"Diary was writen by {date_search}"
        # In this case, it will search by mood
        elif 'mood-select' in request.POST:
            mood_number = request.POST['mood-select']
            mood_select = f"&#{mood_number};"
            diaries = Diary.objects.filter(user=request.user, mood=mood_select).order_by('-timestamp')
            mood_word = inverse_moods[mood_select]
            diary_header = f"The diary entries are being sorted by {mood_word} mood."
    else:
        # For show all diaries
        diaries = Diary.objects.filter(user=request.user).order_by('-timestamp')
        diary_header = "All Diaries"
    
    # Paginator
    paginator = Paginator(diaries, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_pages = page_obj.paginator.num_pages
    page_range = range(1, num_pages + 1)

    return render(request, "plan/all_diaries.html",{
        'page_obj': page_obj,
        'page_range': page_range,
        'diary_header': diary_header
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
            return render(request, "plan/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "plan/login.html")

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
            return render(request, "plan/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "plan/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "plan/register.html")