from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Electronics","Electronics"), ("Fashion","Fashion"),
        ("Home","Home"), ("Accessories","Accessories")
    ]
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    stock = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = [
        ("Pending","Pending"),("Processing","Processing"),
        ("Shipped","Shipped"),("Delivered","Delivered")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} — {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price
