import uuid
from django.db import models
from account.models import CustomUser as User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

# Create your models here.
class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=32)
    balance = models.FloatField(default=0)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')

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
    image = models.ImageField(upload_to='media/transactions', null=True)

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        if self.image and self.image.size > 1024*1024:
            raise ValidationError("File must be shorter than 1mb.")
        if self.type == 'income':
            self.account.balance += self.amount
            self.category = None
        elif self.type == 'expense':
            self.account.balance -= self.amount
        self.account.save()
        super().save(*args, **kwargs)

@receiver(pre_delete, sender=Transaction)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Transaction)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            # Retrieve the existing instance from the database
            old_instance = sender.objects.get(pk=instance.pk)
            # Check if the image field has changed
            if old_instance.image != instance.image:
                # Delete the old image file from the storage
                if old_instance.image:
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
        except sender.DoesNotExist:
            pass