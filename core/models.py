from django.db import models
from userauth.models import User
# pip install django-shortuuidfield
from shortuuid.django_fields import ShortUUIDField

# pip install django-taggit
from taggit.managers import TaggableManager

from django.utils.html import mark_safe


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20,
                         prefix='cat', alphabet='abcdefgh12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Category', default='category.jpg')

    class Meta:
        verbose_name_plural = "Categories"

    # def category_image(self):
    #     return mark_safe('<img src="%s" width="50%" />' & (self.image.url))

    def category_image(self):
        return mark_safe('<img src="%s" width="50%%" />' % self.image.url)

    def __str__(self):
        return self.title


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20,
                         prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default='DefaultVendorName')
    image = models.ImageField(
        upload_to=user_directory_path, default='category.jpg')
    description = models.TextField(
        null=True, blank=True, default="This is the product description.")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, default="123 Main St")
    contact = models.CharField(max_length=100, default="+91 999000")
    chat_response_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warrenty_period = models.CharField(max_length=100, default="100")

    class Meta:
        verbose_name_plural = "Vendors"

    # def vendor_image(self):
    #     return mark_safe('<img src="%s" width="50%" />' & (self.image.url))

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50%%" />' % self.image.url)

    def __str__(self):
        return self.title


class Tags(models.Model):
    pass


STATUS_CHOICES = (
    ('processing', "Processing"),
    ('shipped', "Shipped"),
    ('delivered', "Delivered"),
)

STATUS = (
    ('draft', "Draft"),
    ('disabled', "Disabled"),
    ('rejected', "Rejected"),
    ('in_review', "In Review"),
    ('published', "Published"),
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10,
                         max_length=20, alphabet='abcdefgh12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(
        null=True, blank=True, default="This is the product description.")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(
        max_digits=9999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(
        max_digits=9999999, decimal_places=2, default="2.99")
    specifications = models.TextField(null=True, blank=True)

    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    tags = TaggableManager(blank=True)

    product_status = models.CharField(
        choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=4,
                         max_length=10, alphabet='1234567890')
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    # def product_image(self):
    #     return mark_safe('<img src="%s" width="50%" />' & (self.image.url))
    def product_image(self):
        return mark_safe('<img src="%s" width="50%%" />' % self.image.url)

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(
        upload_to='product-images', default='product.jpg')
    product = models.ForeignKey(
        Product, related_name='p_images', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product_Images"


#######################################


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='processing')

    class Meta:
        verbose_name_plural = "Cart Orders"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    image = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=9999999, decimal_places=2, default="1.99")
    total = models.DecimalField(
        max_digits=9999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50%" />' & (self.image))


# Product review, wishlist ,address
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "WishLists"

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=10, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"


Contact_Status = (
    ('pending', "PENDING"),
    ('processing', "PROCESSING"),
    ('solved', "SOLVED"),
)


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email=models.EmailField()
    message = models.CharField(max_length=200)
    status = models.CharField(choices=Contact_Status,
                              max_length=10, default='pending')

    class Meta:
        verbose_name_plural = 'Contact'

    def __str__(self):
        return f'{self.name} : {self.status}'
