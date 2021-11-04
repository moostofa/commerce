from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Form, ChoiceField

from .models import User, Listing, Bid, Comment, Watchlist

#the form a user will fill out to create a new listing
#all model fields will be present except for the time created (handled in models.py) and who created it (user)
class NewListing(ModelForm):
    class Meta:
        model = Listing
        exclude = ["seller", "created", "bid_count"]


# index page displays all listings
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


# log user in (this was provided)
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


# log user out (this was provided)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# register user (this was provided)
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


# display all information about a listing
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
        HttpResponseRedirect(reverse("index"))


# add or remove an item from the user's watchlist
def watchlist_action(request, id):
    if request.method == "POST":
        #get the action the user wanted to perform (add or remove)
        action = request.POST["watchlist-action"]

        #explicitly comparing action to "add" and "remove" incase user inspects element
        if action == "add": 
            Watchlist(user_id = request.user.id, listing_id = int(id)).save()
        elif action == "remove":
            Watchlist.objects.filter(user_id = request.user.id).filter(listing_id = int(id)).delete()
    return HttpResponseRedirect(reverse("index"))


#allow user to make a bid on a certain item
def make_bid(request, id):
    if request.method == "POST":
        #get the data required
        user_id = request.user.id 
        listing_id = int(id) 
        bid = request.POST["bid-amount"]

        #insert into model the user who made the bid, on what item and the bid amount
        Bid(user_id = user_id, listing_id = listing_id, bid = bid).save()

        #update the price and bid count of the current listing
        item = Listing.objects.get(pk = listing_id)
        item.price = bid
        item.bid_count += 1
        item.save(update_fields = ["price", "bid_count"])

        #redirect user to index page
        return HttpResponseRedirect(reverse("index"))


# allow user to create a new listing
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


# display the user's watchlist
@login_required
def watchlist(request):
    if request.method == "GET":
        users_watchlist = list(Watchlist.objects.filter(user_id = request.user.id).values_list("listing_id", flat = True))
        return render(request, "auctions/watchlist.html", {
            "items_in_watchlist": Listing.objects.filter(id__in = users_watchlist)
        })


# take user to a page where they can select an item category to view
@login_required
def categories(request):
    if request.method == "GET":
        #get all categories from Listing model as a list()
        categories = list(Listing.objects.values_list("category", flat = True))
        #convert the list into a set() and sort it
        categories = sorted({category.lower().capitalize() for category in categories if category})

        return render(request, "auctions/categories.html", {
            "categories": categories
        })
    else:
        return HttpResponseRedirect(reverse("category", args = [request.POST["category-selection"]]))

#TODO: list all items in the category (type) chosen by then user
def category(request, type):
    return HttpResponse(f"This is in the category view. The chosen category is: {type}")