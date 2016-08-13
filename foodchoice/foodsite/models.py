from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Restaurant(models.Model):
    number_requests = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
