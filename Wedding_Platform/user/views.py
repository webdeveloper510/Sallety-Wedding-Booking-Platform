from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import VenueForm, VenueImageFormSet
from .models import Venue

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    return render(request, 'new-index.html')

# def login(request):  
#     return render(request, 'login.html')

@login_required
def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        formset = VenueImageFormSet(request.POST, request.FILES)
        
        if form.is_valid():
            # Save venue but don't commit to DB yet
            venue = form.save(commit=False)
            venue.created_by = request.user
            venue.save()
            
            # Process amenities checkboxes
            venue.has_parking = 'parking' in request.POST.getlist('amenities', [])
            venue.has_prayer_rooms = 'prayer_rooms' in request.POST.getlist('amenities', [])
            venue.has_dj = 'dj' in request.POST.getlist('amenities', [])
            venue.has_photographer = 'photographer' in request.POST.getlist('amenities', [])
            venue.has_wifi = 'wifi' in request.POST.getlist('amenities', [])
            venue.has_swimming_pool = 'swimming_pool' in request.POST.getlist('amenities', [])
            venue.save()
            
            # Save gallery images
            if 'gallery_images' in request.FILES:
                gallery_images = request.FILES.getlist('gallery_images')
                for image in gallery_images:
                    VenueImage.objects.create(venue=venue, image=image)
                    
            messages.success(request, 'Venue added successfully!')
            return redirect('venue_list')  # Redirect to a venue list page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VenueForm()
        formset = VenueImageFormSet()
    
    return render(request, 'addVenue.html', {
        'form': form,
        'formset': formset,
    })


def venue(request):
    return render(request, 'single-venue.html')

def contact(request):
    return render(request, 'contact.html')

def venue_list(request):
    return render(request, 'VenueList.html')

def visit_request(request):
    return render(request, 'VisitRequest.html')

def table_booking(request):
    return render(request, 'TableBooking.html')

def venue_detail(request):
    return render(request, 'single-venue-detail.html')
def booking(request):
    return render(request, 'Booking.html')
def contact(request):
    return render(request, 'contact.html')


def user_login(request):
    if request.method == "POST":
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        print("Username/Email:", username_or_email)
        print("Password:", password)

        user = authenticate(request, username=username_or_email, password=password)
        print("User from authenticate (username):", user)

        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                print("Found user by email:", user_obj.username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                print("No user found with email:", username_or_email)
                user = None

        print("Final user:", user)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'login.html')

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('user-login')  # Redirect to login page after registration

    return render(request, 'register.html')