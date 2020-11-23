from django.db import models
from django.conf import settings
from django.utils import timezone


class list (models.Model):
    query = models.TextField(unique=True)
    stand = models.TextField(null=True, max_length=200 )

    def __str__(self):
        return self.query