from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class BaseModel(models.Model):
    # Unique identifier for each record
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
     
    # Records the date when the record is created
    created_at = models.DateField(auto_now_add=True)  
    
    # Records the date when the record is updated
    updated_at = models.DateField(auto_now_add=True)  
    
    class Meta:
        abstract = True
        
class Cities(BaseModel):
    city = models.CharField(max_length = 100)
    
    def __str__(self) -> str:
        return self.city
    
class Amenities(BaseModel):
    # Model representing various amenities available
    amenity_name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.amenity_name
    
class Hotel(BaseModel):
    # Model representing details of a hotel including name, price, description, amenities, and room count
    hotel_name = models.CharField(max_length=100)
    hotel_price = models.PositiveIntegerField(default=1000)
    description = models.TextField(max_length=500)
    amenity_name = models.ManyToManyField(Amenities)
    room_count = models.PositiveIntegerField(default=10)
    city_name = models.ForeignKey(Cities, related_name="city_name", on_delete = models.CASCADE)
    
    class Meta:
        ordering = ['hotel_name']
    
    def __str__(self) -> str:
        return self.hotel_name
    
class Hotelimages(BaseModel):
    # Model storing images for a hotel
    hotel = models.ForeignKey(Hotel, related_name="images", on_delete=models.CASCADE)
    hotel_images = models.ImageField(upload_to="hotel_images")

class HotelBooking(BaseModel):
    # Model representing hotel bookings made by users
    hotel = models.ForeignKey(Hotel, related_name="hotel_booking", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_booking", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type = models.CharField(max_length = 100, choices=(('pre paid', 'pre paid'), ('post paid', 'post paid')))
    
    
