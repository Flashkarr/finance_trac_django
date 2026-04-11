from django.db import models


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    provider = models.CharField(max_length=50)
    account_number = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.provider}"