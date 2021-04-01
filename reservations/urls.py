from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("room/<int:id>", views.room, name="room"),
    path('booking/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    url(r'^rooms/$', views.rooms, name='rooms'),
    path('booking/room/<int:id>', views.roomBooking, name="roomBooking"),
]