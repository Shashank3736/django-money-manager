from typing import Collection, Iterable
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
    
    def save(self, *args, **kwargs) -> None:
        if self._state.adding and self.category == None and Budgets.objects.filter(user=self.user, category=None).count() > 0:
            raise ValidationError("Budgest can only have one budget with no category.") 
        if self.category and self.category.user != self.user:
            raise ValidationError("User do not own the category.")
        
        if self.amount < 0:
            raise ValidationError("Amount need to be greater than zero.")
        return super().save(*args, **kwargs)