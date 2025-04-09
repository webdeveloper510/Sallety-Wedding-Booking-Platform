# admin.py
from django.contrib import admin
from .models import Venue, VenueImage
from .models import BookingType, Booking

class VenueImageInline(admin.TabularInline):
    model = VenueImage
    extra = 1

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'status', 'created_at', 'price', 'region')
    list_filter = ('status', 'region', 'is_beach', 'is_city', 'is_hotel', 'is_countryside')
    search_fields = ('name', 'description', 'full_address')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    inlines = [VenueImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'contact', 'thumbnail')
        }),
        ('Categories', {
            'fields': ('is_beach', 'is_city', 'is_hotel', 'is_countryside')
        }),
        ('Chambermarie', {
            'fields': ('chambermarie', 'chambermarie_image')
        }),
        ('Location', {
            'fields': ('full_address', 'region', 'longitude', 'latitude')
        }),
        ('Amenities', {
            'fields': ('has_parking', 'has_prayer_rooms', 'has_dj', 'has_photographer', 'has_wifi', 'has_swimming_pool')
        }),
        ('Status Information', {
            'fields': ('user_id', 'status', 'created_at', 'updated_at')
        }),
    )

class BookingTypeAdmin(admin.ModelAdmin):
        list_display = ('name', 'price')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'booking_date', 'guests', 'total_price', 'created_at')
    filter_horizontal = ('types',)
    list_filter = ('booking_date', 'created_at')
    search_fields = ('name', 'email', 'phone')

admin.site.register(BookingType, BookingTypeAdmin)
admin.site.register(Booking, BookingAdmin)