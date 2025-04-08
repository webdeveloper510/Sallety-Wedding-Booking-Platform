# models.py
from django.db import models
from django.contrib.auth.models import User

class Venue(models.Model):
    CHAMBERMARIE_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    
    REGION_CHOICES = (
        ('Connecticut', 'Connecticut'),
        ('New York', 'New York'),
        ('Los Angeles', 'Los Angeles'),
        ('California', 'California'),
    )
    
    # Basic Information
    name = models.CharField(max_length=255)
    description = models.TextField()
    chambermarie = models.CharField(max_length=3, choices=CHAMBERMARIE_CHOICES, default='no')
    chambermarie_image = models.ImageField(upload_to='venues/chambermarie/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.CharField(max_length=20)
    
    # Categories
    is_beach = models.BooleanField(default=False)
    is_city = models.BooleanField(default=False)
    is_hotel = models.BooleanField(default=False)
    is_countryside = models.BooleanField(default=False)
    
    # Gallery
    thumbnail = models.ImageField(upload_to='venues/thumbnails/')
    
    # Location
    full_address = models.CharField(max_length=255)
    region = models.CharField(max_length=100, choices=REGION_CHOICES)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    
    # Amenities
    has_parking = models.BooleanField(default=False)
    has_prayer_rooms = models.BooleanField(default=False)
    has_dj = models.BooleanField(default=False)
    has_photographer = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_swimming_pool = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class VenueImage(models.Model):
    venue = models.ForeignKey(Venue, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='venues/gallery/')
    
    def __str__(self):
        return f"Image for {self.venue.name}"