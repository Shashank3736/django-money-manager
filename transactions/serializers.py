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

class CustomChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return {
            "_id": obj.pk,
            "name": str(obj)
        }
    
class TransactionSerializer(CustomModelSerializer):
    category = CustomChoiceField(choices=[], allow_blank=True, allow_null=True)
    user = CustomReadOnlyField()
    account = CustomChoiceField(choices=[])
    datetime = serializers.DateTimeField(default=timezone.now())

    class Meta:
        model = Transaction
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            self.fields['category'].choices = Category.objects.filter(user=request.user).values_list('id', 'name')
            self.fields['account'].choices = Account.objects.filter(user=request.user).values_list('id', 'name')
    
        