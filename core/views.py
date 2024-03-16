from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address


def home_view(request):
    Products = Product.objects.filter(
        featured=True, product_status='published')
    Categories = Category.objects.all()
    context = {
        'Products': Products,
        'Categories': Categories,
    }
    return render(request, 'core/index.html', context=context)


def products_list_view(request):
    # Products = Product.objects.filter(featured=True, product_status='published')
    Products = Product.objects.all()
    Categories = Category.objects.all()
    Vendors = Vendor.objects.all()
    context = {
        'Products': Products,
        'Categories': Categories,
        'Vendors': Vendors,
    }
    return render(request, 'core/products-list.html', context=context)


def products_detail_view(request, pid):
    # Products = Product.objects.filter(featured=True, product_status='published')
    Products = Product.objects.all()
    Categories = Category.objects.all()
    Vendors = Vendor.objects.all()

    product = get_object_or_404(Product, pid=pid)
    related_products = Product.objects.filter(
        category=product.category, product_status='published'
    ).exclude(pid=product.pid)

    context = {
        'Products': Products,
        'Categories': Categories,
        'Vendors': Vendors,
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'core/product-detail.html', context=context)


def products_in_category_view(request, cid):
    category = get_object_or_404(Category, cid=cid)
    products_in_category = Product.objects.filter(category=category)
    context = {
        'products_in_category': products_in_category,
        'category': category,
    }
    return render(request, 'core/products_in_category.html', context=context)
