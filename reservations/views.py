from django.shortcuts import render
from django.http import HttpResponse
from reservations.models import *
from django.db.models import Max

def home(request):
    return render(request, "reservations/home.html", {
    })

def room(request, id):
    return render(request, "reservations/room.html", {

    })

def booking(request):
    return render(request, "reservations/booking.html")