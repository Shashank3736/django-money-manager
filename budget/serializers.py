from rest_framework import serializers
from moneymanager.serializers import CustomModelSerializer
from .models import Budgets

# code
class BudgetSerializer(CustomModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Budgets
        fields = "__all__"