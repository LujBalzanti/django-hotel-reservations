from datetime import datetime, timedelta
from django.db.models import Max
from django.db.models.deletion import SET_NULL, PROTECT
import random

def NULL_OR_PROTECT(collector, field, sub_objs, using):
    for booking in sub_objs:
        if booking.checkOutDate > datetime.now().date():
            PROTECT(collector, field, sub_objs, using)
            return
    SET_NULL(collector, field, sub_objs, using)

def get3RandomRoomIds(Room):
    max_id = Room.objects.all().aggregate(max_id=Max("id"))['max_id']
    room_ids = []
    while len(room_ids) < 3:
        key = random.randint(1, max_id)
        if key not in room_ids:
            room = Room.objects.filter(pk=key).first()
            if room:
                room_ids.append(key)

    return room_ids

def getDateRangeCheckIn(startDate, endDate):
    while startDate < endDate:
        yield startDate.strftime('%Y-%m-%d')
        startDate += timedelta(days=1)

def getDateRangeCheckOut(startDate, endDate):
    while startDate < endDate:
        startDate += timedelta(days=1)
        yield startDate.strftime('%Y-%m-%d')

def checkRoomStatus(Room, Booking):
    activeBooking = Booking.objects.filter(room=Room,  checkInDate__lte=datetime.now().date(), checkOutDate__gt=datetime.now().date())

    if activeBooking:
        Room.status = "BKD"
        Room.save()
    else:
        Room.status = "AVL"
        Room.save()