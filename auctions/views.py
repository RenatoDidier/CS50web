from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User, AuctionListing, WatchList


def index(request):
    list = AuctionListing.objects.all()

    return render(request, "auctions/index.html", {
        "auction": list,
    })


@login_required(login_url="/login")
def mylist(request):
    list = AuctionListing.objects.filter(id_user=request.user.id)

    return render(request, "auctions/mylist.html", {
        "auction": list,
    })

<<<<<<< Updated upstream
=======
# list test


>>>>>>> Stashed changes
def list(request, id, title):

    list = AuctionListing.objects.get(pk=id, title=title)

    return render(request, "auctions/list.html", {
        "product": str(title),
        "list": list,
    })


def watchlist(request):
    if request.method == "POST":
        id_l = AuctionListing.objects.get(pk = request.POST["id"])
        id_u = User.objects.get(pk = request.user.id)

        if not WatchList.objects.filter(id_list=id_l, id_user=id_u):
            add = WatchList.objects.create(id_list = id_l, id_user = id_u)
            add.save()
            return HttpResponseRedirect(reverse("auctions:watchlist"))
        
        WatchList.objects.filter(id_list=id_l, id_user=id_u).delete()
        return HttpResponseRedirect(reverse("auctions:watchlist"))
        
    else:
        list = []
        id_user = User.objects.get(pk = request.user.id)
        user_watchlists = WatchList.objects.filter(id_user = id_user)

        for element in user_watchlists:
            id_list = element.id_list
            list.append(id_list)

        return render(request, "auctions/watchlist.html", {
            "list": list,
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        id = request.user.id
        id_owner = User.objects.get(pk=id)
        title = request.POST["title"]
        category = request.POST["category"]
        description = request.POST["description"]
        price = int(request.POST["initial_price"])
        url_img = request.POST["url_img"]
        now = datetime.datetime.now()

        listing = AuctionListing.objects.create(id_user = id_owner, title = title, category = category, description = description, image = url_img, price = price, date = now)
        listing.save()
        return HttpResponseRedirect(reverse("auctions:index"))

    else:
        return render(request, "auctions/create.html")