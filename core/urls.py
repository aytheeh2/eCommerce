from django.urls import path
from .import views
app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.products_list_view, name='products-list'),
    path('products/detail/<str:pid>',
         views.products_detail_view, name='product-details'),
]
