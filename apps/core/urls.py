from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('about/', views.about_view, name='about_project'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('wallets/', views.wallets_view, name='wallets'),
    path('wallets/edit/<int:pk>/', views.wallet_edit_view, name='wallet_edit'),
    path('wallets/delete/<int:pk>/', views.wallet_delete_view, name='wallet_delete'),

    path('categories/', views.categories_view, name='categories'),
    path('categories/edit/<int:pk>/', views.category_edit_view, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete_view, name='category_delete'),

    path('payment-methods/', views.payment_methods_view, name='payment_methods'),
    path('payment-methods/edit/<int:pk>/', views.payment_method_edit_view, name='payment_method_edit'),
    path('payment-methods/delete/<int:pk>/', views.payment_method_delete_view, name='payment_method_delete'),

    path('saving-jars/', views.saving_jars_view, name='saving_jars'),
    path('saving-jars/delete/<int:pk>/', views.saving_jar_delete_view, name='saving_jar_delete'),

    path('transactions/', views.transactions_view, name='transactions'),
    path('transactions/edit/<int:pk>/', views.transaction_edit_view, name='transaction_edit'),
    path('transactions/delete/<int:pk>/', views.transaction_delete_view, name='transaction_delete'),
]