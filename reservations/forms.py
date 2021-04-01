from django.forms import ModelForm
from django import forms
from reservations.models import Guest, Booking, Room
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
            'description': _('Description')
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5, "class": "form-control w-75"}),
            'number': forms.NumberInput(attrs={'class': 'form-control w-25'}),
            'firstName': forms.NumberInput(attrs={'class': 'form-control w-50'}),
            'lastName': forms.NumberInput(attrs={'class': 'form-control w-50'})
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
            'checkInDate': forms.SelectDateWidget(attrs={}),
            'checkOutDate': forms.SelectDateWidget(attrs={})
        }        