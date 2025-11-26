from django.db import models

# Create your models here.


class User(models.Model):
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE) # int
    latitude = models.DecimalField(max_digits=10, decimal_places=8) # decimal широта локации
    longitude = models.DecimalField(max_digits=10, decimal_places=8) # decimal долгота локации
