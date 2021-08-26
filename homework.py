import datetime as dt  # for data type to be used
from typing import List, Optional  # for showing type of the variable
# TODO/ grab usd and euro rate from web
# import requests
# from bs4 import BeautifulSoup as bs


class Calculator():
    """Main class for both calculators.
       Parent class to CashCalculator
       and CaloriesCalculator."""
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records: List['Record'] = []

    def add_record(self, inp_record: 'Record') -> bool:
        """Adds object of type record to the list."""
        self.records.append(inp_record)
        return True

    def get_today_stats(self) -> float:
        """Counts amount of money/calories used
           used up in a day."""
        count_day: float = 0
        dt_now = dt.datetime.now()

        # Summ all records of amount (callories/Cash) where day = today.
        for record in self.records:
            if record.date == dt_now.date():
                count_day = count_day + record.amount

        return count_day

    def get_week_stats(self):
        """Counts amount of money/calories used
           used up in a week."""

        week_ago: dt.datetime = dt.datetime.now() - dt.timedelta(days=7)
        week_ago: dt.date = week_ago.date()
        count_week: float = 0

        # Summ all records of amount (callories/Cash) where
        # day = one of the previous 7 days inclusive.
        for record in self.records:
            if (record.date >= week_ago and record.date
               <= dt.datetime.now().date()):
                count_week = count_week + record.amount

        return count_week


class CashCalculator(Calculator):
    """Representing calculator for
       money management."""
    USD_RATE = 73.72
    EURO_RATE = 86.60

    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def converter(self, currencyTo: str, inpAmount: float) -> float:
        """Converst rubles to dollars or euro using information
           from yandex.ru and returns answer to 2dp."""

        # TODO/ Grab usd and euro rate from web.
        # url = 'https://yandex.ru/'
        # headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        #            + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.'
        #            + '0.4515.159 Safari/537.36'}
        # parse = requests.get(url, headers)
        # soup = bs(parse.content, 'html.parser')
        # stoks = soup.findAll("span", {'class': 'inline-stocks__value_inner'})
        # usd_rate = float(stoks[0].text.replace(',', '.'))
        # eur_rate = float(stoks[1].text.replace(',', '.'))

        usd_rate = self.USD_RATE
        eur_rate = self.EURO_RATE
        usd_converted = inpAmount / usd_rate
        eur_converted = inpAmount / eur_rate
        usd_converted = (round(usd_converted, 2))
        eur_converted = (round(eur_converted, 2))

        if currencyTo == 'usd':
            return usd_converted
        elif currencyTo == 'eur':
            return eur_converted

    def get_today_cash_remained(self, currency: str) -> str:
        """Shows how much money is left to spend for today."""
        lmt = self.limit
        gts = self.get_today_stats()
        remaining: float = lmt - gts
        debt: float = gts - lmt

        # Convert currency and rename for better look.
        # Raises error if gets unknown currency.
        if currency == 'eur':
            remaining = self.converter(currency, remaining)
            debt = self.converter(currency, debt)
            currency = 'Euro'
        elif currency == 'usd':
            remaining = self.converter(currency, remaining)
            debt = self.converter(currency, debt)
            currency = 'USD'
        elif currency == 'rub':
            currency = 'руб'
        else:
            raise ValueError('такая валюта не доступна')

        # Compere's money spends today and comperes to limit that was set.
        # Returns msg string accordingly.
        if gts < lmt:
            return f'На сегодня осталось {remaining} {currency}'
        elif self.get_today_stats() == lmt:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {debt} {currency}'


class CaloriesCalculator(Calculator):
    """Representing calculator for
       managing calories"""
    def __init__(self, limit: float, records: List['Record'] = []) -> None:
        self.limit = limit
        self.records = []

    def get_calories_remained(self) -> str:
        """Shows how many calories are stil left to eat"""
        limit = self.limit
        remaining = limit - self.get_today_stats()

        # Compere's calories consumed today and comperes to limit that was set.
        # Returns msg string accordingly.
        if self.get_today_stats() < limit:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    + f'но с общей калорийностью не более {remaining} кКал')
        else:
            return 'Хватит есть!'


class Record:
    """Class representing single record
       with fields: amount, comment, date"""
    date = dt.datetime.now().date()

    def __init__(self,
                 amount: float,
                 comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if type(date) is str:
            date_format = '%d.%m.%Y'
            date = (dt.datetime.strptime(date, date_format)).date()
        else:
            date = dt.datetime.now().date()
        self.date = date
