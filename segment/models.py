from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from general_app.validators import image_max_size


class Destination(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(
        upload_to="segment/images", validators=[image_max_size], null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


ACTIVE = "A"
DRAFT = "D"
COMING_SOON = "C"
BRANCH_STATUS = [(ACTIVE, "Active"), (DRAFT, "Draft"), (COMING_SOON, "Coming Soon")]


class Branch(models.Model):
    name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, null=True, blank=True)
    destination = models.ForeignKey(
        Destination, on_delete=models.PROTECT, related_name="branches"
    )
    initial = models.CharField(max_length=7)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=BRANCH_STATUS, default=COMING_SOON)
    logo = models.ImageField(upload_to="segment/images", validators=[image_max_size])
    overview = models.TextField()
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=14)
    mobile = models.CharField(max_length=14)
    location_iframe = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Slider(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="sliders")
    image = models.ImageField(upload_to="segment/images", validators=[image_max_size])


class BranchManager(models.Model):
    pass
