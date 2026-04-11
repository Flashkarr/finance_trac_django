from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.category_type})"