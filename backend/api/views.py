from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, UserProfile, Crypto, CryptoBalance, Transaction
from .serializers import UserProfileSerializer, CryptoBalanceSerializer, CryptoBalanceSummarySerializer, TransactionSerializer
from .crypto import CryptoHandler

crypto_handler = CryptoHandler()

class UserProfileBalanceView(APIView):
    def get(self, request):
        username = request.GET.get("username")
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        crypto_balances = CryptoBalance.objects.filter(user_profile=user_profile)
        serializer = CryptoBalanceSummarySerializer(crypto_balances, many=True)
        serialized_data = serializer.data
        serialized_data.append({"Blu": user_profile.balance})        
        return Response(serialized_data)


class UserProfileBalanceView(APIView):
    def get(self, request):
        username = request.GET.get("username")
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        crypto_balances = CryptoBalance.objects.filter(user_profile=user_profile)
        output = dict()
        output['blu'] = user_profile.balance
        for crypto_balance in crypto_balances:
            crypto_name = crypto_balance.crypto.symbol
            output[crypto_name] = crypto_balance.balance

        return Response(output)


class TransactionCreateView(APIView):
    def post(self, request):
        username = request.GET.get("username")
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        crypto_symbol = request.GET.get('crypto_symbol')
        transaction_type = request.GET.get('transaction_type')
        amount = Decimal(request.GET.get('amount'))

        crypto = Crypto.objects.get(symbol=crypto_symbol)
        if transaction_type == 'buy':
            crypto_balance, created = CryptoBalance.objects.get_or_create(user_profile=user_profile, crypto=crypto)
            if amount > user_profile.balance:
                return Response({'detail': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)
            amount_in_crypto = crypto_handler.convert_blu_to_crypto(amount, crypto_symbol)
            crypto_balance.balance += Decimal(amount_in_crypto)
            crypto_balance.save()
            user_profile.balance -= amount
            user_profile.save()
            Transaction.objects.create(user_profile=user_profile, crypto=crypto, amount=amount)
        elif transaction_type == 'sell':
            amount_in_blu = crypto_handler.convert_crypto_to_blu(amount, crypto_symbol)
            crypto_balance = CryptoBalance.objects.get(user_profile=user_profile, crypto=crypto)
            if crypto_balance.balance < amount:
                return Response({'detail': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)
            crypto_balance.balance -= amount
            crypto_balance.save()
            user_profile.balance += Decimal(amount_in_blu)
            user_profile.save()
            Transaction.objects.create(user_profile=user_profile, crypto=crypto, amount=-amount)
        else:
            return Response({'detail': 'Invalid transaction type.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Transaction successful.'}, status=status.HTTP_201_CREATED)
    
    
class ConvertCurrencyView(APIView):
    def get(self, request):
        amount = request.GET.get("amount")
        from_crypto = request.GET.get("from_crypto_symbol")
        to_crypto = request.GET.get("to_crypto_symbol")
        
        if from_crypto == 'blu':
            converted_amount = crypto_handler.convert_blu_to_crypto(amount, to_crypto)
        elif to_crypto == 'blu':
            converted_amount = crypto_handler.convert_crypto_to_blu(amount, from_crypto)
        else:
            return Response({'detail': 'One element must be "blu".'}, status=status.HTTP_400_BAD_REQUEST)
            
        output = dict()
        output['from'] = from_crypto
        output['to'] = to_crypto
        output['converted_amount'] = converted_amount
        
        return Response(output)
    
class CurrentValueView(APIView):
    def get(self, request):
        crypto_symbol = request.GET.get("crypto_symbol")
        if request.GET.get("in_blu"):
            return Response({"blu": crypto_handler.convert_crypto_to_blu(1, crypto_symbol)})
        return Response(crypto_handler.get_current_value(crypto_symbol))
    
    
class AllCryptosView(APIView):
    def get(self, request):
        cryptos = Crypto.objects.all().values('name', 'symbol')
        return Response(list(cryptos))