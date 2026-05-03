from django.shortcuts import render, redirect
from .models.transaction import Transaction
from .models.wallet import Wallet
from .models.category import Category

def add_transaction(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        type = request.POST.get('type')
        category_id = request.POST.get('category')

        wallet = Wallet.objects.filter(user=request.user).first()
        category = Category.objects.get(id=category_id)

        Transaction.objects.create(
            user=request.user,
            wallet=wallet,
            category=category,
            amount=amount,
            type=type
        )

        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'core/add_transaction.html', {'categories': categories})