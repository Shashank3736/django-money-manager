from django.db import models
from account.models import CustomUser as User

# Create your models here.
class Profile(models.Model):
    profile_pic = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
