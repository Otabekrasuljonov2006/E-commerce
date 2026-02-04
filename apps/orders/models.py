from django.db import models
from django.contrib.auth.models import User
from apps.carts.models import *
from apps.products.models import *

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.user.username} order"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
