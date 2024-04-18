from rest_framework import serializers
from moneymanager.serializers import CustomModelSerializer
from .models import Profile

class ProfileSerializer(serializers.HyperlinkedModelSerializer, CustomModelSerializer):
    user = serializers.ReadOnlyField(source='user.pk')

    class Meta:
        model = Profile
        fields = '__all__'