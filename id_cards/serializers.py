from rest_framework import serializers
from .models import IdCard
from matir_bank.core.hostname import get_current_host
from django.conf import settings

class IdCardSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = IdCard
        fields = '__all__'

class IdCardPathSerializer(serializers.ModelSerializer):
    
    user = serializers.ReadOnlyField(source='user.id')
    image = serializers.SerializerMethodField()

    class Meta:
        model = IdCard
        fields = '__all__'

    def get_image(self, obj):
        if type(obj).__name__ == "dict":
            return None
        return '{}{}{}'.format(get_current_host(self.context['request'])[:-1], settings.MEDIA_URL, obj.image)

class IdCardMutationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IdCard
        fields = '__all__'
    