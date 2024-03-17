from django.urls import path
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

]
