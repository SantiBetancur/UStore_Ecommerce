from django.db import models
from users.models import Store
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products", null=True, blank=True)

    def __str__(self):
        return self.name
