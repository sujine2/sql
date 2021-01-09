from django.db import models
from django.conf import settings
from django.utils import timezone


class list (models.Model):
    query = models.TextField(unique=True)
    stand = models.TextField(unique=False)

    def __str__(self):
        return self.query