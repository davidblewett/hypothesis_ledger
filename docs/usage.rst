=====
Usage
=====

To use Hypothesis Ledger in a project, first construct a CSV file::

    2015-01-16,john,mary,125.00
    2015-01-17,john,supermarket,20.00
    2015-01-17,mary,insurance,100.00


To use Hypothesis Ledger in a project::

    from datetime import date
    from pathlib import Path
    from hypothesis_ledger.hypothesis_ledger import Ledger
    my_ledger = Ledger(Path('/path/to/your.csv'))


To calculate current balances of all accounts::

    my_ledger.calculate_balances()
    Out[1]: Counter({'insurance': Decimal('100.00'),
                     'john': Decimal('-145.00'),
                     'mary': Decimal('25.00'),
                     'supermarket': Decimal('20.00')})

To calculate balances of all accounts up to a specific day::

    my_ledger.calculate_balances(date(2015, 1, 16))
    Out[1]: Counter({'john': Decimal('-125.00'), 'mary': Decimal('125.00')})

To generate a running sum by day::

    my_ledger.calculate_balances_by_day()
    Out[1]: OrderedDict([
        (datetime.date(2015, 1, 16),
         Counter({'john': Decimal('-125.00'),
                  'mary': Decimal('125.00')})),
        (datetime.date(2015, 1, 17),
         Counter({'insurance': Decimal('100.00'),
                  'john': Decimal('-145.00'),
                  'mary': Decimal('25.00'),
                  'supermarket': Decimal('20.00')}))
    ])


To generate a running sum by day, up to a specific day::

    my_ledger.calculate_balances_by_day(date(2015, 1, 16))
    Out[1]: OrderedDict([
        (datetime.date(2015, 1, 16),
         Counter({'john': Decimal('-125.00'),
                  'mary': Decimal('125.00')})),
    ])


To retrieve the current balance for a specific account::

    my_ledger.balance_for('john')
    Out[1]: Decimal('-145.00')

To retrieve the current balance for a specific account on a specific day::

    my_ledger.balance_for('john', date(2015, 1, 16))
    Out[1]: Decimal('-125.00')

To retrieve the running sum for a specific account::

    my_ledger.balance_for_by_day('john')
    Out[1]: OrderedDict([(datetime.date(2015, 1, 16), Decimal('-125.00')),
                         (datetime.date(2015, 1, 17), Decimal('-145.00'))])

To retrieve the running sum for a specific account, up to a specific day::

    my_ledger.balance_for_by_day('john', date(2015, 1, 16))
    Out[1]: OrderedDict([(datetime.date(2015, 1, 16), Decimal('-125.00'))])
