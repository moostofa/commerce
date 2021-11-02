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

Table columns:
1. id - Primary key
2. Item title - CharField
3. bid price = FloatField
4. DateTimeField - auto-generates the time when the item was listed
5. description - item details - TextField
6. category (optional) - CharField
"""
class Listing(models.Model):
    title = CharField(max_length=20)
    price = FloatField()
    created = DateTimeField(editable=False, auto_now_add=True)
    description = TextField()
    category = CharField(max_length=10, blank=True, null=True)


"""
A table which records the bidding details for a particular listing

Table columns:
1. id - primary key (NOTE: this is unused)
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

Table columns:
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