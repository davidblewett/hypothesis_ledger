=================
Hypothesis Ledger
=================


We’re going to be keeping track of financial transactions between different parties — people and organisations.

This package targets Python 3.6, and makes use of type annotations.


* Free software: BSD license


Features
--------

* Given a CSV file, provide access to a ledger of account activity
* Filter total activity by specific account name and/or transaction end date
* For full usage, see docs/usage.rst
* To run tests:

  * python-3.6 setup.py test

* To check annotations:

  * pip install mypy
  * mypy hypothesis_ledger/hypothesis_ledger.py

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

