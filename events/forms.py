from django import forms 
from django.forms import ModelForm
from .models import Venue, Event

# Admin super user
class EventFormAdmin(ModelForm):
    class Meta: 
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description')
        labels = {
                'name': '',
                'event_date': 'YYY-MM-DD HH:MM:SS',
                'venue': 'Venue',
                'manager': 'Manager',
                'attendees': 'Attendees',
                'description': '',
                }
        widgets = {
                'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event name'}),
                'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event date'}),
                'venue': forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue'}),
                'manger': forms.Select(attrs={'class':'form-select', 'placeholder': 'Manager'}),
                'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder': 'Attendees'}),
                'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}),

                }


class EventForm(ModelForm):
    class Meta: 
        model = Event
        fields = ('name', 'event_date', 'venue', 'attendees', 'description')
        labels = {
                'name': '',
                'event_date': 'YYY-MM-DD HH-MM-SS',
                'venue': 'Venue',
                'attendees': 'Attendees',
                'description': '',
                }
        widgets = {
                'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event name'}),
                'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event date'}),
                'venue': forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue'}),
                'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder': 'Attendees'}),
                'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}),

                }




# Create a venue form 
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'venue_image') 
        labels = {
                'name': '',
                'address': '',
                'zip_code': '',
                'phone': '',
                'web': '',
                'email_address': '',
                'venue_image': ''
                } 
        
        widgets = {
                'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Venue name'}),
                'address': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address'}),
                'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zip code'}),
                'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone number'}),
                'web': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Website URL'}),
                'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}),
                }
