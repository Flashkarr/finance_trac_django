from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name


class Wallet(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='wallets'
    )

    BANK_CHOICES = [
        ('mono', 'Monobank'),
        ('privat', 'PrivatBank'),
        ('cash', 'Готівка'),
        ('other', 'Інше'),
    ]

    name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=20, choices=BANK_CHOICES)

    card_number = models.CharField(max_length=19, blank=True)
    expiry_date = models.CharField(max_length=5, blank=True)
    cvv_demo = models.CharField(max_length=3, blank=True)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='UAH')

    def masked_card(self):
        if self.card_number:
            return '**** **** **** ' + self.card_number[-4:]
        return 'Без карти'

    def __str__(self):
        return self.name


class Category(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'

    CATEGORY_TYPES = [
        (INCOME, 'Дохід'),
        (EXPENSE, 'Витрата'),
    ]

    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'

    TRANSACTION_TYPES = [
        (INCOME, 'Дохід'),
        (EXPENSE, 'Витрата'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    transaction_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)
    is_auto = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Budget(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)


class SavingJar(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title