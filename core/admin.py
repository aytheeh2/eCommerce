from django.contrib import admin

# Register your models here.

# begin imports
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, WishList, Address, Contact


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'category', 'featured',
                    'price', 'featured', 'product_status', 'pid']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']


class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status']
    list_display = ['user', 'price', 'paid_status',
                    'order_date', 'product_status']


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'qty', 'price', 'total']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']


class AddressAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['user', 'address', 'status']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'status']
    list_editable = ['status']


# beging reg
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(WishList, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Contact, ContactAdmin)
