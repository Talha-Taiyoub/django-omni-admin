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


ACTIVE = "Active"
DRAFT = "Draft"
COMING_SOON = "Coming Soon"
BRANCH_STATUS = [(ACTIVE, "Active"), (DRAFT, "Draft"), (COMING_SOON, "Coming Soon")]


class Branch(models.Model):
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


class BranchManager(models.Model):
    pass
