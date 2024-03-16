from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address
from django.shortcuts import get_object_or_404


def default(request):
    # user = request.user
    categories_context = Category.objects.all()
    vendors_context=Vendor.objects.all()

    # address = get_object_or_404(Address, user=user)
    # if address:
    #     address = address
    # else:
    #     address = []
    address = []
    return {
        'categories_context': categories_context,
        'vendors_context': vendors_context,
    }
