xdelta3-python
==============

|BuildStatus| |Coverage| |pypi|

Fast delta encoding in python using xdelta3.

Requirements
------------

* **Python 3.6**
* **linux**

Usage
-----

.. code:: python

    import xdelta3
    value_one = b'this is a wonderful string to demonstrate with. Much of the two strings is duplicated.'
    value_two = b'this is a different string to demonstrate with. Much of the two strings is duplicated.'
    delta = xdelta3.encode(value_one, value_two)

    print(f'New string length: {len(value_two)}, delta length: {len(delta)}')
    value_two_rebuilt = xdelta3.decode(value_one, delta)
    if value_two_rebuilt == value_two:
        print('Boo Ya! Delta encoding successful.')

How fast?
---------

*xdelta3-python* is a thing wrapper around `xdelta 3.1.1 <https://github.com/jmacd/xdelta/>`_
which is a highly optimised c library for delta encoding calculation and compression.

It can encode a delta and decode it again for 5 small changes in a 5.4M character string
(the complete works of shakespeare) in around 30ms. Boom. See ``performance.py``.

.. |BuildStatus| image:: https://travis-ci.org/samuelcolvin/xdelta3-python.svg?branch=master
   :target: https://travis-ci.org/samuelcolvin/xdelta3-python
.. |Coverage| image:: https://codecov.io/gh/samuelcolvin/xdelta3-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/samuelcolvin/xdelta3-python
.. |pypi| image:: https://img.shields.io/pypi/v/xdelta3.svg
   :target: https://pypi.python.org/pypi/xdelta3
