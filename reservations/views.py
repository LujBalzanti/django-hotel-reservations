from django.shortcuts import render
from reservations.models import *
from django.db.models import Max
from datetime import datetime
from reservations.util import get3RandomRoomIds, getDateRangeByDay
from django.core.paginator import Paginator
from reservations.filters import RoomTypeFilter
from reservations.forms import *
import json
from django.core import serializers

def home(request):
    room_ids = get3RandomRoomIds(Room)

    room1 = Room.objects.filter(pk=room_ids[0]).get()
    room2 = Room.objects.filter(pk=room_ids[1]).get()
    room3 = Room.objects.filter(pk=room_ids[2]).get()

    return render(request, "reservations/home.html", {
        "room1": room1,
        "room2": room2,
        "room3": room3,
    })

def room(request, id):
    room = Room.objects.get(id=id)
    bookings = Booking.objects.filter(checkOutDate__gt=datetime.now().date(), room=room)
    
    if request.method == "POST":
        newGuestForm = GuestForm(data=request.POST)
        if newGuestForm.is_valid():           
            newBookingForm = BookingForm(data=request.POST)

            if newBookingForm.is_valid():
                newBooking = newBookingForm.save(commit=False)
                newBooking.room = room
                try:
                    newBooking.clean()
                except:
                    return render(request, "reservations/error.html", {
                        "error": "Validation Error: Something has gone wrong with the booking. Please ensure that the reservation dates are not overlapping."
                })

                newGuest = newGuestForm.save() 
                newBooking.guests = newGuest
                newBooking.save()

                guestForm = GuestForm()
                bookingForm = BookingForm()
                reservedDates = []
                for booking in bookings:
                    for date in getDateRangeByDay(booking.checkInDate, booking.checkOutDate):
                        reservedDates.append(date)   
                return render(request, "reservations/room.html", {
                    "room": room,
                    "guestForm": guestForm,
                    "bookingForm": bookingForm,
                    "reservedDates": reservedDates,
                    "justBooked": True
                })                
            else:
                return render(request, "reservations/error.html", {
                    "error": "Something has gone wrong with the booking. Please ensure that the reservation dates are correct."
                })
        else:
            return render(request, "reservations/error.html", {
                "error": "Something has gone wrong with the booking. Please ensure that the guest information is correct."
            })
        
    else:
        reservedDates = []
        for booking in bookings:
            for date in getDateRangeByDay(booking.checkInDate, booking.checkOutDate):
                reservedDates.append(date)   
        guestForm = GuestForm()
        bookingForm = BookingForm()
        return render(request, "reservations/room.html", {
            "room": room,
            "guestForm": guestForm,
            "bookingForm": bookingForm,
            "reservedDates": reservedDates,
        })

def booking(request):
    return render(request, "reservations/booking.html")

def contact(request):
    return render(request, "reservations/contact.html")

def rooms(request):
    roomList = Room.objects.all()
    filteredRooms = RoomTypeFilter(request.GET, queryset=roomList)
    roomList = filteredRooms.qs

    paginator = Paginator(roomList, 6)
    page = request.GET.get('page', 1)

    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)

    return render(request, "reservations/rooms.html", {
        'rooms': rooms,
        'paginator': paginator,
        'filter': filteredRooms
    })
