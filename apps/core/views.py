from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Wallet, Category, PaymentMethod, Transaction, SavingJar


def welcome_view(request):
    return render(request, 'core/welcome.html')


def about_view(request):
    return render(request, 'about-project.html')


def get_or_create_profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.username,
            'email': request.user.email or f'{request.user.username}@example.com',
            'phone': '0000000000',
        }
    )
    return profile

def get_system_category(transaction_type):
    category, created = Category.objects.get_or_create(
        name='Системні операції',
        category_type=transaction_type
    )
    return category


def get_system_payment_method():
    payment_method, created = PaymentMethod.objects.get_or_create(
        name='Автоматично'
    )
    return payment_method


def create_auto_transaction(wallet, title, amount, transaction_type, note=''):
    Transaction.objects.create(
        wallet=wallet,
        category=get_system_category(transaction_type),
        payment_method=get_system_payment_method(),
        title=title,
        amount=amount,
        transaction_type=transaction_type,
        transaction_date=date.today(),
        note=note,
        is_auto=True
    )

@login_required
def dashboard_view(request):
    profile = get_or_create_profile(request)
    wallets = Wallet.objects.filter(user=profile)
    transactions = Transaction.objects.filter(wallet__user=profile).order_by('-created_at')
    saving_jars = SavingJar.objects.filter(user=profile)

    total_balance = sum(wallet.balance for wallet in wallets)
    total_savings = sum(jar.current_amount for jar in saving_jars)

    return render(request, 'core/dashboard.html', {
        'profile': profile,
        'wallets': wallets,
        'transactions': transactions,
        'saving_jars': saving_jars,
        'total_balance': total_balance,
        'total_savings': total_savings,
    })


@login_required
def wallets_view(request):
    profile = get_or_create_profile(request)

    if request.method == 'POST':
        wallet = Wallet(
            user=profile,
            name=request.POST.get('name'),
            bank_name=request.POST.get('bank_name'),
            card_number=request.POST.get('card_number'),
            expiry_date=request.POST.get('expiry_date'),
            cvv_demo=request.POST.get('cvv_demo'),
            balance=request.POST.get('balance') or 0,
            currency=request.POST.get('currency') or 'UAH',
        )
        wallet.full_clean()
        wallet.save()

        if wallet.balance > 0:
            create_auto_transaction(
                wallet=wallet,
                title='Початковий баланс карти',
                amount=wallet.balance,
                transaction_type=Transaction.INCOME,
                note='Карта була прив’язана до акаунта'
            )

        return redirect('wallets')

    wallets = Wallet.objects.filter(user=profile)
    return render(request, 'core/wallets.html', {
        'wallets': wallets,
        'bank_choices': Wallet.BANK_CHOICES,
    })


@login_required
def wallet_edit_view(request, pk):
    profile = get_or_create_profile(request)
    wallet = get_object_or_404(Wallet, pk=pk, user=profile)

    old_balance = wallet.balance

    wallet.name = request.POST.get('name')
    wallet.bank_name = request.POST.get('bank_name') or wallet.bank_name
    wallet.card_number = request.POST.get('card_number')
    wallet.expiry_date = request.POST.get('expiry_date')
    wallet.cvv_demo = request.POST.get('cvv_demo')
    wallet.balance = Decimal(request.POST.get('balance') or 0)
    wallet.currency = request.POST.get('currency') or 'UAH'

    wallet.full_clean()
    wallet.save()

    difference = wallet.balance - old_balance

    if difference > 0:
        create_auto_transaction(
            wallet=wallet,
            title='Поповнення балансу',
            amount=difference,
            transaction_type=Transaction.INCOME,
            note='Баланс карти було змінено вручну'
        )

    elif difference < 0:
        create_auto_transaction(
            wallet=wallet,
            title='Зменшення балансу',
            amount=abs(difference),
            transaction_type=Transaction.EXPENSE,
            note='Баланс карти було змінено вручну'
        )

    return redirect('wallets')

    return render(request, 'core/wallet_form.html', {'wallet': wallet})


@login_required
def wallet_delete_view(request, pk):
    profile = get_or_create_profile(request)
    wallet = get_object_or_404(Wallet, pk=pk, user=profile)
    wallet.delete()
    return redirect('wallets')


@login_required
def categories_view(request):
    if request.method == 'POST':
        category = Category(
            name=request.POST.get('name'),
            category_type=request.POST.get('category_type'),
            description=request.POST.get('description'),
        )
        category.full_clean()
        category.save()
        return redirect('categories')

    categories = Category.objects.all()
    return render(request, 'core/categories.html', {
        'categories': categories,
        'category_types': Category.CATEGORY_TYPES,
    })


@login_required
def category_edit_view(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.category_type = request.POST.get('category_type')
        category.description = request.POST.get('description')
        category.full_clean()
        category.save()
        return redirect('categories')

    return render(request, 'core/category_form.html', {
        'category': category,
        'category_types': Category.CATEGORY_TYPES,
    })


@login_required
def category_delete_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')


@login_required
def payment_methods_view(request):
    if request.method == 'POST':
        payment_method = PaymentMethod(
            name=request.POST.get('name'),
            details=request.POST.get('details'),
        )
        payment_method.full_clean()
        payment_method.save()
        return redirect('payment_methods')

    payment_methods = PaymentMethod.objects.all()
    return render(request, 'core/payment_methods.html', {
        'payment_methods': payment_methods,
    })


@login_required
def payment_method_edit_view(request, pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk)

    if request.method == 'POST':
        payment_method.name = request.POST.get('name')
        payment_method.details = request.POST.get('details')
        payment_method.full_clean()
        payment_method.save()
        return redirect('payment_methods')

    return render(request, 'core/payment_method_form.html', {
        'payment_method': payment_method,
    })


@login_required
def payment_method_delete_view(request, pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk)
    payment_method.delete()
    return redirect('payment_methods')


def update_wallet_balance(transaction, old_transaction=None):
    wallet = transaction.wallet

    if old_transaction:
        if old_transaction.transaction_type == Transaction.INCOME:
            wallet.balance -= old_transaction.amount
        else:
            wallet.balance += old_transaction.amount

    if transaction.transaction_type == Transaction.INCOME:
        wallet.balance += transaction.amount
    else:
        wallet.balance -= transaction.amount

    wallet.save()


@login_required
def transactions_view(request):
    profile = get_or_create_profile(request)

    wallets = Wallet.objects.filter(user=profile)
    categories = Category.objects.all()
    payment_methods = PaymentMethod.objects.all()

    if request.method == 'POST':
        transaction = Transaction(
            wallet_id=request.POST.get('wallet'),
            category_id=request.POST.get('category'),
            payment_method_id=request.POST.get('payment_method'),
            title=request.POST.get('title'),
            amount=request.POST.get('amount') or 0,
            transaction_type=request.POST.get('transaction_type'),
            transaction_date=request.POST.get('transaction_date') or date.today(),
            note=request.POST.get('note'),
        )
        transaction.full_clean()
        transaction.save()
        update_wallet_balance(transaction)
        return redirect('transactions')

    transactions = Transaction.objects.filter(wallet__user=profile).order_by('-created_at')

    return render(request, 'core/transactions.html', {
        'transactions': transactions,
        'wallets': wallets,
        'categories': categories,
        'payment_methods': payment_methods,
        'transaction_types': Transaction.TRANSACTION_TYPES,
    })


@login_required
def transaction_edit_view(request, pk):
    profile = get_or_create_profile(request)
    transaction = get_object_or_404(Transaction, pk=pk, wallet__user=profile)

    wallets = Wallet.objects.filter(user=profile)
    categories = Category.objects.all()
    payment_methods = PaymentMethod.objects.all()

    if request.method == 'POST':
        old_transaction = Transaction.objects.get(pk=transaction.pk)

        transaction.wallet_id = request.POST.get('wallet')
        transaction.category_id = request.POST.get('category')
        transaction.payment_method_id = request.POST.get('payment_method')
        transaction.title = request.POST.get('title')
        transaction.amount = Decimal(request.POST.get('amount') or 0)
        transaction.transaction_type = request.POST.get('transaction_type')
        transaction.transaction_date = request.POST.get('transaction_date') or date.today()
        transaction.note = request.POST.get('note')

        transaction.full_clean()
        transaction.save()
        update_wallet_balance(transaction, old_transaction)
        return redirect('transactions')

    return render(request, 'core/transaction_form.html', {
        'transaction': transaction,
        'wallets': wallets,
        'categories': categories,
        'payment_methods': payment_methods,
        'transaction_types': Transaction.TRANSACTION_TYPES,
    })


@login_required
def transaction_delete_view(request, pk):
    profile = get_or_create_profile(request)
    transaction = get_object_or_404(Transaction, pk=pk, wallet__user=profile)

    wallet = transaction.wallet
    if transaction.transaction_type == Transaction.INCOME:
        wallet.balance -= transaction.amount
    else:
        wallet.balance += transaction.amount
    wallet.save()

    transaction.delete()
    return redirect('transactions')

@login_required
def saving_jars_view(request):
    profile = get_or_create_profile(request)
    wallets = Wallet.objects.filter(user=profile)

    if request.method == 'POST':
        wallet = get_object_or_404(Wallet, id=request.POST.get('wallet'), user=profile)
        amount = Decimal(request.POST.get('current_amount') or 0)

        if wallet.balance >= amount:
            wallet.balance -= amount
            wallet.save()

            jar = SavingJar.objects.create(
                user=profile,
                wallet=wallet,
                title=request.POST.get('title'),
                goal_amount=request.POST.get('goal_amount') or 0,
                current_amount=amount,
            )

            create_auto_transaction(
                wallet=wallet,
                title=f'Переказ у банку: {jar.title}',
                amount=amount,
                transaction_type=Transaction.EXPENSE,
                note='Гроші перенесено з карти у банку накопичення'
            )

        return redirect('saving_jars')

    saving_jars = SavingJar.objects.filter(user=profile)

    return render(request, 'core/saving_jars.html', {
        'saving_jars': saving_jars,
        'wallets': wallets,
    })


@login_required
def saving_jar_delete_view(request, pk):
    profile = get_or_create_profile(request)
    jar = get_object_or_404(SavingJar, pk=pk, user=profile)

    wallet = jar.wallet
    wallet.balance += jar.current_amount
    wallet.save()

    create_auto_transaction(
        wallet=wallet,
        title=f'Повернення з банки: {jar.title}',
        amount=jar.current_amount,
        transaction_type=Transaction.INCOME,
        note='Гроші повернено з банки на карту'
    )

    jar.delete()
    return redirect('saving_jars')