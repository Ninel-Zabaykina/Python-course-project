from django.db import models
from django.utils import timezone


class Client(models.Model):
    surname = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    otchestvo = models.CharField(max_length=40)
    birthday = models.DateField()
    parent_name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=40)
    date_of_reference = models.DateField()
    disabled = models.BooleanField()
    have_many_children = models.BooleanField()

    @property
    def since(self):
        return (timezone.now().date() - self.date_of_reference).days
