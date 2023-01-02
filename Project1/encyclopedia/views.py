from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util
from random import choice
from markdown2 import Markdown

markdowner = Markdown()

def index(request):

    # Check if method is POST
    if request.method == "POST":  
        # # # Check if get a query from user # # #
        if 'q' in request.POST:
            search_query = request.POST["q"]
            # list of all entries 
            entries_list = util.list_entries()
            print(search_query)
            print(entries_list)

            if search_query in entries_list:
                return HttpResponseRedirect(f"{search_query}")
            else :
                # find search query as a substring of all entries list
                sub_entry_list = []
                for entry in entries_list:
                    # check if there are any substring in each entry
                    if search_query in entry:
                        sub_entry_list.append(entry)
                print(sub_entry_list)
                return render(request, "encyclopedia/search.html", {
                    "sub_entry_list": sub_entry_list
                })
        # # # End of check if get a query from user # # #

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry Page 
def entry_page(request, title):

    # Check if method is POST
    if request.method == "POST":  
        # # # Check if get a query from user # # #
        if 'q' in request.POST:
            search_query = request.POST["q"]
            # list of all entries 
            entries_list = util.list_entries()
            print(search_query)
            print(entries_list)

            if search_query in entries_list:
                return HttpResponseRedirect(f"{search_query}")
            else :
                # find search query as a substring of all entries list
                sub_entry_list = []
                for entry in entries_list:
                    # check if there are any substring in each entry
                    if search_query in entry:
                        sub_entry_list.append(entry)
                print(sub_entry_list)
                return render(request, "encyclopedia/search.html", {
                    "sub_entry_list": sub_entry_list
                })
        # # # End of check if get a query from user # # #
    if util.get_entry(title) is not None:
        print(markdowner.convert(util.get_entry(title)))
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(title)),
            "title": title,
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": "<h3>This Page was not found.</h3>",
            "title": title,
        })

# Edit Page 
def edit_page(request, title):
 
    # Check if method is POST
    if request.method == "POST":  
        # # # Check if get a query from user # # #
        if 'q' in request.POST:
            search_query = request.POST["q"]
            # list of all entries 
            entries_list = util.list_entries()
            print(search_query)
            print(entries_list)

            if search_query in entries_list:
                return HttpResponseRedirect(f"{search_query}")
            else :
                # find search query as a substring of all entries list
                sub_entry_list = []
                for entry in entries_list:
                    # check if there are any substring in each entry
                    if search_query in entry:
                        sub_entry_list.append(entry)
                print(sub_entry_list)
                return render(request, "encyclopedia/search.html", {
                    "sub_entry_list": sub_entry_list
                })
        # # # End of check if get a query from user # # #
        
        elif "content_entry" in request.POST:
            # get content entry in textarea
            content_entry = request.POST["content_entry"]
            util.save_entry(title, content_entry)
            return HttpResponseRedirect(f"../{title}")

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": util.get_entry(title)
    })


# New Page 
def new_page(request):
    # Check if method is POST
    if request.method == "POST":  
        # # # Check if get a query from user # # #
        if 'q' in request.POST:
            search_query = request.POST["q"]
            # list of all entries 
            entries_list = util.list_entries()
            print(search_query)
            print(entries_list)

            if search_query in entries_list:
                return HttpResponseRedirect(f"{search_query}")
            else :
                # find search query as a substring of all entries list
                sub_entry_list = []
                for entry in entries_list:
                    # check if there are any substring in each entry
                    if search_query in entry:
                        sub_entry_list.append(entry)
                print(sub_entry_list)
                return render(request, "encyclopedia/search.html", {
                    "sub_entry_list": sub_entry_list
                })
            # # # End of check if get a query from user # # #

        elif "new_title" and "new_content" in request.POST:
            new_title = request.POST["new_title"]
            new_content = request.POST["new_content"]

            # Check if the encyclopedia entry is already exist
            if new_title not in util.list_entries():
                # if not exist in encyclopedia entry
                util.save_entry(title=new_title, content=new_content)
                # taking to the new entry page
                return HttpResponseRedirect(f"{new_title}")
            else: 
            # * * * * * Display an error message * * * * * *
                return render(request, "encyclopedia/new.html",{
                    "err_message" : f"ERROR ! Encyclopedia entry already have this {new_title} title !"
                })

    return render(request, "encyclopedia/new.html")


# Random Page
def random_page(request):
    # Check if method is POST
    if request.method == "POST":  
        # # # Check if get a query from user # # #
        if 'q' in request.POST:
            search_query = request.POST["q"]
            # list of all entries 
            entries_list = util.list_entries()
            print(search_query)
            print(entries_list)

            if search_query in entries_list:
                return HttpResponseRedirect(f"{search_query}")
            else :
                # find search query as a substring of all entries list
                sub_entry_list = []
                for entry in entries_list:
                    # check if there are any substring in each entry
                    if search_query in entry:
                        sub_entry_list.append(entry)
                print(sub_entry_list)
                return render(request, "encyclopedia/search.html", {
                    "sub_entry_list": sub_entry_list
                })
            # # # End of check if get a query from user # # #

    # list of all entries 
    entries_list = util.list_entries()
    # get random entry
    random_entry_title = choice(entries_list)
    # Redirect to Random Entry Page
    return HttpResponseRedirect(f"{random_entry_title}")

# Search Page 
def search_page(request):

    # Check if method is POST
    if request.method == "POST":  
        # # # Check if get a query from user # # #
        if 'q' in request.POST:
            search_query = request.POST["q"]
            # list of all entries 
            entries_list = util.list_entries()
            print(search_query)
            print(entries_list)

            if search_query in entries_list:
                return HttpResponseRedirect(f"{search_query}")
            else :
                # find search query as a substring of all entries list
                sub_entry_list = []
                for entry in entries_list:
                    # check if there are any substring in each entry
                    if search_query in entry:
                        sub_entry_list.append(entry)
                print(sub_entry_list)
                return render(request, "encyclopedia/search.html", {
                    "sub_entry_list": sub_entry_list
                })
            # # # End of check if get a query from user # # #