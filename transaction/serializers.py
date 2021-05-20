from django.db import models
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    source = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'

class AddFundPreivewSerializer(serializers.ModelSerializer):

    source = serializers.ReadOnlyField()
    type = serializers.ReadOnlyField()
    destination = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = '__all__'