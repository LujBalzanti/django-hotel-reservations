from django.forms import ModelForm
from django import forms
from reservations.models import Guest, Booking, Room, RoomType
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import ugettext_lazy as _

class GuestForm(ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'
        labels = {
            'number': _('Number of Guests'),
            'firstName': _('First Name'),
            'lastName': _('Last Name'),
            'description': _('Notes')
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5, "class": "form-control w-75"}),
            'number': forms.NumberInput(attrs={'class': 'form-control w-25'}),
            'firstName': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control w-50'})
        }
        error_messages = {
            'firstName': {
                'max_length': _("This name is too long."),
            },
            'lastName': {
                'max_length': _("This name is too long."),
            },
            'description': {
                'max_length': _("This description is too long."),
            },
        }

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["checkInDate", "checkOutDate"]
        widgets = {
            'checkInDate': forms.DateInput(attrs={'class': 'datepicker form-control w-25'}),
            'checkOutDate': forms.DateInput(attrs={'class': 'datepicker form-control w-25 mb-3'})
        }
        labels = {
            'checkInDate': _('Check-in date'),
            'checkOutDate': _('Check-out date'),
        }        

class RoomTypeForm(ModelForm):
    type = forms.ModelChoiceField(queryset=RoomType.objects.all(), widget=forms.Select(attrs={'class': 'datepicker form-control form-select w-50'}))
    class Meta:
        model = RoomType
        fields = ["type"]
        labels = {
            'type': _('Room type'),
        }  