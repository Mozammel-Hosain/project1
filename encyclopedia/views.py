from django.shortcuts import render, redirect

from . import util
from markdown2 import Markdown
import random


def convert_markdown_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    html_content = convert_markdown_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
           "message": "The page does not exist" 
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    if request.method == "POST":
        # Safely get the search query from the GET data
        query = request.POST.get('q', '').strip()

        # Handle empty query
        if not query:
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "results": []
            })

        # Get all entries and look for an exact match
        entries = util.list_entries()  # Retrieves all entry titles
        exact_match = next((entry for entry in entries if entry.lower() == query.lower()), None)

        if exact_match:
            # Redirect to the entry page if an exact match is found
            return redirect("entry", title=exact_match)

        # Find partial matches
        matching_entries = [
            entry for entry in entries if query.lower() in entry.lower()
        ]

        # Render search results
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": matching_entries
        })

    # If method is not GET, redirect to index
    return redirect("index")
    

    
def new_page(request):
    if request.method == "POST":
       title = request.POST['title']
       content = request.POST['content']
       if util.get_entry(title):
          return render(request, "encyclopedia/error.html", {
              "message":f"An entry with the title already exists."
          })
       else:
          util.save_entry(title, content)
          html_content = convert_markdown_to_html(title)
          return render(request, "encyclopedia/title.html", {
             "title":title,
             "content":html_content
          })
    return render(request, "encyclopedia/new_page.html")


def edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content":content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html_content = convert_markdown_to_html(title)
        return render(request, "encyclopedia/title.html",{
            "title": title,
            "content": html_content
        })

def rend(request):
    allEntries = util.list_entries()
    random_come = random.choice(allEntries)
    html_content = convert_markdown_to_html(random_come)
    return render(request, "encyclopedia/title.html",{
        "title": random_come,
        "content": html_content
    })
