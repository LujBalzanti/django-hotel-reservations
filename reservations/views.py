from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "reservations/home.html")

def booking(request):
    return render(request, "reservations/booking.html")