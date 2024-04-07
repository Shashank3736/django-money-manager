from rest_framework import serializers
from .models import CustomUser as User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['url', 'username', 'id', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.get('password')
        if password:
            user = User.objects.get(username=instance.username)
            user.set_password(password)
            user.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['request'].user != instance:
            representation['email'] = None
        return representation