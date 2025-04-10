# forms.py
from django import forms
from .models import Venue, VenueImage,Booking, BookingType

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [
            'name', 'description', 'chambermarie', 'chambermarie_image',
            'price', 'contact', 'capacity', 
            'is_beach', 'is_city', 'is_hotel', 'is_countryside',
            'thumbnail', 
            'full_address', 'region', 'longitude', 'latitude',
            'has_parking', 'has_prayer_rooms', 'has_dj', 
            'has_photographer', 'has_wifi', 'has_swimming_pool'
        ]
        widgets = {
            # Text Inputs
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Venue Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Venue Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter Price'}),
            'contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Contact'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter Capacity'}),
            'full_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Address'}),
            'longitude': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Longitude'}),
            'latitude': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Latitude'}),

            # Checkboxes with Bootstrap class
            'is_beach': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_city': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_hotel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_countryside': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_prayer_rooms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_dj': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_photographer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_wifi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_swimming_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



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
    
    # We'll handle booking types with checkboxes in the template
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'booking_date', 'guests']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control booking-form-input', 'placeholder': 'Enter Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control booking-form-input', 'placeholder': 'Enter Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control booking-form-input', 'placeholder': 'Enter Your Phone'}),
            'guests': forms.Select(attrs={'class': 'form-select Booking-select', 'style': 'height:39px'}, 
                                 choices=[(1, '1'), (2, '2')])
        }