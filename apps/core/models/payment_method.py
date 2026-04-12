from django.db import models


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name