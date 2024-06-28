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
