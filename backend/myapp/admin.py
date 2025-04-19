from django.contrib import admin

from .models import RoomInterior


class RoomAdmin(admin.ModelAdmin):
    list_display = ["room_type", "room_image_url"]
    list_display_links = ["room_type"]
    search_fields = ["room_type"]


admin.site.register(RoomInterior, RoomAdmin)
