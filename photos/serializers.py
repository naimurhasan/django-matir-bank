from matir_bank.core.hostname import get_current_host
from rest_framework import serializers
from .models import Photo
from django.conf import settings

class PhotoSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Photo
        fields = '__all__'

class PhotoPathSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.id')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = '__all__'

    def get_image(self, obj):
        if type(obj).__name__ == "dict":
            return None
        return '{}{}{}'.format(get_current_host(self.context['request'])[:-1], settings.MEDIA_URL, obj.image)



class PhotoMutationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Photo
        fields = '__all__'

    