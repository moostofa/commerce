from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, FloatField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey

#website users
class User(AbstractUser):
    pass

"""
A table of listings

Possible columns:
1. Listing ID - Primary key
2. CharField - listing title
3. IntegerField - price
4. DateTimeField - creation time
5. TextArea(?) - additional info about item
6. CharField(?) - item category
"""
class Listing(models.Model):
    title = CharField(max_length=20)
    price = FloatField()
    created = DateTimeField()
    description = TextField()
    category = CharField(max_length=10)


"""
A table which records the bidding details for a particular listing

Possible columns:
1. Listing ID - foreign key
2. IntegerField - current bid
3. IntegerField - number of bids
"""
class Bid(models.Model):
    listing = ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    bid = FloatField()
    bid_count = IntegerField()


"""
A table containing the comments on a particular listing

Possible columns:
1. Foreign key - user ID (who commented)
2. Foreign key - listing ID
3. TextArea(?) - the user's comment
"""
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