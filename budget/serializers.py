from rest_framework import serializers
from .models import Budgets
from rest_framework.exceptions import ValidationError

# code
class BudgetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Budgets
        fields = "__all__"
    
    def create(self, validated_data):
        if validated_data['category'] and validated_data['category'].user != validated_data['user']:
            raise ValidationError("Category is not owned by the user.")
        
        if validated_data['amount'] < 0:
            raise ValidationError("Amount need to be greater than zero.")
        return super().create(validated_data)