from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Card(models.Model):
    name = models.CharField(max_length=255)
    card_no = models.CharField(unique=True, max_length=19)
    validity = models.CharField(max_length=255)
    cvv = models.CharField(max_length=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.card_no