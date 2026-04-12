from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    category_type = models.CharField(
        max_length=20,
        choices=[
            ('income', 'Income'),
            ('expense', 'Expense'),
        ]
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.category_type}"