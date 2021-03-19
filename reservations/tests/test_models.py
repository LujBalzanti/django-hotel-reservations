from django.test import TestCase
from django.forms import ValidationError
from django.db import IntegrityError
from reservations.models import *
from datetime import datetime, timedelta

class TestModels(TestCase):

    def setUp(self):
        self.testRoomType = RoomType.objects.create(
            type = "roomType",
            rate = 50.5
        )
        self.testRoom = Room.objects.create(
            number = 202,
            type = self.testRoomType,
            floor = 2,
        )
        self.testGuest = Guest.objects.create(
            number = 3,
            firstName = "testGuest",
            lastName = "testGuestLast",
            description = "This is a test description"
        )
        self.testBooking = Booking.objects.create(
            checkInDate = datetime.now().date(),
            checkOutDate = datetime.now().date() + timedelta(days=20),
            room = self.testRoom,
            guests = self.testGuest
        )

    def testCreateRoomType_WithNegativeRate_ThrowsValidationError(self):
        testNegativeRateRoomType = RoomType.objects.create(
            type = "testRoomType",
            rate = -45
        )

        self.assertRaises(ValidationError, testNegativeRateRoomType.full_clean)

    def testCreateGuest_WithNumberLessThanOne_ThrowsValidationError(self):
        testNoGuests = Guest.objects.create(
            number = 0,
            firstName = "testGuest",
            lastName = "testGuestLast",
            description = "This is a test description"
        )
        testNegativeGuests = Guest.objects.create(
            number = -5,
            firstName = "testGuest",
            lastName = "testGuestLast",
            description = "This is a test description"
        )

        self.assertRaises(ValidationError, testNoGuests.full_clean)
        self.assertRaises(ValidationError, testNegativeGuests.full_clean)

    def testCreateBooking_WithPastDate_ThrowsValidationError(self):
        testWrongBooking = Booking.objects.create(
            room = self.testRoom,
            checkInDate = datetime(2000, 5, 5),
            checkOutDate = datetime(2030, 3, 3),
            guests = self.testGuest
        ) 

        self.assertRaises(ValidationError, testWrongBooking.full_clean)

    def testCreateBooking_WithOverlappingDates_ThrowsValidationError(self):
        testWrongBooking = Booking.objects.create(
            room = self.testRoom,
            checkInDate = datetime.now().date(),
            checkOutDate = datetime.now().date() + timedelta(days=10),
            guests = self.testGuest
        ) 

        self.assertRaises(ValidationError, testWrongBooking.full_clean)

    def testCreateBooking_EndDateBeforeStartDate_ThrowsValidationError(self):
        testWrongBooking = Booking.objects.create(
            room = self.testRoom,
            checkInDate = datetime.now().date() + timedelta(days=10),
            checkOutDate = datetime.now().date(),
            guests = self.testGuest
        )
        
        self.assertRaises(ValidationError, testWrongBooking.full_clean)

    def testDeleteRoom_WithFutureBooking_RaisesIntegrityError(self):
        with self.assertRaises(IntegrityError):
            self.testRoom.delete()

    def testDeleteRoom_WithNoBookings_Deletes(self):
        room = Room.objects.create(
            type = self.testRoomType,
            number = 400,
            floor = 5
        )

        room.delete()

        self.assertFalse(Room.objects.filter(number=400))