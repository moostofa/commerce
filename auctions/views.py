from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import F
from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Comment, Listing, ObtainedItem, User, Watchlist


# the form a user will fill in to create a new listing
# all model fields will be present except for the time created (handled in models.py) and who created it (user)
class NewListing(ModelForm):
    class Meta:
        model = Listing
        exclude = ["seller", "created", "active"]


# the form a user will fill in to add a comment
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_title", "comment"]
        labels = {
            "comment_title": "",
            "comment": ""
        }
        widgets = {
            "comment_title": TextInput(attrs={
                "placeholder":"Comment title", 
                "class":"form-control w-25"
            }),
            "comment": Textarea(attrs={
                "placeholder":"Write your comment here", 
                "class":"form-control w-25"
            })
        }


# index page displays all ACTIVE listings. NOTE: category view also redirects to this page, but with a filtered QuerySet
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active = True)
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


# allow user to create a new listing
@login_required
def create_listing(request):
    if request.method == "GET":
        # display form for creating a listing
        return render(request, "auctions/create.html", {
            "form": NewListing()
        })
    else:
        # get POST form data
        form = NewListing(request.POST)
        if not form.is_valid():
            return HttpResponse("error")
        
        # create a database entry using the form data, inserting it into the Listing model (table)
        # neat little trick: unpacking a dictionary (the form is returned as a dict)
        new_item = Listing(**form.cleaned_data) 
        new_item.seller = request.user
        
        # check if a cateogory was provided & save the entry
        if new_item.category:
            new_item.category = new_item.category.lower().capitalize()
        new_item.save()

        # redirect user to index
        return HttpResponseRedirect(reverse("index"))


# display all information about a listing
@login_required
def view_listing(request, id):
    #GET request: take user to page with listing info, passing in the item as context
    if request.method == "GET":
        listing_id = int(id)
        item = Listing.objects.get(pk = listing_id)

        return render(request, "auctions/page.html", {
            #pass in the specific listing item the user wants to view & its bid details
            "item": item,
            "bid_info": Bid.objects.get(listing = item) if Bid.objects.filter(listing = item) else None,

            # item_in_watchling returns a bool indicating whether or not the chosen item is in the user's watchlist
            # in template, this is used to determine whether the watchlist button should display "add to" or "remove from"
            "item_in_watchlist": listing_id in Watchlist.objects.values_list("listing_id", flat=True),
            
            # allow user to make a comment & view all other comments
            "comment_form": CommentForm(),
            "comments": Comment.objects.filter(listing = item).values("user__username", "comment", "time")
        })


# add or remove an item from the user's watchlist
@login_required
def watchlist_action(request, id):
    if request.method == "POST":
        # get the action the user wanted to perform (add or remove)
        action = request.POST["watchlist-action"]

        # explicitly comparing action to "add" and "remove" incase user inspects element
        if action == "add": 
            Watchlist(user_id = request.user.id, listing_id = int(id)).save()
        elif action == "remove":
            Watchlist.objects.filter(user_id = request.user.id).filter(listing_id = int(id)).delete()
    return HttpResponseRedirect(reverse("watchlist"))


# display the user's watchlist
@login_required
def watchlist(request):
    if request.method == "GET":
        users_watchlist = list(Watchlist.objects.filter(user_id = request.user.id).values_list("listing_id", flat = True))
        return render(request, "auctions/watchlist.html", {
            "items_in_watchlist": Listing.objects.filter(id__in = users_watchlist)
        })


#allow user to make a bid on a certain item
@login_required
def make_bid(request, id):
    if request.method == "POST":
        listing_item = Listing.objects.get(pk = int(id)) 

        #insert bid details into Bid model - "winner" is the current highest bidder
        Bid.objects.update_or_create(
            listing = listing_item,
            defaults={
                "winner": request.user,
                "bid": request.POST["bid-amount"]
            }
        )
        # increment bid_count
        Bid.objects.filter(listing = listing_item).update(bid_count = F("bid_count") + 1)

        #redirect user to index page
        return HttpResponseRedirect(reverse("index"))


# takes POST data from category select menu and passes it as a parameter to the category view
# NOTE: I could not send POST data from a select menu directly to the category view. How do I do this?
def helper(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("category", args = [request.POST["category-selection"]]))


# list all ACTIVE items in the category chosen by then user
def category(request, choice):
    if request.method == "GET":
        return render(request, "auctions/index.html", {
            "category": choice,
            "listings": Listing.objects.filter(active = True).filter(category = choice)
        })


# user who created the listing can close the auction, making the highest bidder the winner
@login_required
def close_auction(request, id):
    if request.method == "POST":
        # try to get the winner of the auction
        # If an exception is raised, the auction was ended prematurely (without any bids), thus, there is no winner
        try:
            winner = Bid.objects.get(listing_id = int(id)).winner
        except Bid.DoesNotExist:
            pass
        else:
            ObtainedItem(user = winner, listing = Listing.objects.get(pk = int(id))).save()
        finally:
            Listing.objects.filter(pk = int(id)).update(active = False)
    return HttpResponseRedirect(reverse("index"))


# show users profile: what active items they have listed, and what items they have won
@login_required
def profile(request):
    if request.method == "GET":
        items_won = ObtainedItem.objects.filter(user = request.user).values_list("listing", flat = True)
        return render(request, "auctions/profile.html", {
            "my_listings": Listing.objects.filter(active = True).filter(seller = request.user),
            "my_winnings": Listing.objects.filter(id__in = items_won)
        })


# allow user to make a comment on a listing
@login_required
def comment(request, id):
    if request.method == "POST":
        # get the comment and validate it
        form = CommentForm(request.POST)
        if not form.is_valid():
            return HttpResponse("comment form is invalid")
        
        # add into the Comment model the user who commented, on which listing and the comment
        Comment(
            listing = Listing.objects.get(pk = int(id)), 
            user = request.user, 
            comment = form.cleaned_data["comment"]
        ).save()

        # "refresh" the webpage
        return HttpResponseRedirect(reverse("view_listing", args=[id]))
