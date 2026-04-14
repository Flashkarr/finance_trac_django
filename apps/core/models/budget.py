from django.db import models
from .user_profile import UserProfile
from .category import Category


class Budget(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    title = models.CharField(max_length=100)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount_limit}"