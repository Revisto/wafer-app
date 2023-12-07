from rest_framework import serializers
from .models import UserProfile, Crypto, CryptoBalance, Transaction

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('balance',)

class CryptoBalanceSummarySerializer(serializers.ModelSerializer):
    crypto_symbol = serializers.CharField(source='crypto.symbol')
    crypto_name = serializers.CharField(source='crypto.name')
    balance = serializers.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        model = CryptoBalance
        fields = ('crypto_symbol', 'crypto_name', 'balance')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        crypto_name = data['crypto_name']
        crypto_symbol = data['balance']
        balance = data['balance']
        return {crypto_symbol: balance}
    
    
class CryptoBalanceSerializer(serializers.ModelSerializer):
    crypto_name = serializers.CharField(source='crypto.name', read_only=True)
    crypto_symbol = serializers.CharField(source='crypto.symbol', read_only=True)

    class Meta:
        model = CryptoBalance
        fields = ('crypto_name', 'crypto_symbol', 'balance')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('crypto', 'amount', 'timestamp')