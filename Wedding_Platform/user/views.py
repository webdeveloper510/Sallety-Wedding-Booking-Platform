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
from .models import *
from .models import BookingType, Booking
from .forms import BookingForm
from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import VisitRequestForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator



def index(request):
    # Get active venues from the database
    venues = Venue.objects.filter(status='active')
    context = {
        'venues': venues
    }
    return render(request, 'new-index.html', context)


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
    if request.user.is_staff:
        venue_list = Venue.objects.all().order_by('-created_at')
    else:
        venue_list = Venue.objects.filter(user_id=request.user).order_by('-created_at')

    # Set up pagination: 10 venues per page
    paginator = Paginator(venue_list, 5)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, 'VenuList.html', {'venues': venues})

def venue(request):
    return render(request, 'single-venue.html')

def contact(request):
    return render(request, 'contact.html')

def venue_list(request):
    venues = Venue.objects.all().order_by('-id')  
    return render(request, 'VenueList.html', {
        'venues': venues
    })
# def VisitRequest(request):
#     return render(request, 'VisitRequest.html')


# def table_booking(request):
#     return render(request, 'TableBooking.html')

def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    # Get related images for this venue
    venue_images = venue.images.all()
    context = {
        'venue': venue,
        'venue_images': venue_images,
        'venue_id': venue_id
    }
    return render(request, 'single-venue-detail.html', context)
# def booking(request):
#     return render(request, 'Booking.html')
def booking(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)  # optional but useful
    return render(request, 'Booking.html', {
        'venue': venue,
        'venue_id': venue_id
    })


def contact(request):
    return render(request, 'contact.html')


def user_register(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(name=name).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(name=name, email=email, password=password, role=role)
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


###########################Booking################################################
def booking(request, venue_id):
    booking_types = BookingType.objects.all()

    if not booking_types.exists():
        BookingType.objects.create(name="Lunch", price=500)
        BookingType.objects.create(name="Coffee", price=200)
        BookingType.objects.create(name="Dinner", price=700)
        BookingType.objects.create(name="Coffee + Dinner", price=900)
        booking_types = BookingType.objects.all()
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            selected_types = request.POST.getlist('booking_types')
            
            if not selected_types:
                messages.error(request, "Please select at least one booking type.")
                return render(request, 'Booking.html', {
                    'form': form,
                    'booking_types': booking_types,
                    'venue_id': venue_id,
                })
            
            total_price = 0
            for type_id in selected_types:
                booking_type = BookingType.objects.get(id=type_id)
                total_price += booking_type.price

            booking.total_price = total_price
            booking.venue_id = venue_id

            if request.user.is_authenticated:
                booking.user = request.user
            
            booking.save()

            for type_id in selected_types:
                booking.types.add(BookingType.objects.get(id=type_id))

            messages.success(request, "Booking confirmed successfully!")
            form = BookingForm(initial={'venue_id': venue_id})
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(initial={'venue_id': venue_id})
    
    # ✅ Fetch bookings
    bookings = Booking.objects.filter(venue_id=venue_id)

    return render(request, 'Booking.html', {
        'form': form,
        'booking_types': booking_types,
        'venue_id': venue_id,
        'bookings': bookings  # ✅ Pass this to the template
    })
# class VisitRequestView(View):
#     def get(self, request):
#         form = VisitRequestForm()
#         return render(request, 'visit_request.html', {'form': form})
    
#     def post(self, request):
#         form = VisitRequestForm(request.POST)
#         print("form------------------",form)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your visit request has been submitted successfully!")
#             return redirect('visit_request')
#         else:
#             print("Form errors:", form.errors)  # ✅ debug
#         return render(request, 'visit_request.html', {'form': form})



###########################Visite Request ################################################
def visit_request_view(request):
    if request.method == 'POST':
        # print(request.user, "herere")
        
        add_visit = VisitRequest.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            visit_date=request.POST.get('visit_date'),
            venue_id=request.POST.get('venue_id'),
            time_slot=request.POST.get('time_slot'),
        )
        add_visit.save()
        messages.success(request, 'Thank you! Your visit request has been submitted.')

    visit_requests = VisitRequest.objects.all().order_by('-created_at')  # fetch all requests
    return render(request, 'VisitRequest.html', {'visit_requests': visit_requests})


        # return redirect('visit_request')

# class VenueDetailView(DetailView):
    model = Venue
    template_name = 'venue_detail.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(f"ID from path: {pk}")
        return super().get(request, *args, **kwargs)


###########################Update visite status################################################
@csrf_exempt
def update_visit_status(request, visit_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')

            visit = VisitRequest.objects.get(id=visit_id)
            visit.status = new_status
            visit.save()

            return JsonResponse({'success': True})
        except VisitRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Visit not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


###########################Update venue status################################################

@csrf_exempt
def update_venue_status(request, venue_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_status = data.get('status')
        try:
            venue = Venue.objects.get(id=venue_id)
            venue.status = new_status
            venue.save()
            return JsonResponse({'message': 'Status updated successfully'})
        except Venue.DoesNotExist:
            return JsonResponse({'error': 'Venue not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


###########################Tabel booking list################################################
def table_booking(request):
    bookings = Booking.objects.all()
    return render(request, 'TableBooking.html', {'bookings': bookings})



###########################Updatebooking status################################################
@csrf_exempt
def update_booking_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        booking_id = data.get("booking_id")
        new_status = data.get("status")

        try:
            booking = Booking.objects.get(id=booking_id)
            booking.status = new_status
            booking.save()
            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Booking not found"})

    return JsonResponse({"success": False, "error": "Invalid request method"})