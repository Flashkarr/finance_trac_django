from django.contrib import admin
from .models import UserProfile, Wallet, Category, Transaction, Budget, PaymentMethod

admin.site.register(UserProfile)
admin.site.register(Wallet)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(PaymentMethod)