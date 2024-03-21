from django.urls import include, path
from .import views
app_name = 'core'

urlpatterns = [
    # home
    path('', views.home_view, name='home'),
    # all products
    path('products/', views.products_list_view, name='products-list'),
    # product details
    path('products/detail/<pid>/',
         views.products_detail_view, name='product-details'),
    # all categories
    path('categories/', views.all_categories, name='all-categories'),
    # products category details
    path('category/<cid>/', views.products_in_category_view,
         name='category-details'),
    #  vendors
    path('vendors/', views.all_vendors, name='all-vendors'),
    path('vendor/<vid>/', views.vendor_details, name='vendor-details'),
    path('vendor/<vid>/shop/', views.vendor_shop, name='vendor-shop'),

    # Tags
    path('tags/<tag>/', views.tags, name='tags'),

    # Product Review AJAX
    path('ajax-add-review/<pid>/', views.ajax_addreview, name='ajax-add-review'),


    # product ajax filtering
    path('filter-products/', views.filter_product, name='filter-product'),

    # add to cart ajax
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    # cart
    path('cart/', views.cart_view, name='cart-view'),

    # delete from cart
    path('delete-from-cart/', views.delete_from_cart, name='delete-from-cart'),

    # update items in cart by pressing the button refresh
    path('update-items-in-cart/', views.update_items_in_cart,
         name='update-items-in-cart'),


    # checkout
    path('checkout/', views.checkout, name='checkout'),

    # paypal
    path('paypal/', include("paypal.standard.ipn.urls"), name='paypal-ipn'),

    # payment success
    path('payment-success/', views.payment_completed_view,
         name='payment_completed_view'),

    # payment failed
    path('payment-failed/', views.payment_failed_view,
         name='payment_failed_view'),

    # dashboard
    path('dashboard/', views.customer_dashboard,
         name='dashboard'),

    # order details by id
    path('order/<int:id>/', views.order_details,
         name='order-details'),

    path('make-address-default/', views.make_address_default,
         name="make_address_default"),
]
