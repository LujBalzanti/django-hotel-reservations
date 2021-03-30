from django.shortcuts import render
from django.http import HttpResponse
from reservations.models import *
from django.db.models import Max
from reservations.util import get3RandomRoomIds

def home(request):
    room_ids = get3RandomRoomIds(Room)

    room1 = Room.objects.filter(pk=room_ids[0]).get()
    room2 = Room.objects.filter(pk=room_ids[1]).get()
    room3 = Room.objects.filter(pk=room_ids[2]).get()

    room1Img = room1.pictured_room.first()
    room2Img = room2.pictured_room.first()
    room3Img = room3.pictured_room.first()

    return render(request, "reservations/home.html", {
        "room1Img": room1Img,
        "room2Img": room2Img,
        "room3Img": room3Img,
        "room1": room1,
        "room2": room2,
        "room3": room3,
    })

def room(request, id):
    return render(request, "reservations/room.html", {

    })

def booking(request):
    return render(request, "reservations/booking.html")