from rest_framework import serializers
from .models import Budgets
from rest_framework.exceptions import ValidationError

# code
class BudgetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Budgets
        fields = "__all__"