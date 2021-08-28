import datetime as dt  # for data type to be used
# for showing type of the variable
from typing import Dict, List, Optional, Tuple


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

    def get_today_stats(self) -> float:
        """Counts amount of money/calories used
           used up in a day."""

        # Summ all records of amount (callories/Cash) where day = today.
        dt_now = dt.datetime.now()
        amount_records: List[float] = [
            record.amount for record in self.records
            if record.date == dt_now.date()]
        count_day: float = sum(amount_records)

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
            if (week_ago < record.date
               <= dt.datetime.now().date()):
                count_week = count_week + record.amount

        return count_week

    def today_remained(self):
        """Calculates money/calories left below limit"""
        remaining: float = self.limit - self.get_today_stats()
        return(remaining)


class CashCalculator(Calculator):
    """Representing calculator for
       money management."""
    # Unit test accept only this rates???
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00
    currencys: Dict[str, Tuple[str, float]] = {
        'eur': ('Euro', EURO_RATE),
        'usd': ('USD', USD_RATE),
        'rub': ('руб', RUB_RATE)}

    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def converter(self, inpAmount: float, rate: float) -> float:
        """Converst rubles to dollars or euro using information
           from yandex.ru and returns answer to 2dp."""

        converted = inpAmount / rate
        converted = (round(converted, 2))
        return converted

    def get_today_cash_remained(self, currency: str) -> str:
        """Shows how much money is left to spend for today."""
        remaining = self.today_remained()
        debt: float = abs(remaining)

        # Convert currency and rename for better look.
        # Raises error if gets unknown currency.
        try:
            currencys_out = self.currencys[currency]
            cur_out = currencys_out[1]
            remaining = self.converter(remaining, cur_out)
            debt = self.converter(debt, cur_out)
            currency_name = currencys_out[0]
        except KeyError:
            raise ValueError('Такая валюта не доступна.')

        # Compere's money spends today and comperes to limit that was set.
        # Returns msg string accordingly.
        if remaining > 0:
            return f'На сегодня осталось {remaining} {currency_name}'
        elif remaining == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {debt} {currency_name}'


class CaloriesCalculator(Calculator):
    """Representing calculator for
       managing calories"""

    def get_calories_remained(self) -> str:
        """Shows how many calories are stil left to eat"""
        limit = self.limit
        remaining = self.today_remained()

        # Compere's calories consumed today and comperes to limit that was set.
        # Returns msg string accordingly.
        if self.get_today_stats() < limit:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remaining} кКал')
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
