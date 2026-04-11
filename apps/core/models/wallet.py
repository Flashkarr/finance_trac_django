from django.db import models


class Wallet(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.balance} {self.currency}"