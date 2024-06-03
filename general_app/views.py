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
