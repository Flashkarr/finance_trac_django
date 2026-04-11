from django.db import models


class Transaction(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    transaction_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.amount}"