from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True)
