import uuid
from django.db import models
from account.models import CustomUser as User
from django.core.exceptions import ValidationError

# Create your models here.
class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=32)
    balance = models.FloatField(default=0)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class Transaction(models.Model):
    types = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    amount = models.FloatField()
    datetime = models.DateTimeField()
    type = models.CharField(max_length=32, choices=types)
    description = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        if self.type == 'income':
            if not self.category:
                raise ValidationError('Category is required for income transactions')
            self.account.balance += self.amount
        elif self.type == 'expense':
            self.account.balance -= self.amount
        super().save(*args, **kwargs)
