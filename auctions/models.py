from tkinter import CASCADE
from cv2 import CascadeClassifier
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    category = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField()
    price = models.IntegerField()
    date = models.DateTimeField()

class Bids(models.Model):
    id_list = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()

class Comments(models.Model):
    id_list = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

class VoteCheck(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    checker = models.SmallIntegerField()

class VoteSystem(models.Model):
    id_comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    upvote = models.IntegerField()
    downvote = models.IntegerField()

class WatchList(models.Model):
    id_list = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

