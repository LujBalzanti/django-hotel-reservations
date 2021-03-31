from reservations.models import *
import django_filters

class RoomTypeFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = {
            'type': ['exact']
        }