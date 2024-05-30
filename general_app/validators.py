from django.core.exceptions import ValidationError


def image_max_size(file):
    max_size = 2  # Maximum file size in MB
    if file.size > max_size * 1024:
        raise ValidationError("Images cannot be larger than 2 MB")
