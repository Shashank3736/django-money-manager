from rest_framework import serializers
from moneymanager.serializers import CustomModelSerializer, CustomReadOnlyField
from .models import Account, Transaction, Category
from rest_framework.exceptions import ValidationError
from django.utils import timezone

class AccountSerializer(CustomModelSerializer):
    user = CustomReadOnlyField()

    class Meta:
        model = Account
        fields = '__all__'

class CategorySerializer(CustomModelSerializer):
    user = CustomReadOnlyField()
    class Meta:
        model = Category
        fields = '__all__'
    
class TransactionSerializer(CustomModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none(), allow_null=True)
    user = CustomReadOnlyField()
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.none())
    datetime = serializers.DateTimeField(default=timezone.now())

    class Meta:
        model = Transaction
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            self.fields['account'].queryset = Account.objects.filter(user=request.user)
            self.fields['category'].queryset = Category.objects.filter(user=request.user)
