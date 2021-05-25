from django.db import models
from django.db.models.fields import CharField
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionPostSerializer(serializers.ModelSerializer):

    destination = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = Transaction
        fields = ('destination', 'amount')
    
    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError('Must Be Positive')
        return value

#  add fund serializer
class AddFundSerializer(TransactionPostSerializer):

    card_id = serializers.IntegerField(required=True)

    class Meta:
        model = Transaction
        fields = ('amount', 'card_id')

    def create(self, validated_data):
        card_id = validated_data.pop('card_id')
        validated_data['additional'] = card_id 
        return Transaction.objects.create(**validated_data)

#  send moneyh
class SendMoneySerializer(TransactionPostSerializer):

    class Meta:
        model = Transaction
        fields = ('amount', 'destination')

    # def create(self, validated_data):
    #     card_id = validated_data.pop('card_id')
    #     validated_data['additional'] = card_id 
    #     return Transaction.objects.create(**validated_data)
    

# TransactionPostSerializer Added So we get validate amount method auto
class TopUpSerializer(TransactionPostSerializer):

    operator = serializers.CharField(max_length=255, write_only=True)
    mobile = serializers.CharField(max_length=255)
    
    def create(self, validated_data):
        return Transaction.objects.create(amount=validated_data['amount'], type='TopUP', mobile=validated_data['mobile'])

    class Meta:
        model = Transaction
        fields = ('operator', 'mobile', 'amount', )
       
        
