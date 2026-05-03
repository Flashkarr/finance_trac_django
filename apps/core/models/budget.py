from django.db import models
from django.conf import settings
from .category import Category


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField()
    end_date = models.DateField()

    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title