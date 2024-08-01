from django.core.files.storage import FileSystemStorage
from django.shortcuts import HttpResponse, redirect, render

from segment.models import Branch, Destination

from .forms import BranchForm

# Create your views here.


def index(request):
    return render(request, "fixed-index.html")


def branch(request):
    branch_queryset = (
        Branch.objects.all()
        .select_related("destination")
        .prefetch_related("branchstaff_set__staff")
    )
    active = 0
    inactive = 0
    branch_data = []
    for branch in branch_queryset:
        branch_manager = branch.branchstaff_set.filter(
            staff__role="Branch Manager"
        ).first()
        branch_data.append({"data": branch, "manager": branch_manager})
        if branch.status == "Active":
            active += 1
        else:
            inactive += 1

    return render(
        request,
        "branch.html",
        {
            "branches": branch_data,
            "active_counter": active,
            "inactive_counter": inactive,
        },
    )


def crud_branch(request):
    destination_queryset = Destination.objects.all()
    if request.method == "POST":
        form = BranchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('success_url')  # Redirect after successful save
            print("saved")
            form = BranchForm()
            return redirect("branch")  # Redirect after successful save

    else:
        form = BranchForm()

    return render(
        request,
        "add-edit-branch.html",
        {"form": form, "destinations": destination_queryset},
    )


def edit_branch(request, id):
    destination_queryset = Destination.objects.all()
    # Retrieve the branch to be edited
    branch = Branch.objects.filter(pk=id).first()

    if request.method == "POST":
        # Bind the form to the POST data and files
        form = BranchForm(request.POST, request.FILES, instance=branch)
        if form.is_valid():
            form.save()
            return redirect("branch")  # Redirect after successful save
    else:
        # Create a form instance with the existing branch data
        form = BranchForm(instance=branch)

    return render(
        request,
        "add-edit-branch.html",
        {"form": form, "destinations": destination_queryset},
    )


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
