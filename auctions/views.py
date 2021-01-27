from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm


def index(request):
    listings = Listing.objects.filter(is_active=True).order_by('-posted_date')
    return render(request, "auctions/index.html", {'listings': listings})

def categories(request):
    categories = Listing.objects.filter(is_active=True).values('category').distinct()
    return render(request, "auctions/categories.html", {'categories': categories})

def cat_items(request, name):
    listings = Listing.objects.filter(category=name).filter(is_active=True).order_by('-posted_date')
    return render(request, "auctions/cat_items.html", {'listings': listings, 'name': name})

def new(request):
    instance = Listing(creator=request.user)
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "auctions/new.html", 
            {'form': ListingForm(instance=instance), 
            'message': 'Your listing was created successfully'})
        else:
            return render(request, "auctions/new.html", 
            {'form': ListingForm(instance=instance), 
            'message': 'Form error: your listing was not created'})
    else:
        return render(request, "auctions/new.html", 
            {'form': ListingForm(instance=instance)})

def watchlist(request):
    watchlist = Listing.objects.all().filter(watched_by=request.user).order_by('-posted_date')
    return render(request, "auctions/watchlist.html", {'watchlist': watchlist})

def my_listings(request):
    listings = Listing.objects.all().filter(creator=request.user).order_by('-posted_date')
    return render(request, "auctions/my_listings.html", {'listings': listings})

def listing(request, name):
    listing = Listing.objects.get(pk=name)
    user = User.objects.get(username=request.user.username)
    w = listing in user.watching.all()
    comm_instance = Comment(listing=listing, author=request.user)
    cform = CommentForm(instance=comm_instance)
    comments = Comment.objects.filter(listing=listing).order_by('-comment_datetime')
    if request.method == 'POST' and "bid" in request.POST:
        form = BidForm(request.POST)
        highest = Bid.objects.filter(listing=listing).order_by('-bid_date').first()
        if highest:
                winner = highest.bid_user
                to_beat= float(highest.amount)
        else:
            highest = None
            to_beat = listing.starting_bid
            winner = False
        instance = Bid(listing=listing, bid_user=request.user)
        if form.is_valid() and float(request.POST['amount']) > to_beat : 
            form.save()
            highest = Bid.objects.filter(listing=listing).order_by('-bid_date').first()
            winner = highest.bid_user
            listing.current_price = highest.amount
            listing.save()
            return render(request, 'auctions/listing.html', {
                    "message": 'Bid successfully placed',
                    "listing": listing,
                    "highest": highest.amount,
                    "winner": winner,
                    "comments": comments,
                    "w": w,
                    "cform": cform,
                    "bid_count": Bid.objects.filter(listing=listing).count(),
                    "form": BidForm(instance=instance)
            })
        elif form.is_valid():
            return render(request, 'auctions/listing.html', {
                    "message": 'Bid is too low',
                    "listing": listing,
                    "highest": to_beat,
                    "winner": winner,
                    "cform": cform,
                    "comments": comments,
                    "w": w,
                    "bid_count": Bid.objects.filter(listing=listing).count(),
                    "form": BidForm(instance=instance)
            })
        else:
            return HttpResponseBadRequest("Bad Request: form was not valid")
    elif request.method == 'POST' and "close" in request.POST:
        listing.is_active = False
        listing.save()
        highest = Bid.objects.filter(listing=listing).order_by('-bid_date').first()
        if highest:
                winner = highest.bid_user
        else:
            highest = None
            winner = False
        return render(request, 'auctions/listing.html', {
                    "message": 'Auction has been closed',
                    "listing": listing,
                    "highest": highest,
                    "cform": cform,
                    "comments": comments,
                    "w": w,
                    "bid_count": Bid.objects.filter(listing=listing).count(),
                    "winner": winner
            })
    elif request.method == 'POST' and "watch" in request.POST:
        # change watched status and create message
        if listing in user.watching.all():
            listing.watched_by.remove(user)
            message = 'The listing was removed from your watchlist'
            w = False
        else:
            listing.watched_by.add(user)
            message = 'The listing was added to your watchlist'
            w = True
        highest = Bid.objects.filter(listing=listing).order_by('-bid_date').first()
        if highest:
                winner = highest.bid_user
                highest = highest.amount
        else:
            highest = None
            winner = False
        return render(request, 'auctions/listing.html', {
                    "message": message,
                    "listing": listing,
                    "highest": highest,
                    "cform": cform,
                    "comments": comments,
                    "w": w,
                    "bid_count": Bid.objects.filter(listing=listing).count(),
                    "winner": winner
            })
    elif request.method == 'POST':
        cform = CommentForm(request.POST)
        cform.save()
        cform = CommentForm(instance=comm_instance)
        comments = Comment.objects.filter(listing=listing).order_by('-comment_datetime')
        highest = Bid.objects.filter(listing=listing).order_by('-bid_date').first()
        if highest:
                winner = highest.bid_user
                highest = highest.amount
        else:
            highest = None
            winner = False
        return render(request, 'auctions/listing.html', {
                    "message": 'Your comment has been saved',
                    "listing": listing,
                    "highest": highest,
                    "cform": cform,
                    "comments": comments,
                    "w": w,
                    "bid_count": Bid.objects.filter(listing=listing).count(),
                    "winner": winner
            })
    else:
        listing = Listing.objects.get(pk=name)
        if listing:
            instance = Bid(listing=listing, bid_user=request.user)
            highest = Bid.objects.filter(listing=listing.id).order_by('-bid_date').first()
            if highest:
                winner = highest.bid_user
                highest = highest.amount
            else:
                highest = listing.starting_bid
                winner = False
            return render(request, 'auctions/listing.html', {
                "listing": listing,
                "highest": highest,
                "winner": winner,
                "cform": cform,
                "comments": comments,
                "w": w,
                "bid_count": Bid.objects.filter(listing=listing).count(),
                "form": BidForm(instance=instance)
            })
        else:
            return HttpResponseBadRequest("Bad Request: listing does not exist")

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
