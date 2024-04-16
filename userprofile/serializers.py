from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = '__all__'
    
    def create(self, validated_data):
        try:
            Profile.objects.create(**validated_data)
        except Exception as e:
            raise ValidationError(e)