from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address
from django.shortcuts import get_object_or_404


def default(request):
    # user = request.user
    categories = Category.objects.all()
    # address = get_object_or_404(Address, user=user)
    # if address:
    #     address = address
    # else:
    #     address = []
    address = []
    return {
        'categories': categories,
        'address': address,
    }
