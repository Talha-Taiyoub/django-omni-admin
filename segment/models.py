from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from general_app.validators import image_max_size


class Destination(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


ACTIVE = "A"
DRAFT = "D"
COMING_SOON = "C"
BRANCH_STATUS = [(ACTIVE, "Active"), (DRAFT, "Draft"), (COMING_SOON, "Coming Soon")]


# branch manager will be a user_id,later it will be added
class Branch(models.Model):
    name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT)
    initial = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r"^[A-Z0-9]{1,7}$",
                message="Initials must be 1-7 characters long and contain only uppercase letters and numbers.",
            )
        ],
    )
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=BRANCH_STATUS, default=COMING_SOON)
    logo = models.ImageField(upload_to="segment/images", validators=[image_max_size])
    overview = models.TextField()
    email = models.EmailField(unique=True)
    telephone = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                # ensures that the phone number starts with either a plus sign or a digit, and the rest of the characters are digits
                regex=r"^[+\d][\d]+$",
                message="Enter a valid telephone number.",
            )
        ],
    )
    mobile = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                # ensures that the mobile number either starts with "+88" followed by "0" and then 10 digits or starts with "0" followed by 10 digits.
                regex=r"^\+880?\d{10}$|^0\d{10}$",
                message="Enter a valid Bangladeshi mobile number.",
            )
        ],
    )
    location_iframe = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Slider(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="sliders")
    image = models.ImageField(upload_to="segment/images", validators=[image_max_size])
