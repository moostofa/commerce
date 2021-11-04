from .models import Listing

def category_list(request):
    categories = list(Listing.objects.values_list("category", flat = True))
    categories = sorted({category.lower().capitalize() for category in categories if category})
    return {
        "categories_list": categories
    }