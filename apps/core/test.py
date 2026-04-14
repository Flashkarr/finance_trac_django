from datetime import date
from django.test import TestCase

from apps.core.models import (
    UserProfile,
    Wallet,
    Category,
    PaymentMethod,
    Budget,
    Transaction,
)


class TestUserProfile(TestCase):
    def setUp(self):
        self.user_data = {
            "full_name": "Ivan Petrenko",
            "email": "ivan@example.com",
            "phone": "+380991112233",
        }
        self.user = UserProfile.objects.create(**self.user_data)

    def test_create_user_profile(self):
        saved_user = UserProfile.objects.get(id=self.user.id)
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.full_name, self.user_data["full_name"])
        self.assertEqual(saved_user.email, self.user_data["email"])
        self.assertEqual(saved_user.phone, self.user_data["phone"])

    def test_update_user_profile(self):
        self.user.full_name = "Petro Ivanenko"
        self.user.phone = "+380992223344"
        self.user.save()

        updated_user = UserProfile.objects.get(id=self.user.id)
        self.assertEqual(updated_user.full_name, "Petro Ivanenko")
        self.assertEqual(updated_user.phone, "+380992223344")

    def test_delete_user_profile(self):
        user_id = self.user.id
        self.user.delete()

        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=user_id)


class TestCategory(TestCase):
    def setUp(self):
        self.category_data = {
            "name": "Food",
            "category_type": "expense",
            "description": "Food expenses",
        }
        self.category = Category.objects.create(**self.category_data)

    def test_create_category(self):
        saved_category = Category.objects.get(id=self.category.id)
        self.assertIsNotNone(saved_category)
        self.assertEqual(saved_category.name, self.category_data["name"])
        self.assertEqual(saved_category.category_type, self.category_data["category_type"])
        self.assertEqual(saved_category.description, self.category_data["description"])

    def test_update_category(self):
        self.category.name = "Transport"
        self.category.category_type = "expense"
        self.category.description = "Transport expenses"
        self.category.save()

        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.name, "Transport")
        self.assertEqual(updated_category.description, "Transport expenses")

    def test_delete_category(self):
        category_id = self.category.id
        self.category.delete()

        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category_id)


class TestPaymentMethod(TestCase):
    def setUp(self):
        self.payment_method_data = {
            "name": "Bank Card",
            "details": "Visa card",
        }
        self.payment_method = PaymentMethod.objects.create(**self.payment_method_data)

    def test_create_payment_method(self):
        saved_payment_method = PaymentMethod.objects.get(id=self.payment_method.id)
        self.assertIsNotNone(saved_payment_method)
        self.assertEqual(saved_payment_method.name, self.payment_method_data["name"])
        self.assertEqual(saved_payment_method.details, self.payment_method_data["details"])

    def test_update_payment_method(self):
        self.payment_method.name = "Cash"
        self.payment_method.details = "Cash payment"
        self.payment_method.save()

        updated_payment_method = PaymentMethod.objects.get(id=self.payment_method.id)
        self.assertEqual(updated_payment_method.name, "Cash")
        self.assertEqual(updated_payment_method.details, "Cash payment")

    def test_delete_payment_method(self):
        payment_method_id = self.payment_method.id
        self.payment_method.delete()

        with self.assertRaises(PaymentMethod.DoesNotExist):
            PaymentMethod.objects.get(id=payment_method_id)


class TestWallet(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            full_name="Ivan Petrenko",
            email="ivan_wallet@example.com",
            phone="+380991112233"
        )

        self.wallet_data = {
            "user": self.user,
            "name": "Main Wallet",
            "balance": 1500.50,
            "currency": "UAH",
        }
        self.wallet = Wallet.objects.create(**self.wallet_data)

    def test_create_wallet(self):
        saved_wallet = Wallet.objects.get(id=self.wallet.id)
        self.assertIsNotNone(saved_wallet)
        self.assertEqual(saved_wallet.user, self.user)
        self.assertEqual(saved_wallet.name, self.wallet_data["name"])
        self.assertEqual(saved_wallet.balance, self.wallet_data["balance"])
        self.assertEqual(saved_wallet.currency, self.wallet_data["currency"])

    def test_update_wallet(self):
        self.wallet.name = "Updated Wallet"
        self.wallet.balance = 2000.00
        self.wallet.save()

        updated_wallet = Wallet.objects.get(id=self.wallet.id)
        self.assertEqual(updated_wallet.name, "Updated Wallet")
        self.assertEqual(updated_wallet.balance, 2000.00)

    def test_delete_wallet(self):
        wallet_id = self.wallet.id
        self.wallet.delete()

        with self.assertRaises(Wallet.DoesNotExist):
            Wallet.objects.get(id=wallet_id)


class TestBudget(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            full_name="Olena Kovalenko",
            email="olena_budget@example.com",
            phone="+380993334455"
        )

        self.category = Category.objects.create(
            name="Products",
            category_type="expense",
            description="Daily products"
        )

        self.budget_data = {
            "user": self.user,
            "category": self.category,
            "title": "Monthly Food Budget",
            "amount_limit": 5000.00,
            "start_date": date(2025, 4, 1),
            "end_date": date(2025, 4, 30),
            "comment": "Budget for April",
        }
        self.budget = Budget.objects.create(**self.budget_data)

    def test_create_budget(self):
        saved_budget = Budget.objects.get(id=self.budget.id)
        self.assertIsNotNone(saved_budget)
        self.assertEqual(saved_budget.user, self.user)
        self.assertEqual(saved_budget.category, self.category)
        self.assertEqual(saved_budget.title, self.budget_data["title"])
        self.assertEqual(saved_budget.amount_limit, self.budget_data["amount_limit"])
        self.assertEqual(saved_budget.start_date, self.budget_data["start_date"])
        self.assertEqual(saved_budget.end_date, self.budget_data["end_date"])
        self.assertEqual(saved_budget.comment, self.budget_data["comment"])

    def test_update_budget(self):
        self.budget.title = "Updated Budget"
        self.budget.amount_limit = 6000.00
        self.budget.comment = "Updated comment"
        self.budget.save()

        updated_budget = Budget.objects.get(id=self.budget.id)
        self.assertEqual(updated_budget.title, "Updated Budget")
        self.assertEqual(updated_budget.amount_limit, 6000.00)
        self.assertEqual(updated_budget.comment, "Updated comment")

    def test_delete_budget(self):
        budget_id = self.budget.id
        self.budget.delete()

        with self.assertRaises(Budget.DoesNotExist):
            Budget.objects.get(id=budget_id)


class TestTransaction(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            full_name="Andrii Melnyk",
            email="andrii_transaction@example.com",
            phone="+380995556677"
        )

        self.wallet = Wallet.objects.create(
            user=self.user,
            name="Card Wallet",
            balance=2500.00,
            currency="UAH"
        )

        self.category = Category.objects.create(
            name="Salary",
            category_type="income",
            description="Monthly salary"
        )

        self.payment_method = PaymentMethod.objects.create(
            name="Bank Transfer",
            details="Transfer to card"
        )

        self.transaction_data = {
            "wallet": self.wallet,
            "category": self.category,
            "payment_method": self.payment_method,
            "title": "April Salary",
            "amount": 18000.00,
            "transaction_type": "income",
            "transaction_date": date(2025, 4, 10),
            "note": "Salary for April",
        }
        self.transaction = Transaction.objects.create(**self.transaction_data)

    def test_create_transaction(self):
        saved_transaction = Transaction.objects.get(id=self.transaction.id)
        self.assertIsNotNone(saved_transaction)
        self.assertEqual(saved_transaction.wallet, self.wallet)
        self.assertEqual(saved_transaction.category, self.category)
        self.assertEqual(saved_transaction.payment_method, self.payment_method)
        self.assertEqual(saved_transaction.title, self.transaction_data["title"])
        self.assertEqual(saved_transaction.amount, self.transaction_data["amount"])
        self.assertEqual(saved_transaction.transaction_type, self.transaction_data["transaction_type"])
        self.assertEqual(saved_transaction.transaction_date, self.transaction_data["transaction_date"])
        self.assertEqual(saved_transaction.note, self.transaction_data["note"])

    def test_update_transaction(self):
        self.transaction.title = "Updated Salary"
        self.transaction.amount = 19000.00
        self.transaction.note = "Updated note"
        self.transaction.save()

        updated_transaction = Transaction.objects.get(id=self.transaction.id)
        self.assertEqual(updated_transaction.title, "Updated Salary")
        self.assertEqual(updated_transaction.amount, 19000.00)
        self.assertEqual(updated_transaction.note, "Updated note")

    def test_delete_transaction(self):
        transaction_id = self.transaction.id
        self.transaction.delete()

        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(id=transaction_id)