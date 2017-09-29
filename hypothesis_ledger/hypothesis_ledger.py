# -*- coding: utf-8 -*-
"""Main module."""
import csv
import typing
from collections import Counter, OrderedDict
from decimal import Decimal
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Mapping, NamedTuple, NewType, TypeVar


Date = NewType('Date', date)
T = TypeVar('T')
# Unfortunately, typing.Counter is defined as [str, int],
# and there doesn't appear to be a way to add a type overload.
# We really want a custome type that's Counter[str, Decimal]
StrDict = Dict[str, T]


class Transaction(NamedTuple):
    date: Date
    source: str
    destination: str
    value: Decimal
    currency_symbol:str = u'§'

    def __str__(self) -> str:
        return f'<Transaction {self.date}, {self.source}:-{self.currency_symbol}{self.value}, {self.destination}:+{self.currency_symbol}{self.value} >'


class Ledger(object):

    date_format = '%Y-%m-%d'

    def __init__(self,
                 transaction_filename:Path,
                 load_transactions:bool=True) -> None:
        self.transactions: List[Transaction] = []
        if load_transactions:
            self.transactions.extend(
                self.load_transactions(transaction_filename)
            )

    def load_transactions(self, transaction_path:Path) -> List[Transaction]:
        """Given a path to a CSV file, return a list of parsed transactions.
        """
        transactions = []
        with transaction_path.resolve().open() as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=Transaction._fields)
            for row in reader:
                transactions.append(
                    Transaction(
                        date=Date(datetime.strptime(row['date'],
                                                    self.date_format).date()),
                        source=row['source'],
                        destination=row['destination'],
                        value=Decimal(row['value']),
                    )
                )
        # Since elements are tuples, they will naturally sort by index:
        # date, source, destination, value
        return sorted(transactions)

    def balance_for(self,
                    account_name:str,
                    ending_date:date=date.max) -> Decimal:
        """Given an account name and optional ending date, return the final
        balance.
        """
        return self.calculate_balances(ending_date)[account_name]

    def balance_for_by_day(self,
                           account_name:str,
                           ending_date:date=date.max) -> Mapping[date, Decimal]:
        """Given an account name and optional ending date, return the final
        balance.
        """
        # De-duplicate days with a set comprehension
        days = {
            transaction.date
            for transaction in self.transactions
            if transaction.date <= ending_date
        }
        # {
        #   day1: Decimal(balance),
        #   day2: Decimal(balance),
        # }
        return OrderedDict([
            (day, self.calculate_balances(day)[account_name])
            for day in sorted(list(days))
        ])

    def calculate_balances(self,
                           ending_date:date=date.max) -> StrDict:
        """Calculate balances for all accounts in our transactions,
        ending on optional ending_date.
        """
        balances: StrDict = Counter()
        for transaction in self.transactions:
            if transaction.date <= ending_date:
                balances[transaction.source] -= transaction.value
                balances[transaction.destination] += transaction.value
        return balances

    def calculate_balances_by_day(
            self,
            ending_date:date=date.max) -> Mapping[date, StrDict]:
        """Given an optional ending date, return balances for each day.
        """
        # De-duplicate days with a set comprehension
        days = {
            transaction.date
            for transaction in self.transactions
            if transaction.date <= ending_date
        }
        # {
        #   day1: Counter({foo: balance, bar: balance}),
        #   day2: Counter({foo: balance, bar: balance, baz: balance}),
        # }
        return OrderedDict([
            (day, self.calculate_balances(day))
            for day in sorted(list(days))
        ])
