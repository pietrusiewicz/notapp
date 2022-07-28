import datetime

from django.db import models
from django.utils import timezone

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    last_usage = models.DateTimeField('date_published')

    def __str__(self):
        return self.category_name

    def used_last_year(self):
        return self.last_usage >= timezone.now() - datetime.timedelta(days=365)

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.item_name
