from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import VenueForm, VenueImageFormSet
from .models import Venue, User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Venue, VenueImage, User
from .models import BookingType, Booking
from .forms import BookingForm


def index(request):
    return render(request, 'new-index.html')


@login_required
def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        
        if form.is_valid():
            venue = form.save(commit=False)
            
            # ✅ Assign user correctly
            venue.user = request.user
            venue.status = 'Active'
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
                    
            messages.success(request, 'Venue added successfully! It will be reviewed by an administrator.')
            return redirect('venue-list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VenueForm()
    
    return render(request, 'addVenue.html', {
        'form': form,
    })


@login_required
def VenueList(request):
    # Show all venues for admins, but only user's own venues for regular users
    if request.user.is_staff:
        venues = Venue.objects.all().order_by('-created_at')
    else:
        venues = Venue.objects.filter(user_id=request.user).order_by('-created_at')
    
    return render(request, 'VenuList.html', {'venues': venues})


def venue(request):
    return render(request, 'single-venue.html')

def contact(request):
    return render(request, 'contact.html')

def venue_list(request):
    venues = Venue.objects.all().order_by('-id')  # Show latest first, optional
    return render(request, 'VenueList.html', {
        'venues': venues
    })

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



def user_register(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(name=name).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(name=name, email=email, password=password)
            messages.success(request, "Account created successfully!")
            return redirect('user-login')

    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        # Authenticate using email (USERNAME_FIELD)
        user = authenticate(request, username=username_or_email, password=password)

        # Try with name if the first attempt fails
        if user is None:
            try:
                user_obj = User.objects.get(name=username_or_email)
                user = authenticate(request, username=user_obj.email, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

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



def booking(request):
    # Get all booking types to display on the form
    booking_types = BookingType.objects.all()
    
    # If there are no booking types in the database, create default ones
    if not booking_types.exists():
        BookingType.objects.create(name="Lunch", price=500)
        BookingType.objects.create(name="Coffee", price=200)
        BookingType.objects.create(name="Dinner", price=700)
        BookingType.objects.create(name="Coffee + Dinner", price=900)
        booking_types = BookingType.objects.all()
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if form.is_valid():
            # Create booking without saving to DB yet
            booking = form.save(commit=False)
            
            # Get selected booking types
            selected_types = request.POST.getlist('booking_types')
            
            if not selected_types:
                messages.error(request, "Please select at least one booking type.")
                return render(request, 'Booking.html', {'form': form, 'booking_types': booking_types})
            
            # Calculate total price
            total_price = 0
            for type_id in selected_types:
                booking_type = BookingType.objects.get(id=type_id)
                total_price += booking_type.price
            
            booking.total_price = total_price
            booking.save()
            
            # Add the selected booking types
            for type_id in selected_types:
                booking.types.add(BookingType.objects.get(id=type_id))
            
            messages.success(request, "Booking confirmed successfully!")
            return redirect('booking')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()
    
    return render(request, 'Booking.html', {'form': form, 'booking_types': booking_types})