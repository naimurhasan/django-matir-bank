from rest_framework import serializers
from .models import IdCard

class IdCardSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = IdCard
        fields = '__all__'

class IdCardMutationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IdCard
        fields = '__all__'
    