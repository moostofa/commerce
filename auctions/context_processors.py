from .models import Listing

def category_context(request):
    categories = list(Listing.objects.values_list("category", flat = True))
    categories = sorted({category for category in categories if category})
    return {
        "category_menu": categories
    }