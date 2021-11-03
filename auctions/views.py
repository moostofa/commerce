from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import User, Listing, Bid, Comment, Watchlist

#the form a user will fill out to create a new listing
#all model fields will be present except for the time created (handled in models.py) and who created it (user)
class NewListing(ModelForm):
    class Meta:
        model = Listing
        exclude = ["seller", "created"]


#TODO: display listings
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


#TODO: display all info about the listing
@login_required
def view_listing(request, id):
    #GET request: take user to page with listing info, passing in the item as context
    if request.method == "GET":
        return render(request, "auctions/page.html", {
            "item": Listing.objects.get(pk = int(id)),
            #item_in_watchling returns a bool indicating whether or not the chosen item is in the user's watchlist
            "item_in_watchlist": int(id) in Watchlist.objects.values_list("listing_id", flat=True)
        })
    else:
        #if user pressed add to/remove from watchlist button
        if request.POST["watchlist-action"]:
            action = request.POST["watchlist-action"]
            #explicitly comparing to "add" and "remove" incase user inspects element
            if action == "add": 
                Watchlist(user_id = request.user.id, listing_id = int(id)).save()
            elif action == "remove":
                Watchlist.objects.filter(user_id = request.user.id).filter(listing_id = int(id)).delete()
        return HttpResponseRedirect(reverse("index"))


#TODO: allow user to create a listing. Make a Django form for this.
@login_required
def create_listing(request):
    if request.method == "GET":
        #display form for creating a listing
        return render(request, "auctions/create.html", {
            "form": NewListing()
        })
    else:
        #get form data
        form = NewListing(request.POST)
        if not form.is_valid():
            return HttpResponse("error")
        
        #create a database entry using the form data, inserting it into the Listing model (table)
        model = Listing(
            title = form.cleaned_data["title"],
            price = form.cleaned_data["price"],
            seller = request.user.username,
            description = form.cleaned_data["description"],
            category = form.cleaned_data["category"],
            image = form.cleaned_data["image"]
        )

        #save the entry and redirect user to index
        model.save()
        return HttpResponseRedirect(reverse("index"))


#TODO: display user's watchlist (maybe I need a DB table or another DS to keep track of the watchlist?)
@login_required
def watchlist(request):
    pass


#TODO: display listings by category
@login_required
def category(request):
    pass