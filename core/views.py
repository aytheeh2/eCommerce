from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address
from django.contrib.auth.decorators import login_required
from django.conf import settings

# taggit
from taggit.models import Tag

# for product reviews
from .forms import ReviewForm
from django.http import JsonResponse

# for ajax product filtering
from django.template.loader import render_to_string

# paypal
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm


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
        product_status='published').order_by('-date')
    Vendors = Vendor.objects.all()
    context = {
        'Products': Products,
    }
    return render(request, 'core/products-list.html', context=context)


# Redirect anonymous users to the login page
# @login_required(login_url='/login/')
def products_detail_view(request, pid):

    product = get_object_or_404(Product, pid=pid)
    related_products = Product.objects.filter(
        category=product.category, product_status='published'
    ).exclude(pid=product.pid)

    # extra images
    p_images = product.p_images.all()

    # reviews
    reviews_of_product = ProductReview.objects.filter(
        product=product).order_by('-date')
    # finding average review rating
    total_rating = 0
    for i in reviews_of_product:
        total_rating += i.rating
    try:
        average_rating = total_rating/len(reviews_of_product)
    except ZeroDivisionError:
        average_rating = "Not Rated"

    # for product review see ajax addReview view
    review_form = ReviewForm()

    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
        # checks no.of reviews the user has for the product
        no_of_reviews = ProductReview.objects.filter(
            product=product, user=user).count()
        can_review = False
        # if user has more than 0 review, that means user has atleast 1 review, so set can_review to false so that form will be hidden using {% if can_review %}
        if no_of_reviews == 0:
            can_review = True
    else:
        user = None
        can_review = False  # Allow anonymous users to review

    context = {
        'product': product,
        'related_products': related_products,
        'p_images': p_images,
        'reviews_of_product': reviews_of_product,
        'average_rating': average_rating,
        'review_form': review_form,
        'can_review': can_review,
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


def ajax_addreview(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    # Get the date of the review to pass to ajax
    review_date = review.date

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
        # formatting the date as similar to the |date:"d M, Y" in the template
        'date': review_date.strftime("%I:%M %p %d %b, %Y"),
    }

    return JsonResponse(
        {
            'bool': True,
            'context': context
        }
    )


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    Products = Product.objects.filter(
        product_status='published',).order_by('-id').distinct()

    # filtering by price
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    Products = Product.objects.filter(
        product_status='published').order_by('-date').distinct()

    Products = Products.filter(price__gte=min_price)
    Products = Products.filter(price__lte=max_price)

    if len(categories) > 0:
        Products = Product.objects.filter(
            category__id__in=categories).distinct()

    if len(vendors) > 0:
        Products = Product.objects.filter(
            vendor__id__in=vendors).distinct()

    context = {
        'Products': Products,
    }

    data = render_to_string("core/async/products-list.html", context)

    return JsonResponse({
        "data": data
    })

# @login_required


def add_to_cart(request):
    if request.user:
        print('sssss')
    else:
        print('nooooooooooooo')

    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'quantity': request.GET['quantity'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:

        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = int(
                cart_product[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({
        "data": request.session['cart_data_obj'],
        "total_cart_items": len(request.session['cart_data_obj'])
    })


def cart_view(request):
    cart_total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total += int(item['quantity']) * float(item['price'])
        return render(request, 'core/cart.html', {
            "cart_data": request.session['cart_data_obj'],
            "total_cart_items": len(request.session['cart_data_obj']),
            "cart_total": cart_total
        })
    else:
        messages.warning(request, "Your Cart is empty!")
        return redirect('core:home')


def delete_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        print('yes', request.session['cart_data_obj'])
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total += int(item['quantity']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {
        "cart_data": request.session['cart_data_obj'],
        "total_cart_items": len(request.session['cart_data_obj']),
        "cart_total": cart_total
    })

    return JsonResponse({
        "data": context,
        "total_cart_items": len(request.session['cart_data_obj']),

    })


def update_items_in_cart(request):
    product_id = str(request.GET['id'])
    product_quantity = request.GET['quantity']

    if 'cart_data_obj' in request.session:
        print('yes', request.session['cart_data_obj'])
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = product_quantity
            request.session['cart_data_obj'] = cart_data

    cart_total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total += int(item['quantity']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {
        "cart_data": request.session['cart_data_obj'],
        "total_cart_items": len(request.session['cart_data_obj']),
        "cart_total": cart_total
    })

    return JsonResponse({
        "data": context,
        "total_cart_items": len(request.session['cart_data_obj']),

    })


@login_required
def checkout(request):

    total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['quantity']) * float(item['price'])

        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount,

        )

        cart_total = 0
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total += int(item['quantity']) * float(item['price'])

        cart_order_products = CartOrderItems.objects.create(
            order=order,
            invoice_no="INVOICE-NO-"+str(order.id),
            item=item['title'],
            qty=item['quantity'],
            price=item['price'],
            total=float(item['quantity']) * float(item['price']),
            image=item['image'],
            product_status="processing",
        )

    paypal_dict = {
        "business": "bizaytheeh@gmail.com",
        "amount": cart_total,
        "item_name": "order_item_no-"+str(order.id),
        "invoice": "INVOICE_NO-"+str(order.id),
        "currency_code": "USD",
        "notify_url": request.build_absolute_uri(reverse('core:paypal-ipn')),
        "return": request.build_absolute_uri(reverse('core:payment_completed_view')),
        "cancel_return": request.build_absolute_uri(reverse('core:payment_failed_view')),
        # Custom command to correlate to some function later (optional)
        # "custom": "premium_plan",
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'core/checkout.html', {
        "cart_data": request.session['cart_data_obj'],
        "total_cart_items": len(request.session['cart_data_obj']),
        "cart_total": cart_total,
        "form": form,  # paypal form
    })


def payment_completed_view(request):
    return render(request, 'core/payment_completed.html')


def payment_failed_view(request):
    return render(request, 'core/payment_failed.html')


@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'core/dashboard.html', context)
