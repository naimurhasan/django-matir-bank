from django.db import models

# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=255)
    card_no = models.CharField(unique=True, max_length=19)
    validity = models.CharField(max_length=255)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.card_no