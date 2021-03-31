from django.shortcuts import render
from reservations.models import *
from django.db.models import Max
from reservations.util import get3RandomRoomIds
from django.core.paginator import Paginator
from reservations.filters import RoomTypeFilter

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
    return render(request, "reservations/room.html", {

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
