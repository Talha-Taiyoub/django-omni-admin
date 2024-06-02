from django.shortcuts import HttpResponse, render

# Create your views here.


def index(request):
    return render(request, "fixed-index.html")


def branch(request):
    return render(request, "branch.html")


def crud_branch(request):
    return render(request, "add-edit-branch.html")


def booking(request):
    return render(request, "booking.html")


def crud_booking(request):
    return render(request, "add-edit-booking.html")


def rooms(request):
    return render(request, "rooms.html")


def crud_room(request):
    return render(request, "add-room.html")


def room_categories(request):
    return render(request, "room-categories.html")


def crud_room_categories(request):
    return render(request, "crud-room-categories.html")


def guests(request):
    return render(request, "guests.html")


def crud_guests(request):
    return render(request, "add-guests.html")


def expected_guests(request):
    return render(request, "expected-guests.html")


def departing_guests(request):
    return render(request, "departing-guests.html")


def inhouse_guests(request):
    return render(request, "inhouse-guests.html")


def restaurants(request):
    return render(request, "restaurants.html")


def crud_restaurants(request):
    return render(request, "add-restaurants.html")


def restaurant_booking(request):
    return render(request, "restaurant-booking.html")


def crud_restaurant_booking(request):
    return render(request, "add-restaurant-booking.html")


def gym(request):
    return render(request, "gym.html")


def crud_gym(request):
    return render(request, "add-gym.html")


def gym_members(request):
    return render(request, "gym-members.html")


def crud_gym_members(request):
    return render(request, "add-gym-members.html")


def gym_membership_request(request):
    return render(request, "gym-membership-request.html")


def sys_users(request):
    return render(request, "users.html")


def crud_sys_users(request):
    return render(request, "add-user.html")


def login(request):
    return render(request, "login.html")


def cms_sliders(request):
    return render(request, "sliders.html")


def crud_cms_sliders(request):
    return render(request, "edit-slider.html")


def cms_attractions(request):
    return render(request, "nearby-attractions.html")


def crud_cms_attraction(request):
    return render(request, "edit-nearby-attraction.html")


def lead_dashboard(request):
    return render(request, "lead-dashboard.html")


from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.utils import decode_uid

# Writing views to override methods of Djoser's views
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.data["email"])
        except User.DoesNotExist:
            return Response(
                {"message": "No account found with this email."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user:
            context = {"user": user}
            to = [user.email]
            settings.EMAIL.password_reset(self.request, context).send(to)
            return Response(
                {
                    "message": "An email has been sent to your email address. Check the spam folder if necessary"
                },
                status=status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):

        if request.data["new_password"] != request.data["re_new_password"]:
            return Response(
                {"message": "Passwords should match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(serializer.data["new_password"])
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": serializer.user}
            to = [get_user_email(serializer.user)]
            settings.EMAIL.password_changed_confirmation(self.request, context).send(to)
        return Response(
            {"message": "Password has been changed successfully."},
            status=status.HTTP_200_OK,
        )
