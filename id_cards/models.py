from django.db import models
from django.contrib.auth import get_user_model
from enum import Enum
User = get_user_model()


class IdCard(models.Model):
    
    NID = 'NID'
    PASSPORT = 'PASSPORT'
    BIRTH_CERTIFICATE = 'BIRTH_CERTIFICATE'
    DRIVING_LICENSE = 'DRIVING_LICENSE'
    OTHER = 'OTHER'

    ID_CARD_TYPE_CHOICES = [
        (NID, 'National Id Card'),
        (PASSPORT, 'Passport'),
        (BIRTH_CERTIFICATE, 'Birth Certificate'),
        (DRIVING_LICENSE, 'Driving License'),
        (OTHER, 'Other'),
    ]

    type = models.CharField(
        max_length=17,
        choices=ID_CARD_TYPE_CHOICES,
    )
    image = models.ImageField(upload_to='id_card/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return 'Id of '+str(self.user.id)
