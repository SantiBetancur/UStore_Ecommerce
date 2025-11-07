from django.db import models

class Store(models.Model):
    market_id = models.AutoField(primary_key=True)
    name = models.TextField(null=False, unique=True)
    description = models.TextField()
    logo = models.TextField(null=True, blank=True) 