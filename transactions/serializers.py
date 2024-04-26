from rest_framework import serializers
from moneymanager.serializers import CustomModelSerializer, CustomReadOnlyField
from .models import Account, Transaction, Category
from rest_framework.exceptions import ValidationError
from django.utils import timezone
import uuid

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

class CustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        try:
            value = uuid.UUID(str(value))
            account = self.queryset.get(pk=value)
            # Customize the representation of the related object here
            return {
                '_id': account.id,
                'name': account.name,
                # Add more fields as needed
            }
        except:
            # Handle the case where the related object does not exist
            return None 
    
class TransactionSerializer(CustomModelSerializer):
    category = CustomPrimaryKeyRelatedField(queryset=Category.objects.none(), allow_null=True)
    user = CustomReadOnlyField()
    account = CustomPrimaryKeyRelatedField(queryset=Account.objects.none())
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
