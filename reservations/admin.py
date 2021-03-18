from django.contrib import admin
from .models import *

class RoomPictureInline(admin.StackedInline):
    model = RoomPicture

class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomPictureInline, ]

admin.site.register(RoomPicture)
admin.site.register(RoomType)
admin.site.register(Room, RoomAdmin)
admin.site.register(Guest)
admin.site.register(Booking)
