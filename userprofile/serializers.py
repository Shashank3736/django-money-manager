from rest_framework import serializers
from moneymanager.serializers import CustomModelSerializer
from .models import Profile

class ProfileSerializer(CustomModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = '__all__'