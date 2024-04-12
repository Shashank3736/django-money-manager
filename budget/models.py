from typing import Collection
from django.db import models
from account.models import CustomUser as User
from transactions.models import Category
from django.core.exceptions import ValidationError
import uuid
# Create your models here.
class Budgets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    name = models.CharField(max_length=32)
    amount = models.IntegerField()
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name="budget", null=True)

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')

    def __str__(self) -> str:
        return self.name
    
    def validate_constraints(self, exclude: Collection[str] | None = ...) -> None:
        if self.category.user != self.user:
            raise ValidationError("User do not own the category.")
        
        if self.amount < 0:
            raise ValidationError("Amount need to be greater than zero.")
        return super().validate_constraints(exclude)