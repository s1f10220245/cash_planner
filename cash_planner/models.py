from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    INCOME = 'IN'
    EXPENSE = 'EX'
    TRANSACTION_TYPES = [
        (INCOME, '収入'),
        (EXPENSE, '支出'),
    ]
    
    date = models.DateField(default=timezone.now)
    type = models.CharField(max_length=2, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} - {self.description}"