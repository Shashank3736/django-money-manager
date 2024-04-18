from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from account.models import CustomUser as User
import uuid, os

# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

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