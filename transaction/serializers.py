from django.db import models
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('destination', 'amount')


class AddFundSerializer(serializers.ModelSerializer):

    card_id = serializers.IntegerField(required=True)

    class Meta:
        model = Transaction
        fields = ('amount', 'card_id')
        
    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('Must Be Positive')
        return value