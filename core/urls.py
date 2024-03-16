from django.urls import path
from .import views
app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.products_list_view, name='products-list'),
    path('products/detail/<pid>/',views.products_detail_view, name='product-details'),
    path('categories/',views.all_categories, name='all-categories'),
    path('category/<cid>/',views.products_in_category_view, name='category-details'),
]
