from moneymanager.serializers import CustomModelSerializer, CustomReadOnlyField
from .models import Budgets
from transactions.serializers import CategorySerializer

# code
class BudgetSerializer(CustomModelSerializer):
    user = CustomReadOnlyField()

    class Meta:
        model = Budgets
        fields = "__all__"