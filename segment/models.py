from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from community.models import Staff
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


class Branch(models.Model):
    ACTIVE = "Active"
    DRAFT = "Draft"
    COMING_SOON = "Coming Soon"
    BRANCH_STATUS = [(ACTIVE, "Active"), (DRAFT, "Draft"), (COMING_SOON, "Coming Soon")]

    name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, null=True, blank=True)
    destination = models.ForeignKey(
        Destination, on_delete=models.PROTECT, related_name="branches"
    )
    initial = models.CharField(max_length=7)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=BRANCH_STATUS, default=COMING_SOON)
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


class BranchSlider(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="sliders")
    type = models.CharField(
        max_length=15,
        choices=[
            ("Single Video", "Single Video"),
            ("Static Sliders", "Static Sliders"),
        ],
    )
    featured_image = models.ImageField(
        upload_to="segment/images", validators=[image_max_size]
    )
    # video slider
    video_slider_title = models.CharField(max_length=255, null=True, blank=True)
    video_slider_subtitle = models.CharField(max_length=255, null=True, blank=True)
    video_slider_button_one_title = models.CharField(
        max_length=255, null=True, blank=True
    )
    video_slider_button_one_link = models.CharField(
        max_length=255, null=True, blank=True
    )
    video_slider_button_two_title = models.CharField(
        max_length=255, null=True, blank=True
    )
    video_slider_button_two_link = models.CharField(
        max_length=255, null=True, blank=True
    )
    video_slider_youtube_link = models.CharField(max_length=255, null=True, blank=True)
    # static slider one
    static_slider_one_title = models.CharField(max_length=255, null=True, blank=True)
    static_slider_one_subtitle = models.CharField(max_length=255, null=True, blank=True)
    static_slider_one_button_one_title = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_one_button_one_link = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_one_button_two_title = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_one_button_two_link = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_one_image_link = models.ImageField(
        upload_to="segment/images", null=True, blank=True
    )
    # static slider two
    static_slider_two_title = models.CharField(max_length=255, null=True, blank=True)
    static_slider_two_subtitle = models.CharField(max_length=255, null=True, blank=True)
    static_slider_two_button_one_title = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_two_button_one_link = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_two_button_two_title = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_two_button_two_link = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_two_image_link = models.ImageField(
        upload_to="segment/images", null=True, blank=True
    )
    # static slider three
    static_slider_three_title = models.CharField(max_length=255, null=True, blank=True)
    static_slider_three_subtitle = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_three_button_one_title = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_three_button_one_link = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_three_button_two_title = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_three_button_two_link = models.CharField(
        max_length=255, null=True, blank=True
    )
    static_slider_three_image_link = models.ImageField(
        upload_to="segment/images", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class BranchStaff(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("branch", "staff")

    def __str__(self):
        return f"{self.staff.name} at {self.branch.name} as {self.staff.role}"


# amenities will be added later
class RoomCategory(models.Model):
    ACTIVE = "Active"
    OUT_OF_ORDER = "Out Of Order"
    ROOM_STATUS = [(ACTIVE, "Active"), (OUT_OF_ORDER, "Out Of order")]

    room_name = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=ROOM_STATUS, default=OUT_OF_ORDER)
    featured_image = models.ImageField(upload_to="segment/images")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    overview = models.TextField()
    panorama = models.ImageField(upload_to="segment/images")
    adults = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    children = models.PositiveSmallIntegerField()
    regular_price = models.DecimalField(max_digits=9, decimal_places=2)
    discount_in_percentage = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Gallery(models.Model):
    room_category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="segment/images")


class Amenities(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
