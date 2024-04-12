from rest_framework import serializers
from .models import Account, Transaction, Category
from rest_framework.exceptions import ValidationError
from django.utils import timezone

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Account
        fields = '__all__'        

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Category
        fields = '__all__'

class CustomChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return {
            "id": obj.pk,
            "name": str(obj)
        }
    
class TransactionSerializer(serializers.ModelSerializer):
    category = CustomChoiceField(choices=[], allow_blank=True, allow_null=True)
    user = serializers.ReadOnlyField(source='user.username')
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
    
    def validate(self, data):
        if data.get('category', None):
            data['category'] = Category.objects.get(id=data['category'])
        else:
            data['category'] = None
            if data['type'] == 'expense':
                raise ValidationError({'category': 'Category is required for expense transactions'})
        if data['account']:
            data['account'] = Account.objects.get(id=data['account'])
        
        if data['amount'] < 0:
            raise ValidationError({'amount': 'Amount cannot be negative'})
        
        if data.get('category', None) and data['category'].user != self.context.get('request').user:
            raise ValidationError({'category': 'Category does not belong to user'})
        
        if data['account'].user != self.context.get('request').user:
            raise ValidationError({'account': 'Account does not belong to user'})
        
        return data
    
    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)
