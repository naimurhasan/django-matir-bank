from rest_framework import serializers
from .models import Card
from django.db import models

class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'
    
    
    

    
    
    