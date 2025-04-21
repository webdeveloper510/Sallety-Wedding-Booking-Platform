# forms.py
from django import forms
from .models import Venue, VenueImage,Booking, BookingType
from .models import VisitRequest
import re



class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [
            'name', 'description', 'chambermarie', 'chambermarie_image',
            'price', 'contact', 'capacity',
            'is_beach', 'is_city', 'is_hotel', 'is_countryside',
            'is_mountain', 'is_resort', 'is_forest', 'is_rooftop', 'is_garden', 
            'is_desert','is_lake','is_island','is_cave','is_vineyard',
            'thumbnail',
            'full_address', 'region', 'longitude', 'latitude',
            'has_parking', 'has_prayer_rooms', 'has_dj',
            'has_photographer', 'has_wifi', 'has_swimming_pool'
        ]
        widgets = {
            # Text Inputs
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Venue Name', 'required': True}),
            'description': forms.Textarea(attrs={'placeholder': 'Venue Description', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter Price', 'required': True}),
            'contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Contact', 'required': True}),
            'capacity': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter Capacity (Ex-100)', 'required': True}),
            'full_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Address', 'required': True}),
            'longitude': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Longitude', 'required': True}),
            'latitude': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Latitude', 'required': True}),
            
            # Checkboxes with Bootstrap class
            'is_beach': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_city': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_hotel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_countryside': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_mountain': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_resort': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_forest': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_rooftop': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_garden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_desert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_lake': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_island': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_cave': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_vineyard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_prayer_rooms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_dj': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_photographer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_wifi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_swimming_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Venue name is required.")
        if len(name) < 3:
            raise forms.ValidationError("Venue name must be at least 3 characters long.")
        return name
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("Venue description is required.")
        if len(description) < 20:
            raise forms.ValidationError("Description must be at least 20 characters long.")
        return description
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise forms.ValidationError("Price is required.")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
    
    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact:
            raise forms.ValidationError("Contact information is required.")
        # Basic phone number validation
        if not re.match(r'^[\d\s\+\-\(\)]{7,20}$', contact):
            raise forms.ValidationError("Please enter a valid phone number.")
        return contact
    
    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity is None:
            raise forms.ValidationError("Capacity is required.")
        if capacity <= 0:
            raise forms.ValidationError("Capacity must be greater than zero.")
        return capacity
    
    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        if not thumbnail and not self.instance.pk:
            raise forms.ValidationError("Please upload a thumbnail image.")
        return thumbnail
    
    def clean_full_address(self):
        address = self.cleaned_data.get('full_address')
        if not address:
            raise forms.ValidationError("Full address is required.")
        return address
    
    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if not longitude:
            raise forms.ValidationError("Longitude is required.")
        try:
            lon_value = float(longitude)
            if lon_value < -180 or lon_value > 180:
                raise forms.ValidationError("Longitude must be between -180 and 180.")
        except ValueError:
            raise forms.ValidationError("Longitude must be a valid number.")
        return longitude
    
    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if not latitude:
            raise forms.ValidationError("Latitude is required.")
        try:
            lat_value = float(latitude)
            if lat_value < -90 or lat_value > 90:
                raise forms.ValidationError("Latitude must be between -90 and 90.")
        except ValueError:
            raise forms.ValidationError("Latitude must be a valid number.")
        return latitude
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check if at least one category is selected
        categories = [
            'is_beach', 'is_city', 'is_hotel', 'is_countryside',
            'is_mountain', 'is_resort', 'is_forest', 'is_rooftop', 'is_garden'
        ]
        
        category_selected = False
        for category in categories:
            if cleaned_data.get(category):
                category_selected = True
                break
        
        if not category_selected:
            raise forms.ValidationError("Please select at least one venue category.")
        
        return cleaned_data

class VenueImageForm(forms.ModelForm):
    class Meta:
        model = VenueImage
        fields = ['image']
       
# FormSet for handling multiple image uploads
VenueImageFormSet = forms.inlineformset_factory(
    Venue, VenueImage, form=VenueImageForm,
    extra=5, max_num=5, can_delete=True
)

class BookingForm(forms.ModelForm):
    booking_date = forms.DateField(widget=forms.HiddenInput())
    venue_id = forms.IntegerField(widget=forms.HiddenInput())
    
    # We'll handle booking types with checkboxes in the template
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'booking_date', 'guests']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control booking-form-input', 'placeholder': 'Enter Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control booking-form-input', 'placeholder': 'Enter Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control booking-form-input', 'placeholder': 'Enter Your Phone'}),
            'guests': forms.Select(attrs={'class': 'form-select Booking-select', 'style': 'height:39px'}, 
                                 choices=[(1, '1'), (2, '2'),(3,'3'),(4,'4'),(5,'5')])
        }


        
class VisitRequestForm(forms.ModelForm):
    class Meta:
        model = VisitRequest
        fields = ['name', 'email', 'phone', 'visit_date', 'time_slot']


    #     class VisitRequestForm(forms.ModelForm):
    # class Meta:
    #     model = VisitRequest
    #     fields = ['name', 'email', 'phone', 'visit_date', 'time_slot']
    #     widgets = {
    #         'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
    #         'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    #         'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone'}),
    #         'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    #         'time_slot': forms.Select(attrs={'class': 'form-select'}),
    #     }