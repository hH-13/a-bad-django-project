import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]


class Item(models.Model):
    type = models.ForeignKey(Type, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True, default="")
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def topup(self):
        self.stock += 50
        self.save()

    class Meta:
        ordering = ["id"]


class Client(User):
    CITY_CHOICES = [
        ("WD", "Windsor"),
        ("TO", "Toronto"),
        ("CH", "Chatham"),
        ("WL", "WATERLOO"),
    ]

    # fullname = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default="CH")
    interested_in = models.ManyToManyField(Type)
    mobile = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ["id"]


class OrderItem(models.Model):
    STATUS_CHOICES = [
        (0, "Cancelled"),
        (1, "Placed"),
        (2, "Shipped"),
        (3, "Delivered"),
    ]
    item = models.ForeignKey(Item, related_name="order_items", on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    last_updated = models.DateField(default=timezone.now)

    def __str__(self):
        return f" {self.item.name} by  {self.client.get_full_name()} {self.quantity} units where status is {self.get_status_display()}"

    def total_price(self):
        return self.quantity * self.item.price


class made_by(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    student_id = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ["id"]
