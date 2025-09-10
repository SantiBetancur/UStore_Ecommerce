from django.db import models

class Store(models.Model):
    market_id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()