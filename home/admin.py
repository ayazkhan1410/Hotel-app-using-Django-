from django.contrib import admin
from .models import *

@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ['amenity_name']
    
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['hotel_name',
                    'hotel_price',
                    'description',
                    'room_count',
    ]
                    #'city_name'# Removed 'amenity_name' as it's a ManyToManyField

@admin.register(Hotelimages)
class HotelimagesAdmin(admin.ModelAdmin):
    list_display = ['hotel',
                    'hotel_images']
    
@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ['hotel',
                    'user',
                    'start_date',
                    'end_date',
                    'booking_type']
    
@admin.register(Cities)
class Cities(admin.ModelAdmin):
    list_display = ['city_name']

