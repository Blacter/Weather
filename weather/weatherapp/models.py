import uuid
import json
from django.db import models

# Create your models here.


class User(models.Model):
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)


class Location(models.Model):
    name = models.CharField(max_length=255)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE) # int
    latitude = models.DecimalField(max_digits=10, decimal_places=6) # decimal широта локации
    longitude = models.DecimalField(max_digits=10, decimal_places=6) # decimal долгота локации


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    session_data = models.TextField(default=json.dumps(None))
    expire_at = models.DateTimeField()


