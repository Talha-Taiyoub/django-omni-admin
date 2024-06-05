from django.dispatch import receiver
from djoser.signals import user_activated

from account.views import CustomUserViewSet


@receiver(user_activated, sender=CustomUserViewSet)
def create_guest_for_new_user(sender, **kwargs):
    print("I'm receiving the Signal")
    print(kwargs["user"].email)
