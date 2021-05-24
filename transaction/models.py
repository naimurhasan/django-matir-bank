from django.db import models

# Create your models here.
class Transaction(models.Model):
    source = models.BigIntegerField()
    destination = models.BigIntegerField()
    type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=10)
    additional = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)