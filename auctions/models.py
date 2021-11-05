from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, DecimalField, IntegerField, TextField, URLField
from django.db.models.fields.related import ForeignKey

#website users
class User(AbstractUser):
    pass


class Listing(models.Model):
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

    def __str__(self) -> str:
        return f"""
        title = {self.title},
        price = ${self.price},
        seller = {self.seller}
        time created = {self.created},
        description = {self.description},
        category = {self.category},
        """


"""
FOREIGN KEY Bid (user_id) REFERENCES PRIMARY KEY User (id)
FOREIGN KEY Bid (listing_id) REFERENCES PRIMARY KEY Listing (id)
"""
class Bid(models.Model):
    listing = ForeignKey(
        Listing,
        on_delete=models.CASCADE
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
class Comment(models.Model):
    listing = ForeignKey(
        Listing,
        on_delete=CASCADE
    )
    user = ForeignKey(
        User,
        on_delete=CASCADE
    )
    comment = TextField()


"""
FOREIGN KEY Watchlist (user_id) REFERENCES PRIMARY KEY User (id)
FOREIGN KEY Watchlist (listing_id) REFERENCES PRIMARY KEY Listing (id)
"""
class Watchlist(models.Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE
    )
    listing = ForeignKey(
        Listing,
        on_delete=CASCADE
    )