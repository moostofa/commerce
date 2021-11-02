from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, FloatField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey

#website users
class User(AbstractUser):
    pass


class Listing(models.Model):
    title = CharField(max_length=20)
    price = FloatField()
    created = DateTimeField(editable=False, auto_now_add=True)
    description = TextField()
    category = CharField(max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return f"""
        title = {self.title},
        price = ${self.price},
        time created (UTC) = {self.created},
        description = {self.description},
        category = {self.category}
        """


class Bid(models.Model):
    listing = ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    bid = FloatField()
    bid_count = IntegerField()


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