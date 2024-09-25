from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    place_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
