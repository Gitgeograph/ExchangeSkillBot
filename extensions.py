import requests
import json
from config import keys


class APIExeption(Exception):
    pass


class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote.lower() == base.lower():
            raise APIExeption(f'Невозможно перевести одинаковые валюты: {base}\nВзгляни сюда /help')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту: {base}\nВзгляни сюда /help')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту: {quote}\nВзгляни сюда /help')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f"Не удалось обработать количество: {amount}\nВзгляни сюда /help")


        url = f'https://api.apilayer.com/exchangerates_data/convert?to={quote_ticker}&from={base_ticker}&amount={amount}'
        payload = {}
        headers = {
            'apikey': 'S1uVLEz3t4agwdAeNWXL0g0ugHzYimCL'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        res = json.loads(response.content)
        result = round(res['result'], 2)
        return result
