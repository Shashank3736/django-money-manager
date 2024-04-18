from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = '__all__'
    
    def create(self, validated_data):
        if validated_data['profile_pic']:
            if validated_data['profile_pic'].size > 1024*1024:
                raise ValidationError("File is too large")
        try:
            return Profile.objects.create(**validated_data)
        except Exception as e:
            raise ValidationError(e)