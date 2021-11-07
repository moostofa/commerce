# context_processors.py allows the list of categories to be globally accessible by the category select menu in layout.html

from .models import Listing

def category_context(request):
    # get a values_list of the category field for every listing item
    categories = list(Listing.objects.values_list("category", flat = True))
    # convert into a sorted set
    categories = sorted({category for category in categories if category})
    return {
        "category_menu": categories
    }
