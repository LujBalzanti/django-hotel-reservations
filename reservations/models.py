from django.db import models
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from .util import NULL_OR_PROTECT
from django.core.exceptions import ValidationError

class RoomType(models.Model):
    type = models.CharField(max_length=50)
    rate = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.type

class Room(models.Model):

    class CardinalLocation(models.TextChoices):
        SOUTH = "S", _("South")
        NORTH = "N", _("North")
        EAST = "E", _("East")
        WEST = "W", _("West")
        SOUTHEAST = "SE", _("South East")
        SOUTHWEST = "SW", _("South West")
        NORTHEAST = "NE", _("North East")
        NORTHWEST = "NW", _("North West")

    class Status(models.TextChoices):
        BOOKED = "BKD", _("Booked")
        AVAILABLE = "AVL", _("Available")
        MAINTENANCE = "MTC", _("Maintenance")

    number = models.IntegerField()        
    status = models.CharField(
        max_length = 3,
        choices = Status.choices,
        default = Status.AVAILABLE,
    )   
    type = models.ForeignKey(
        RoomType,
        on_delete = models.PROTECT,
        related_name="room_type",
    )
    floor = models.IntegerField() 
    cardinalLocation = models.CharField(
        max_length = 2,
        choices = CardinalLocation.choices,
        default = CardinalLocation.EAST,
    )

    def __str__(self):
        return str(self.number)

class RoomPicture(models.Model):
    picture = models.ImageField(null=True, blank=True, upload_to="roomImages")
    room = models.ForeignKey(Room, related_name="pictured_room", on_delete=models.CASCADE)

class Guest(models.Model):
    number = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

class Booking(models.Model):
    checkInDate = models.DateField()
    checkOutDate = models.DateField()
    room = models.ForeignKey(
        Room,
        related_name="booked_room",
        null=True,
        on_delete=NULL_OR_PROTECT,
    )
    guests = models.ForeignKey(
        Guest,
        related_name="booked_guests",
        on_delete=models.PROTECT,
    )

    def clean(self, *args, **kwargs):
        if self.checkInDate > self.checkOutDate:
            raise ValidationError(
                "Check out date cannot be before check in date"
            )

        if self.checkInDate < datetime.now().date():
            raise ValidationError(
                "Check in date cannot be before today"
            )
                
        bookings = Booking.objects.filter(room=self.room, checkOutDate__gt=datetime.now().date())

        for booking in bookings:
            if booking.checkInDate < self.checkOutDate and booking.checkOutDate > self.checkInDate:
                raise ValidationError(
                    "The room is already booked within that timeframe"
                )
