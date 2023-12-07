from django.contrib import admin

from .models import User, UserProfile, Crypto, CryptoBalance, Transaction

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Crypto)
admin.site.register(CryptoBalance)
admin.site.register(Transaction)