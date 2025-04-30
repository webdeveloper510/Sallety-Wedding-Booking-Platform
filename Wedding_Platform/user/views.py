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
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from datetime import datetime

# Custom decorator for owner-only access
def owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ['owner', 'admin']:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('index')
    return wrapper

#####################index#####################
def index(request):
    # Get active venues from the database
    venues = Venue.objects.filter(status='active').order_by('created_at')
   # Get search parameters
    region = request.GET.get('destination')
    date = request.GET.get('date')
    capacity = request.GET.get('guests')
    
    # Apply region filter
    if region:
        venues = venues.filter(region__icontains=region)
    
    # Apply capacity filter
    if capacity:
        try:
            capacity = int(capacity)
            venues = venues.filter(capacity__gte=capacity)  # Greater than or equal to
        except ValueError:
            pass  # Invalid capacity input
    
    # Apply date filter - check if venues are available on that date
    if date:
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # With your existing model, we need to filter by venue_id
            booked_venue_ids = Booking.objects.filter(
                booking_date=search_date,
                status='confirmed'  # Only consider confirmed bookings as blocking availability
            ).values_list('venue_id', flat=True).distinct()
            
            # Exclude venues that have bookings on the selected date
            venues = venues.exclude(id__in=booked_venue_ids)
        except ValueError:
            pass  # Invalid date format
    
    # Check if category filter is provided (keep your existing code)
    category = request.GET.get('category')
    if category:
        # Map category name to model field
        category_mapping = {
            'beach': 'is_beach',
            'city': 'is_city',
            'hotel': 'is_hotel',
            'countryside': 'is_countryside',
            'mountain': 'is_mountain',
            'resort': 'is_resort',
            'forest': 'is_forest',
            'rooftop': 'is_rooftop',
            'garden': 'is_garden',
            'desert': 'is_desert',
            'lake': 'is_lake',
            'island': 'is_island',
            'cave': 'is_cave',
            'vineyard': 'is_vineyard',
        }

        if category.lower() in category_mapping:
            filter_kwargs = {category_mapping[category.lower()]: True}
            venues = venues.filter(**filter_kwargs).order_by('-created_at')
    
    context = {
        'venues': venues.order_by('-created_at'),
        'active_category': category,
        # Add search parameters to context to maintain form state
        'search_region': region,
        'search_date': date,
        'search_capacity': capacity
    }
    return render(request, 'new-index.html', context)

@login_required
def logout_user(request):
    logout(request)
    return redirect('index')

#####################add venue#############################
@login_required
@owner_required  # Only owners can add venues
def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        
        if form.is_valid():
            venue = form.save(commit=False)
            
            # Assign user correctly
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
                # Limit to 4 images
                for image in gallery_images[:4]:
                    VenueImage.objects.create(venue=venue, image=image)
                    
            messages.success(request, 'Venue added successfully! It will be reviewed by an administrator.')
            return redirect('venue-list')
        else:
            # Enhanced error handling
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = VenueForm()
    
    return render(request, 'addVenue.html', {
        'form': form,
    })

#venue list
@login_required
def VenueList(request):
    print("checking",request.user.role)
    if request.user.role != 'owner':
        venue_list = Venue.objects.all().order_by('-created_at')
    else:
        venue_list = Venue.objects.filter(user_id=request.user).order_by('-created_at')

    # Set up pagination: 10 venues per page
    paginator = Paginator(venue_list, 5)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, 'VenuList.html', {'venues': venues})

def venue(request):
    venue_id = request.GET.get('id')
    if venue_id:
        try:
            venue = Venue.objects.get(id=venue_id, status='active')
            context = {'venue': venue}
            return render(request, 'single-venue.html', context)
        except Venue.DoesNotExist:
            messages.error(request, "Venue not found or not active.")
            return redirect('index')
    else:
        # Handle case where no ID is provided
        return redirect('index')

def contact(request):
    return render(request, 'contact.html')

@login_required
def venue_list(request):
    print("jjjjjjj",request.user.role)
    if request.user.role != 'owner':
        venues = Venue.objects.all().order_by('-created_at')
    else:
        venues = Venue.objects.filter(user_id=request.user).order_by('-created_at')
    
    return render(request, 'VenueList.html', {
        'venues': venues
    })

######################venue detail###################################
@login_required
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

#######################bookign##############################
def booking(request, venue_id):
    print("Venue name:")
    venue = get_object_or_404(Venue, id=venue_id)  # optional but useful
   
   
    return render(request, 'Booking.html', {
        'venue': venue,
        'venue_id': venue_id
    })

#####################contact#############
def contact(request):
    return render(request, 'contact.html')


#########################register########################
def user_register(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role", "user")

        if User.objects.filter(name=name).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user = User.objects.create_user(name=name, email=email, password=password, role=role)
            messages.success(request, "Account created successfully!")
            # No redirect — show toast, then redirect via JavaScript
            return render(request, 'register.html')

    return render(request, 'register.html')


#######################3login#############################
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

###########################Booking################################################
@login_required
def booking(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
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
            
            # Check if any of the selected booking types are already booked for this date
            booking_date = form.cleaned_data['booking_date']
            existing_bookings = Booking.objects.filter(
                venue=venue,
                booking_date=booking_date,
                status__in=['confirmed', 'pending']
            )
            
            unavailable_types = []
            for existing in existing_bookings:
                for booked_type in existing.types.all():
                    if str(booked_type.id) in selected_types:
                        unavailable_types.append(booked_type.name)
            
            if unavailable_types:
                messages.error(request, f"The following booking types are no longer available for this date: {', '.join(unavailable_types)}. Please refresh and try again.")
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
            booking.venue = venue 
            print(booking.venue_id,"kuch vi")

            if request.user.is_authenticated:
                booking.user = request.user
            
            booking.save()

            for type_id in selected_types:
                booking.types.add(BookingType.objects.get(id=type_id))

            messages.success(request, "Booking confirmed successfully!")
            return redirect('booking', venue_id=venue_id)  # Redirect to clear the form
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(initial={'venue_id': venue_id})
    
    # Fetch all bookings for this venue
    bookings = Booking.objects.filter(
        venue=venue,
        status__in=['confirmed', 'pending']
    )
    
    # Prepare booking data for JavaScript
    bookings_data = []
    for booking in bookings:
        booking_types_ids = [bt.id for bt in booking.types.all()]
        bookings_data.append({
            'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
            'venue_id': booking.venue_id,
            'booking_types': booking_types_ids
        })
    
    # Convert to JSON for template
    bookings_json = json.dumps(bookings_data)

    return render(request, 'Booking.html', {
        'form': form,
        'booking_types': booking_types,
        'venue_id': venue_id,
        'venue': venue, 
        'bookings': bookings,
        'bookings_json': bookings_json  # Pass JSON data to template
    })

###########################Visite Request ################################################
@login_required
def visit_request_view(request):
    if request.method == 'POST':
        try:
            venue_id = request.POST.get('venue_id')
            venue = Venue.objects.get(id=venue_id)
            # Create the visit request
            add_visit = VisitRequest.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                visit_date=request.POST.get('visit_date'),
                venue=venue,
                time_slot=request.POST.get('time_slot'),
                user=request.user,  # Associate the visit request with the current user
            )
            add_visit.save()
            
            # Check if AJAX request
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if is_ajax:
                # Return JSON response for AJAX requests
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you! Your visit request has been submitted.'
                })
            else:
                # For regular form submissions, add a message and continue to render
                messages.success(request, 'Thank you! Your visit request has been submitted.')
        
        except Exception as e:
            # Handle errors
            print(f"Error saving visit request: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Error: {str(e)}'
                })
            else:
                messages.error(request, f'Error: {str(e)}')

    # Get visit requests data for the template
    if request.user.role == 'admin':
        # Admins see all visit requests
        visit_requests = VisitRequest.objects.all().order_by('-created_at')
    elif request.user.role == 'owner':
        # Owners see only visit requests for venues they own
        visit_requests = VisitRequest.objects.filter(venue__user=request.user).order_by('-created_at')
    else:
        # Regular users see only their own visit requests
        visit_requests = VisitRequest.objects.filter(user=request.user).order_by('-created_at')
    
    # Only return the template for GET requests or non-AJAX POST requests
    if request.method == 'GET' or request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return render(request, 'VisitRequest.html', {'visit_requests': visit_requests})
    
    # This line should not be reached for AJAX requests since we return above
    return JsonResponse({'success': False, 'message': 'Invalid request'})
###########################Update visite status################################################
@csrf_exempt
@login_required
@owner_required  # Only owners can update visit status
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
@login_required
@owner_required  # Only owners can update venue status
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
@login_required
def table_booking(request):
    if request.user.role == 'owner':
        # Owners see only bookings for venues they own - latest first
        bookings = Booking.objects.select_related('venue').filter(venue__user=request.user).order_by('-created_at')
    else:
        # Regular users see only their own bookings - latest first
        bookings = Booking.objects.select_related('venue').filter(user=request.user).order_by('-created_at')
    
    return render(request, 'TableBooking.html', {'bookings': bookings})
###########################Updatebooking status################################################
@csrf_exempt
@login_required
@owner_required  # Only owners can update booking status
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

###########################Search result################################################
def search_results(request):
    # Get active venues from the database
    venues = Venue.objects.filter(status='active')
    
    # Get search parameters
    region = request.GET.get('destination')
    date = request.GET.get('date')
    capacity = request.GET.get('guests')
    
    # Apply region filter
    if region:
        venues = venues.filter(region__icontains=region)
    
    # Apply capacity filter
    if capacity:
        try:
            capacity = int(capacity)
            venues = venues.filter(capacity__gte=capacity)  # Greater than or equal to
        except ValueError:
            pass  # Invalid capacity input
    
    # Apply date filter - check if venues are available on that date
    if date:
        try:
            from datetime import datetime
            search_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Filter out venues with confirmed bookings on this date
            booked_venue_ids = Booking.objects.filter(
                booking_date=search_date,
                status='confirmed'
            ).values_list('venue_id', flat=True).distinct()
            
            venues = venues.exclude(id__in=booked_venue_ids)
        except ValueError:
            pass  # Invalid date format
    
    # Check if category filter is provided
    category = request.GET.get('category')
    if category:
        # Map category name to model field
        category_mapping = {
            'beach': 'is_beach',
            'city': 'is_city',
            'hotel': 'is_hotel',
            'countryside': 'is_countryside',
            'mountain': 'is_mountain',
            'resort': 'is_resort',
            'forest': 'is_forest',
            'rooftop': 'is_rooftop',
            'garden': 'is_garden',
            'desert': 'is_desert',
            'lake': 'is_lake',
            'island': 'is_island',
            'cave': 'is_cave',
            'vineyard': 'is_vineyard',
        }

        if category.lower() in category_mapping:
            filter_kwargs = {category_mapping[category.lower()]: True}
            venues = venues.filter(**filter_kwargs)
    
    context = {
        'venues': venues,
        'active_category': category,
        'search_region': region,
        'search_date': date,
        'search_capacity': capacity,
        'total_results': venues.count()
    }
    
    # Render using your existing single-venue.html template
    return render(request, 'single-venue.html', context)
    # Get active venues from the database
    venues = Venue.objects.filter(status='active')
    
    # Get search parameters
    region = request.GET.get('destination')
    date = request.GET.get('date')
    capacity = request.GET.get('guests')
    
    # Apply region filter
    if region:
        venues = venues.filter(region__icontains=region)
    
    # Apply capacity filter
    if capacity:
        try:
            capacity = int(capacity)
            venues = venues.filter(capacity__gte=capacity)  # Greater than or equal to
        except ValueError:
            pass  # Invalid capacity input
    
    # Apply date filter - check if venues are available on that date
    if date:
        try:
            from datetime import datetime
            search_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Filter out venues with confirmed bookings on this date
            booked_venue_ids = Booking.objects.filter(
                booking_date=search_date,
                status='confirmed'
            ).values_list('venue_id', flat=True).distinct()
            
            venues = venues.exclude(id__in=booked_venue_ids)
        except ValueError:
            pass  # Invalid date format
    
    # Check if category filter is provided
    category = request.GET.get('category')
    if category:
        # Map category name to model field
        category_mapping = {
            'beach': 'is_beach',
            'city': 'is_city',
            'hotel': 'is_hotel',
            'countryside': 'is_countryside',
            'mountain': 'is_mountain',
            'resort': 'is_resort',
            'forest': 'is_forest',
            'rooftop': 'is_rooftop',
            'garden': 'is_garden',
            'desert': 'is_desert',
            'lake': 'is_lake',
            'island': 'is_island',
            'cave': 'is_cave',
            'vineyard': 'is_vineyard',
        }

        if category.lower() in category_mapping:
            filter_kwargs = {category_mapping[category.lower()]: True}
            venues = venues.filter(**filter_kwargs)
    
    context = {
        'venues': venues,
        'active_category': category,
        'search_region': region,
        'search_date': date,
        'search_capacity': capacity,
        'total_results': venues.count()
    }
    
    # Use an existing template temporarily
    return render(request, 'new-index.html', context)
    # Get active venues from the database
    venues = Venue.objects.filter(status='active')
    
    # Get search parameters
    region = request.GET.get('destination')
    date = request.GET.get('date')
    capacity = request.GET.get('guests')
    
    # Apply region filter
    if region:
        venues = venues.filter(region__icontains=region)
    
    # Apply capacity filter
    if capacity:
        try:
            capacity = int(capacity)
            venues = venues.filter(capacity__gte=capacity)  # Greater than or equal to
        except ValueError:
            pass  # Invalid capacity input
    
    # Apply date filter - check if venues are available on that date
    if date:
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Filter out venues with confirmed bookings on this date
            booked_venue_ids = Booking.objects.filter(
                booking_date=search_date,
                status='confirmed'
            ).values_list('venue_id', flat=True).distinct()
            
            venues = venues.exclude(id__in=booked_venue_ids)
        except ValueError:
            pass  # Invalid date format
    
    # Check if category filter is provided
    category = request.GET.get('category')
    if category:
        # Map category name to model field
        category_mapping = {
            'beach': 'is_beach',
            'city': 'is_city',
            'hotel': 'is_hotel',
            'countryside': 'is_countryside',
            'mountain': 'is_mountain',
            'resort': 'is_resort',
            'forest': 'is_forest',
            'rooftop': 'is_rooftop',
            'garden': 'is_garden',
            'desert': 'is_desert',
            'lake': 'is_lake',
            'island': 'is_island',
            'cave': 'is_cave',
            'vineyard': 'is_vineyard',
        }

        if category.lower() in category_mapping:
            filter_kwargs = {category_mapping[category.lower()]: True}
            venues = venues.filter(**filter_kwargs)
    
    context = {
        'venues': venues,
        'active_category': category,
        'search_region': region,
        'search_date': date,
        'search_capacity': capacity,
        'total_results': venues.count()
    }
    return render(request, 'venue-search-results.html', context)


################################# 1. Create the edit_venue view function########################
@login_required
def edit_venue(request, venue_id):
    # Get the venue or return 404 if not found
    venue = get_object_or_404(Venue, id=venue_id)
    
    # Check if the user is an admin or the owner of the venue
    if not request.user.is_staff and venue.user != request.user:
        messages.error(request, "You don't have permission to edit this venue.")
        return redirect('venue-list')
    
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        
        if form.is_valid():
            venue = form.save(commit=False)
            venue.save()
            
            # Process amenities checkboxes
            venue.has_parking = 'parking' in request.POST.getlist('amenities', [])
            venue.has_prayer_rooms = 'prayer_rooms' in request.POST.getlist('amenities', [])
            venue.has_dj = 'dj' in request.POST.getlist('amenities', [])
            venue.has_photographer = 'photographer' in request.POST.getlist('amenities', [])
            venue.has_wifi = 'wifi' in request.POST.getlist('amenities', [])
            venue.has_swimming_pool = 'swimming_pool' in request.POST.getlist('amenities', [])
            venue.save()
            
            # Handle gallery images
            if 'gallery_images' in request.FILES:
                gallery_images = request.FILES.getlist('gallery_images')
                # Limit to 4 images
                current_images_count = VenueImage.objects.filter(venue=venue).count()
                remaining_slots = 4 - current_images_count
                
                if remaining_slots > 0:
                    for image in gallery_images[:remaining_slots]:
                        VenueImage.objects.create(venue=venue, image=image)
                else:
                    messages.warning(request, 'Maximum of 4 gallery images allowed. No new images were added.')
            
            messages.success(request, 'Venue updated successfully!')
            return redirect('venue-list')
        else:
            # Enhanced error handling
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        # Create the form with the venue instance to pre-fill values
        form = VenueForm(instance=venue)
    
    # Get existing gallery images
    gallery_images = VenueImage.objects.filter(venue=venue)
    
    return render(request, 'addVenue.html', {
        'form': form,
        'venue': venue,
        'gallery_images': gallery_images,
        'is_edit': True
    })