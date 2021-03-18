from datetime import datetime
from django.db.models.deletion import SET_NULL, PROTECT

def NULL_OR_PROTECT(collector, field, sub_objs, using):
    for booking in sub_objs:
        if booking.checkOutDate > datetime.now().date():
            PROTECT(collector, field, sub_objs, using)
            return
    SET_NULL(collector, field, sub_objs, using)