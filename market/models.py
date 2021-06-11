from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

DIV_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Chattogram', 'Chattogram'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Mymensingh', 'Mymensingh'),
    ('Rangpur', 'Rangpur'),
    ('Barisal', 'Barisal'),
    ('Sylhet', 'Sylhet'),
)

CATEGORY_CHOICES = (
    ('Electronics', 'Electronics'),
    ('Food & Bevarage', 'Food & Bevarage'),
    ('Furniture', 'Furniture'),
    ('Stationary', 'Stationary'),
    ('Decoration', 'Decoration'),
    ('Clothes', 'Clothes'),
    ('Accessories', 'Accessories'),
)

STATUS_CHOICES = (
    ('Accepted', 'Accepted',),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Order cancelled', 'Order cancelled'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=DIV_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20,
        default='Pending',
    )
