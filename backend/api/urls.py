from django.urls import path

from . import views

from django.urls import path
from .views import UserProfileBalanceView, TransactionCreateView, ConvertCurrencyView, CurrentValueView, AllCryptosView

urlpatterns = [
    path('balance/', UserProfileBalanceView.as_view(), name='user_balance'),
    path('transaction/create/', TransactionCreateView.as_view(), name='create_transaction'),
    path('convert/', ConvertCurrencyView.as_view(), name='covert_currency'),
    path('current/', CurrentValueView.as_view(), name='current value of crypto'),
    path('all_cryptos/', AllCryptosView.as_view(), name='all cryptos'),
]