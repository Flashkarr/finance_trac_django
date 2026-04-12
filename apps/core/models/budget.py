from django.db import models


class Budget(models.Model):
    title = models.CharField(max_length=100)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount_limit}"