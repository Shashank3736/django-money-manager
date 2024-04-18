from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

class CustomModelSerializer(ModelSerializer):
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