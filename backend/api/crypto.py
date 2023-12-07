import cryptocompare

class CryptoHandler:
    def __init__(self):
        api_key = 'c442457b0db47632cb208c42dd7a1063fff2f893617b5fe8872c8e99a1815aea'
        cryptocompare.cryptocompare._set_api_key_parameter(api_key)
        self.blu_value_in_usd = 1000

    def get_current_value(self, crypto_symbol):
        if crypto_symbol.lower() == "blu":
            return {"USD": self.blu_value_in_usd}
        crypto_symbol = crypto_symbol.upper()
        output = cryptocompare.get_price(crypto_symbol, currency='USD')[crypto_symbol]
        output["USD"] = round(output["USD"], 3)
        return cryptocompare.get_price(crypto_symbol, currency='USD')[crypto_symbol]


    def convert_crypto_to_blu(self, amount, from_crypto_symbol):
        crypto_in_usd = self.get_current_value(from_crypto_symbol)["USD"]
        amount_in_crypto = int(amount) * crypto_in_usd / self.blu_value_in_usd
        return round(amount_in_crypto, 2)
        
    def convert_blu_to_crypto(self, amount, to_crypto_symbol):
        crypto_in_usd = self.get_current_value(to_crypto_symbol)["USD"]
        amount_in_crypto = int(amount) * self.blu_value_in_usd / crypto_in_usd
        return round(amount_in_crypto, 2)