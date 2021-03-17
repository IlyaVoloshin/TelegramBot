import json
import requests

from config import exchanger

class ConverterException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise ConverterException("Неверное количество параметров")
        qoute, base, amount = values

        if qoute == base:
            raise ConverterException(f'Невозмоно перевести одинаковые валюты {base}')

        try:
            qoute_formatted = exchanger[qoute]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту {qoute}')

        try:
            base_formatted = exchanger[base]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConverterException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latesr?base={qoute_formatted}&synbols={base_formatted}')

        result = float(json.loads(r.content)['rates'][base_formatted])*amount

        return round(result, 3)
