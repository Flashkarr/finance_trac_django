from django.db import models


class Transaction(models.Model):
    title = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ('income', 'Income'),
            ('expense', 'Expense'),
        ]
    )
    transaction_date = models.DateField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"