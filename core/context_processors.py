from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address
from django.shortcuts import get_object_or_404
from django.db.models import Min, Max, Count


def default(request):
    # user = request.user
    categories_context = Category.objects.all()
    vendors_context = Vendor.objects.all()
    try:
        address_context = Address.objects.get(user=request.user)
    except:
        address_context = None

    # for product filtering based on price
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    return {
        'categories_context': categories_context,
        'vendors_context': vendors_context,
        'address_context': address_context,
        'min_max_price_context': min_max_price,
    }
