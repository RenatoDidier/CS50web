from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from sympy import re

from .models import User, AuctionListing, WatchList, Comments

categories_global = ["Geral", "Clothes", "Toys",
                     "Gaming", "Acessory", "House", "Books"]


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


def list(request, id, title):
    list = AuctionListing.objects.get(pk=id, title=title)
    comments = Comments.objects.filter(id_list=list)
    user_id = User.objects.get(pk=request.user.id)
    watchlist_status = 1
    if not WatchList.objects.filter(id_user=user_id, id_list=list):
        watchlist_status = 0

    return render(request, "auctions/list.html", {
        "list": list,
        "comments": comments,
        "wl_status": watchlist_status
    })


def watchlist(request):
    if request.method == "POST":
        id_l = AuctionListing.objects.get(pk=request.POST["id"])
        id_u = User.objects.get(pk=request.user.id)

        if not WatchList.objects.filter(id_list=id_l, id_user=id_u):
            add = WatchList.objects.create(id_list=id_l, id_user=id_u)
            add.save()
            return HttpResponseRedirect(reverse("auctions:watchlist"))

        WatchList.objects.filter(id_list=id_l, id_user=id_u).delete()
        return HttpResponseRedirect(reverse("auctions:watchlist"))

    else:
        list = []
        id_user = User.objects.get(pk=request.user.id)
        user_watchlists = WatchList.objects.filter(id_user=id_user)

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

        listing = AuctionListing.objects.create(
            id_user=id_owner, title=title, category=category, description=description, image=url_img, price=price, date=now)
        listing.save()
        return HttpResponseRedirect(reverse("auctions:index"))

    else:
        return render(request, "auctions/create.html", {
            "categories": categories_global,
        })


def add_comment(request):
    id_user = User.objects.get(pk=request.user.id)
    id_list = AuctionListing.objects.get(pk=request.POST["id_list"])
    comment = request.POST["comment"]

    add_comment = Comments.objects.create(
        id_list=id_list, id_user=id_user, comment=comment)
    add_comment.save()

    url = ("/product/" + request.POST["id_list"] + "/" + id_list.title)
    return HttpResponseRedirect(url)


def rmv_comment(request):
    id_c = Comments.objects.get(pk=request.POST["id_c"]).delete()

    url = ("/product/" + request.POST["id_l"] + "/" + request.POST["title"])
    return HttpResponseRedirect(url)


def editcomment(request):
    if request.method == "POST":
        comment = Comments.objects.get(pk=request.POST["id_comment"])
        comment.comment = request.POST["comment"]
        comment.save()

        url = ("/product/" +
               request.POST["id_list"] + "/" + comment.id_list.title)
        return HttpResponseRedirect(url)

    else:
        id_comment = request.GET["comment"]
        id_list = request.GET["id_list"]
        comment = Comments.objects.get(pk=id_comment)

        return render(request, "auctions/editcomment.html", {
            "comment": comment,
            "id_list": id_list,
        })


def editlist(request, id_list):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        image = request.POST["url_img"]

        list = AuctionListing.objects.get(pk=id_list)

        list.title = title
        list.description = description
        list.price = price
        list.category = category
        list.image = image

        list.save()

        return HttpResponseRedirect(reverse("auctions:mylist"))

    else:
        list = AuctionListing.objects.get(pk=id_list)

        return render(request, "auctions/editlist.html", {
            "list": list,
            "categories": categories_global,
        })
