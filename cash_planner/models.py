from django.db import models
from django.utils import timezone

# Create your models here.

class MainCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', '現金'),
        ('credit', 'クレジットカード'),
        ('cashless', 'キャッシュレス決済'),
    ]

    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cash')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.amount} - {self.main_category} - {self.date}"

class Income(models.Model):
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)

class Patience(models.Model):
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=50)

class UserInfo(models.Model):
    mbti = models.CharField(max_length=4)
    occupation = models.CharField(max_length=100)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expenses = models.TextField()
    payment = models.CharField(max_length=50)
    savings = models.DecimalField(max_digits=10, decimal_places=2)
    goal = models.CharField(max_length=255)
    personality = models.CharField(max_length=50)
    awareness = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.occupation}'
