from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .form import ListingForm
from .models import User , Listing , Bid , Comment , Category


def index(request):
    listings = Listing.objects.filter(is_active= True)
    return render(request, "auctions/index.html" , {
        "listings": listings
    }) 

def listing(request, id):
    listing = Listing.objects.get(id=id)
    message = None
    message_type = None
    if request.method == "POST":
        message , message_type= place_bid(request, listing)

    highest_bid = Bid.objects.filter(bid_product=listing).order_by("-bid_amount").first()
    winner = None
    if not listing.is_active and highest_bid:
        winner = highest_bid.bidder
    comments = Comment.objects.filter(listing=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "highest_bid": highest_bid,
        "message": message,
        "message_type" : message_type, 
        "comments": comments,
        "winner": winner
    })


def place_bid(request, listing):
    amount = request.POST["bid_amount"]
    if not listing.is_active:
        return "This auction has been closed.", "danger"
    if request.user == listing.owner:
        return "You cannot bid on your own listing." , "warning"

    highest_bid = Bid.objects.filter(
        bid_product=listing
    ).order_by("-bid_amount").first()
    if highest_bid and float(amount) <= highest_bid.bid_amount:
        return "Your bid must be higher than the current highest bid." , "danger"
    Bid.objects.create(
        bidder=request.user,
        bid_product=listing,
        bid_amount=amount
    )
    return "Your bid was placed successfully!" , "success"

@login_required
def watchlist(request, id):
    listing = Listing.objects.get(id=id)
    if request.user in listing.watchlist.all():
        listing.watchlist.remove(request.user)
    else:
        listing.watchlist.add(request.user)
    return redirect("listing", id=id)


@login_required
def watchlist_view(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def add_comment(request, id):
    listing = Listing.objects.get(id=id)

    if request.method == "POST":
        message = request.POST["comment"]

        Comment.objects.create(
            user=request.user,
            listing=listing,
            message=message
        )
    return redirect("listing", id=id)


@login_required
def close_listing(request, id):
    listing = Listing.objects.get(id=id)
    if request.user == listing.owner:
        listing.is_active = False
        listing.save()
    return redirect("listing", id=id)

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_page(request, id):
    category = Category.objects.get(id=id)
    listings = Listing.objects.filter(
        category=category,
        is_active=True
    )
    return render(request, "auctions/category_page.html", {
        "category": category,
        "listings": listings
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


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })