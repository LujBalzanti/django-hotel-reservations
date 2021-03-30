from django.forms import ModelForm
from reservations.models import Guest, Booking


class GuestForm(ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'
        labels{
            'number': _('Number of Guests'),
            'firstName': _('First Name'),
            'lastName': _('Last Name'),
            'description': _('Description')
        }
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20})
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