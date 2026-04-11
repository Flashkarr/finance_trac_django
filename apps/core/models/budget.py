from django.db import models


class Budget(models.Model):
    title = models.CharField(max_length=100)
    limit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.limit_amount}"