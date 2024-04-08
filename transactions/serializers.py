from rest_framework import serializers
from .models import Account, Transaction, Category
from rest_framework.exceptions import ValidationError

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

class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=[], source='category.name', allow_blank=True, allow_null=True)
    user = serializers.ReadOnlyField(source='user.username')
    account = serializers.ChoiceField(choices=[], source='account.name')

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
        if data.get('category', None) and data['category']['name']:
            data['category'] = Category.objects.get(id=data['category']['name'])
        else:
            if data['type'] == 'expense':
                raise ValidationError({'category': 'Category is required for expense transactions'})
        if data['account']:
            data['account'] = Account.objects.get(id=data['account']['name'])
        
        if data['amount'] < 0:
            raise ValidationError({'amount': 'Amount cannot be negative'})
        
        return data
    
    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)
