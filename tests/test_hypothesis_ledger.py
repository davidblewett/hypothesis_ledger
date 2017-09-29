#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hypothesis_ledger` package."""


import unittest
from collections import Counter, OrderedDict
from datetime import date
from decimal import Decimal
from pathlib import Path

from hypothesis_ledger.hypothesis_ledger import Ledger, Transaction


class TestLedger(unittest.TestCase):
    """Tests for `hypothesis_ledger` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.transaction_path = Path(__file__).with_name('transactions.csv')
        self.ledger = Ledger(self.transaction_path, load_transactions=True)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_load_transaction_length(self):
        self.assertEqual(len(self.ledger.transactions), 3)

    def test_load_transaction_formatting(self):
        self.assertEqual(
            str(self.ledger.transactions[0]),
            '<Transaction 2015-01-16, john:-§125.00, mary:+§125.00 >',
        )

    def test_load_transaction_parse_types(self):
        for transaction in self.ledger.transactions:
            self.assertIsInstance(transaction, Transaction)
            self.assertIsInstance(transaction.date, date)
            self.assertIsInstance(transaction.source, str)
            self.assertIsInstance(transaction.destination, str)
            self.assertIsInstance(transaction.value, Decimal)
            self.assertIsInstance(transaction.currency_symbol, str)

    def test_load_transaction_parse_values(self):
        transactions = [
            Transaction(date=date(2015, 1, 16),
                        source='john',
                        destination='mary',
                        value=Decimal('125.00')),
            Transaction(date=date(2015, 1, 17),
                        source='john',
                        destination='supermarket',
                        value=Decimal('20.00')),
            Transaction(date=date(2015, 1, 17),
                        source='mary',
                        destination='insurance',
                        value=Decimal('100.00')),
        ]
        self.assertEqual(self.ledger.transactions, transactions)

    def test_calculate_no_bounds(self):
        balances = Counter({'insurance': Decimal('100.00'),
                            'mary': Decimal('25.00'),
                            'supermarket': Decimal('20.00'),
                            'john': Decimal('-145.00')})
        self.assertEqual(self.ledger.calculate_balances(), balances)

    def test_calculate_with_bounds(self):
        self.assertEqual(self.ledger.calculate_balances(date(2015, 1, 16)),
                         Counter({'john': Decimal('-125.00'),
                                  'mary': Decimal('125.00')}))

    def test_calculate_early_bounds(self):
        self.assertEqual(self.ledger.calculate_balances(date.min),
                         Counter())

    def test_balance_for_no_bounds(self):
        self.assertEqual(self.ledger.balance_for('john'), Decimal('-145.00'))

    def test_balance_for_with_bounds(self):
        self.assertEqual(self.ledger.balance_for('john', date(2015, 1, 16)),
                         Decimal('-125.00'))

    def test_balance_for_missing_account(self):
        self.assertEqual(self.ledger.balance_for('bob'), 0)

    def test_balance_for_invalid_type(self):
        with self.assertRaises(TypeError):
            self.ledger.balance_for('john', '2015-01-16')

    def test_balance_for_by_day_no_bounds(self):
        self.assertEqual(
            self.ledger.balance_for_by_day('john'),
            OrderedDict([
                (date(2015, 1, 16), Decimal('-125.00')),
                (date(2015, 1, 17), Decimal('-145.00'))
            ])
        )

    def test_balance_for_by_day_with_bounds(self):
        self.assertEqual(
            self.ledger.balance_for_by_day('john', date(2015, 1, 16)),
            OrderedDict([
                (date(2015, 1, 16), Decimal('-125.00')),
            ])
        )

    def test_balance_for_by_day_missing_account(self):
        self.assertEqual(
            self.ledger.balance_for_by_day('bob'),
            OrderedDict([
                (date(2015, 1, 16), 0),
                (date(2015, 1, 17), 0),
            ])
        )

    def test_balance_by_day_no_bounds(self):
        day_balances = OrderedDict([
            (date(2015, 1, 16),
             Counter({'mary': Decimal('125.00'),
                      'john': Decimal('-125.00')})),
            (date(2015, 1, 17),
             Counter({'insurance': Decimal('100.00'),
                      'mary': Decimal('25.00'),
                      'supermarket': Decimal('20.00'),
                      'john': Decimal('-145.00')}))
        ])
        self.assertEqual(self.ledger.calculate_balances_by_day(), day_balances)

    def test_balance_by_day_with_bounds(self):
        day_balances = OrderedDict([
            (date(2015, 1, 16),
             Counter({'mary': Decimal('125.00'),
                      'john': Decimal('-125.00')})),
        ])
        self.assertEqual(
            self.ledger.calculate_balances_by_day(date(2015, 1, 16)),
            day_balances,
        )
