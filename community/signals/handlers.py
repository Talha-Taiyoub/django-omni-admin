from django.conf import settings
from django.dispatch import receiver
from djoser.signals import user_activated


@receiver(user_activated, sender=settings.AUTH_USER_MODEL)
def create_guest_for_new_user(sender, **kwargs):
    print("I'm receiving the Signal")
