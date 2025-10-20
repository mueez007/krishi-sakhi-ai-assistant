from django.db import models
from django.contrib.auth.models import User

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.username

class Farm(models.Model):
    owner = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=100, default='My Farm')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    land_area = models.DecimalField(max_digits=10, decimal_places=2) 
    
    def __str__(self):
        return f"{self.name} ({self.owner.user.username})"

class CropCycle(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crop_cycles')
    crop_name = models.CharField(max_length=100)
    sowing_date = models.DateField()
    harvest_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.crop_name} on {self.farm.name}"

