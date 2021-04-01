from reservations.models import *
import django_filters
from django_filters.widgets import LinkWidget

class RoomTypeFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = {
            'type': ['exact']
        }       