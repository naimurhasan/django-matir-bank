from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Card
from django.db import models

class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'
    
    
    

    
    
    