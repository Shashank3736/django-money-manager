from rest_framework import serializers
from moneymanager.serializers import CustomModelSerializer, CustomReadOnlyField
from .models import Budgets
from transactions.serializers import CategorySerializer

# code
class BudgetSerializer(CustomModelSerializer):
    user = CustomReadOnlyField()
    category = CategorySerializer()

    class Meta:
        model = Budgets
        fields = "__all__"