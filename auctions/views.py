from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import User, Listing, Bid, Comment

class NewListing(ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"


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
def view_listing():
    pass


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
        
        #create a database entry using the form data, inserting it into the model (table)
        model = Listing(
            title = form.cleaned_data["title"],
            price = form.cleaned_data["price"],
            description = form.cleaned_data["description"],
            category = form.cleaned_data["category"]
        )

        #save the entry and redirect user to index
        model.save()
        return HttpResponseRedirect(reverse("index"))


#TODO: display user's watchlist (maybe I need a DB table or another DS to keep track of the watchlist?)
@login_required
def watchlist():
    pass


#TODO: display listings by category
@login_required
def category():
    pass