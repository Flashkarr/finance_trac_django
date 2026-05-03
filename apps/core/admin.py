from django.contrib import admin

from .models import (
    UserProfile,
    Wallet,
    Category,
    PaymentMethod,
    Budget,
    Transaction,
    SavingJar,
)

admin.site.register(UserProfile)
admin.site.register(Wallet)
admin.site.register(Category)
admin.site.register(PaymentMethod)
admin.site.register(Budget)
admin.site.register(Transaction)
admin.site.register(SavingJar)