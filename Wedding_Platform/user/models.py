from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name='Admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, password=password, name=name, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('customer', 'Customer'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('banned', 'Banned'),
    ]

    name = models.CharField(max_length=255 )
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"



# ############################Add Venue########################################
class Venue(models.Model):
    CHAMBERMARIE_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )

    REGION_CHOICES = (
       
        ('Connecticut1', 'Connecticut1'),
        ('New York', 'New York'),
        ('Los Angeles', 'Los Angeles'),
        ('California', 'California'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('rejected', 'Rejected'),
    )

    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='venues',null=True, blank=True)

    # Basic Information
    name = models.CharField(max_length=255,null=True, blank=True)
    description = models.TextField()
    chambermarie = models.CharField(max_length=3, choices=CHAMBERMARIE_CHOICES, default='no')
    chambermarie_image = models.ImageField(upload_to='venues/chambermarie/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.CharField(max_length=20,null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True) 

    # Categories
    is_beach = models.BooleanField(default=False)
    is_city = models.BooleanField(default=False)
    is_hotel = models.BooleanField(default=False)
    is_countryside = models.BooleanField(default=False)
    is_mountain = models.BooleanField(default=False)
    is_resort = models.BooleanField(default=False)
    is_forest = models.BooleanField(default=False)
    is_rooftop = models.BooleanField(default=False)
    is_garden = models.BooleanField(default=False)
    is_desert = models.BooleanField(default=False)
    is_lake = models.BooleanField(default=False)
    is_island = models.BooleanField(default=False)
    is_cave = models.BooleanField(default=False)
    is_vineyard = models.BooleanField(default=False)



    # Gallery
    thumbnail = models.ImageField(upload_to='venues/thumbnails/')

    # Location
    full_address = models.CharField(max_length=255,null=True, blank=True)
    region = models.CharField(max_length=100, choices=REGION_CHOICES,null=True, blank=True)
    longitude = models.CharField(max_length=50,null=True, blank=True)
    latitude = models.CharField(max_length=50,null=True, blank=True)

    # Amenities
    has_parking = models.BooleanField(default=False)
    has_prayer_rooms = models.BooleanField(default=False)
    has_dj = models.BooleanField(default=False)
    has_photographer = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)

    # Additional fields
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active',null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class VenueImage(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='images',null=True, blank=True)
    image = models.ImageField(upload_to='venue_gallery/',null=True, blank=True)


    def __str__(self):
        return f"Image for {self.venue.name}"


# ############################Booking########################################

class BookingType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (${self.price})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    booking_date = models.DateField()
    guests = models.IntegerField()
    venue_id = models.IntegerField(default=1)
    types = models.ManyToManyField(BookingType)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Booking by {self.name} on {self.booking_date}"

    def get_booking_types_display(self):
        types = list(self.types.all())
        if len(types) == 2:
            return f"{types[0].name} + {types[1].name}"
        return ", ".join([t.name for t in types])

class VisitRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    visit_date = models.DateField()
    venue_id = models.IntegerField(default=1)
    time_slot = models.CharField(
        max_length=50,
        choices=[
            ('Morning (9 AM - 12 PM)', 'Morning (9 AM - 12 PM)'),
            ('Afternoon (12 PM - 3 PM)', 'Afternoon (12 PM - 3 PM)'),
            ('Evening (3 PM - 6 PM)', 'Evening (3 PM - 6 PM)'),
        ]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.visit_date}"

