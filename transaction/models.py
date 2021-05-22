from django.db import models

# Create your models here.
class Transaction(models.Model):
    source = models.CharField(max_length=255, null=True)
    destination = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=10)
    card_id = models.BigIntegerField(null=True)
    mobile = models.CharField(max_length=255, null=True)
