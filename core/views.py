from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address

# taggit
from taggit.models import Tag


def home_view(request):
    Products = Product.objects.filter(
        featured=True, product_status='published')
    Categories = Category.objects.all()
    context = {
        'Products': Products,
        'Categories': Categories,
    }
    return render(request, 'core/index.html', context=context)


def all_categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'core/all_categories.html', context)


def products_list_view(request):
    Products = Product.objects.filter(
        featured=True, product_status='published')
    Vendors = Vendor.objects.all()
    context = {
        'Products': Products,
    }
    return render(request, 'core/products-list.html', context=context)


def products_detail_view(request, pid):

    product = get_object_or_404(Product, pid=pid)
    related_products = Product.objects.filter(
        category=product.category, product_status='published'
    ).exclude(pid=product.pid)

    p_images = product.p_images.all()

    context = {
        'product': product,
        'related_products': related_products,
        'p_images': p_images,
    }

    return render(request, 'core/product-detail.html', context=context)


def products_in_category_view(request, cid):
    category = get_object_or_404(Category, cid=cid)
    products_in_category = Product.objects.filter(
        category=category, product_status='published')
    context = {
        'products_in_category': products_in_category,
        'category': category,
    }
    return render(request, 'core/products_in_category.html', context=context)


def all_vendors(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors,
    }
    return render(request, 'core/vendor_list.html', context)


def vendor_details(request, vid):
    vendor = get_object_or_404(Vendor, vid=vid)
    products_of_vendor = Product.objects.filter(
        vendor=vendor, product_status='published').order_by('?')
    context = {
        'vendor': vendor,
        'products_of_vendor': products_of_vendor,
    }
    return render(request, 'core/vendor_details.html', context)


def vendor_shop(request, vid):
    vendor = get_object_or_404(Vendor, vid=vid)
    products_of_vendor = Product.objects.filter(
        vendor=vendor, product_status='published').order_by('?')
    context = {
        'vendor': vendor,
        'products_of_vendor': products_of_vendor,
    }
    return render(request, 'core/vendor_shop.html', context)


def tags(request, tag):

    tag = get_object_or_404(Tag, name=tag)
    tag_products = Product.objects.filter(tags__in=[tag])

    context = {
        'tag_products': tag_products,
        'tag': tag,
    }
    return render(request, 'core/tag.html', context)
