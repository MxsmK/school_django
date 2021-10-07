from django.db import models
from django.utils import timezone


class Person(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    sum = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    is_free = models.BooleanField()
    is_weak = models.BooleanField()
