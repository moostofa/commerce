from django.contrib.auth.models import AbstractUser
from django.db.models import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import BooleanField, CharField, DateTimeField, DecimalField, IntegerField, TextField, URLField
from django.db.models.fields.related import ForeignKey


# website users
class User(AbstractUser):
    pass


class Listing(Model):
    seller = ForeignKey(
        User,
        on_delete=CASCADE
    )

    title = CharField(max_length=20)
    price = DecimalField(max_digits=9, decimal_places=2)
    created = DateTimeField(editable=False, auto_now_add=True)
    description = TextField()
    category = CharField(max_length=20, blank=True, null=True)
    image = URLField(verbose_name="Image URL", blank=True, null=True)
    active = BooleanField(default=True)


"""
FOREIGN KEY Bid (user_id) REFERENCES PRIMARY KEY User (id)
FOREIGN KEY Bid (listing_id) REFERENCES PRIMARY KEY Listing (id)
"""
class Bid(Model):
    listing = ForeignKey(
        Listing,
        on_delete=CASCADE
    )
    winner = ForeignKey(
        User,
        on_delete=CASCADE
    )
    bid = DecimalField(max_digits=9, decimal_places=2)
    bid_count = IntegerField(default=0)


"""
FOREIGN KEY Comment (user_id) REFERENCES PRIMARY KEY User (id)
FOREIGN KEY Comment (listing_id) REFERENCES PRIMARY KEY Listing (id)
"""
class Comment(Model):
    listing = ForeignKey(
        Listing,
        on_delete=CASCADE
    )
    user = ForeignKey(
        User,
        on_delete=CASCADE
    )
    comment = TextField()
    time = DateTimeField(auto_now_add=True)


"""
FOREIGN KEY Watchlist (user_id) REFERENCES PRIMARY KEY User (id)
FOREIGN KEY Watchlist (listing_id) REFERENCES PRIMARY KEY Listing (id)
"""
class Watchlist(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE
    )
    listing = ForeignKey(
        Listing,
        on_delete=CASCADE
    )


"""
FOREIGN KEY ObtainedItem (user_id) REFERENCES PRIMARY KEY User (id)
FOREIGN KEY ObtainedItem (listing_id) REFERENCES PRIMARY KEY Listing (id)
"""
class ObtainedItem(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE
    )
    listing = ForeignKey(
        Listing,
        on_delete=PROTECT
    )
