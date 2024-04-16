from django.db import models
from account.models import CustomUser as User
import uuid

# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
