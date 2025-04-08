# forms.py
from django import forms
from .models import Venue, VenueImage

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [
            'name', 'description', 'chambermarie', 'chambermarie_image',
            'price', 'contact', 
            'is_beach', 'is_city', 'is_hotel', 'is_countryside',
            'thumbnail', 
            'full_address', 'region', 'longitude', 'latitude',
            'has_parking', 'has_prayer_rooms', 'has_dj', 
            'has_photographer', 'has_wifi', 'has_swimming_pool'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Venue Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Venue Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter Price'}),
            'contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Contact'}),
            'full_address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Address'}),
            'longitude': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Longitude'}),
            'latitude': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Latitude'}),
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