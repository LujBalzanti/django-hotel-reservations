from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("room/<int:id>", views.room, name="room"),
    path('booking/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    path('rooms/', views.rooms, name='rooms'),
]