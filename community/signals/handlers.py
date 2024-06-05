from django.dispatch import receiver
from djoser.signals import user_activated

from account.views import CustomUserViewSet
from community.models import Guest


@receiver(user_activated, sender=CustomUserViewSet)
def create_guest_for_new_user(sender, **kwargs):
    user = kwargs["user"]
    if not Guest.objects.filter(user=user).exists():
        Guest.objects.create(user=user)
