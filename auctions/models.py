from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, DecimalField, IntegerField, TextField, URLField
from django.db.models.fields.related import ForeignKey

#website users
class User(AbstractUser):
    pass


class Listing(models.Model):
    title = CharField(max_length=20)
    price = DecimalField(max_digits=9, decimal_places=2)
    seller = CharField(max_length=20)
    created = DateTimeField(auto_now_add=True)
    description = TextField()
    category = CharField(max_length=20, blank=True, null=True)
    image = URLField(blank=True, null=True)
    bid_count = IntegerField(default=0)

    def __str__(self) -> str:
        return f"""
        title = {self.title},
        price = ${self.price},
        seller = {self.seller}
        time created = {self.created},
        description = {self.description},
        category = {self.category},
        number of bids on item: {self.bid_count}
        """


class Bid(models.Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE
    )
    listing = ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    bid = DecimalField(max_digits=9, decimal_places=2)


class Comment(models.Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE
    )
    listing = ForeignKey(
        Listing,
        on_delete=CASCADE
    )
    comment = TextField()

class Watchlist(models.Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE
    )
    listing = ForeignKey(
        Listing,
        on_delete=CASCADE
    )