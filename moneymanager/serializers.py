from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.urls import reverse

class CustomModelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField('get_id')
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(*list(e))
    
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise ValidationError(*list(e))
    
    def get_id(self, instance):
        return instance.pk