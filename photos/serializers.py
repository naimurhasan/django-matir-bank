from rest_framework import serializers
from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Photo
        fields = '__all__'

class PhotoMutationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Photo
        fields = '__all__'

    