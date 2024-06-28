from django.core.validators import MinValueValidator
from django.db import models

from segment.models import Branch


class Restaurant(models.Model):
    ACTIVE = "Active"
    OUT_OF_ORDER = "Out Of Order"
    RESTAURANT_STATUS = [(ACTIVE, "Active"), (OUT_OF_ORDER, "Out Of order")]

    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=RESTAURANT_STATUS, default=ACTIVE)
    overview = models.TextField()
    featured_image = models.ImageField(upload_to="refuel/images")
    breakfast_opening = models.TimeField()
    breakfast_closing = models.TimeField()
    lunch_opening = models.TimeField()
    lunch_closing = models.TimeField()
    dinner_opening = models.TimeField()
    dinner_closing = models.TimeField()
    discount_in_percentage = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Gallery(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="refuel/images")


class Cuisine(models.Model):
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class RestaurantCuisine(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="cuisines"
    )
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["restaurant", "cuisine"]


class Reservation(models.Model):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    RESERVATION_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    PAYMENT_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (CANCELLED, "Cancelled"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=14)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15, choices=RESERVATION_STATUS_CHOICES, default=PENDING
    )
    number_of_people = models.IntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True
    )
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    # in dashboard we will use this field against reservation description
    additional_information = models.TextField(null=True, blank=True)
    total_bill = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=15, choices=PAYMENT_STATUS_CHOICES, default=PENDING
    )
    placed_at = models.DateTimeField(auto_now_add=True)
