from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from account.models import CustomUser as User
import os

# Create your models here.
class Profile(models.Model):
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)

    def save(self, *args, **kwargs) -> None:
        if self.profile_pic and self.profile_pic.size > 1024*1024:
            raise ValidationError('File size must be smaller than 1mb.')
        return super().save(*args, **kwargs)

@receiver(pre_delete, sender=Profile)
def delete_image(sender, instance, **kwargs):
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)

@receiver(pre_save, sender=Profile)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            # Retrieve the existing instance from the database
            old_instance = sender.objects.get(pk=instance.pk)
            # Check if the image field has changed
            if old_instance.profile_pic != instance.profile_pic:
                # Delete the old profile_pic file from the storage
                if old_instance.profile_pic:
                    if os.path.isfile(old_instance.profile_pic.path):
                        os.remove(old_instance.profile_pic.path)
        except sender.DoesNotExist:
            pass