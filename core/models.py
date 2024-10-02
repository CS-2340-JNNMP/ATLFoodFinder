# models.py
from django.db import models
from django.contrib.auth.models import User



class Restaurant(models.Model):
    image = models.URLField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    place_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class SavedRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} saved {self.restaurant.name}"