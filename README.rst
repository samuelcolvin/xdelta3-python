xdelta3-python
==============

|BuildStatus| |Coverage| |pypi|

Fast delta encoding in python using xdelta3.

Requirements
------------

* **Python 3.5 or 3.6** - it's 2017, you should be using python 3.6 by now anyway.
* **linux** - compilation only tested on ubuntu, might work on other platform.

Installation
------------

.. code:: shell

    pip install xdelta3

Usage
-----

.. code:: python

    import xdelta3
    value_one = b'wonderful string to demonstrate xdelta3, much of these two strings is the same.'
    value_two = b'different string to demonstrate xdelta3, much of these two strings is the same.'
    delta = xdelta3.encode(value_one, value_two)
    # delta is an unreadable byte string: b'\xd6\xc3 ... \x01different\n\x13F\x00'

    print(f'New string length: {len(value_two)}, delta length: {len(delta)}')
    value_two_rebuilt = xdelta3.decode(value_one, delta)
    if value_two_rebuilt == value_two:
        print('Boo Ya! Delta encoding successful.')

*(with xdelta3 installed this code should run "as is", just copy it into ipython or a file and run)*

How fast?
---------

*xdelta3-python* is a thin wrapper around `xdelta 3.1.1 <https://github.com/jmacd/xdelta/>`_
which is a highly optimised c library for delta calculation and compression.
It can encode a delta and decode it again for 5 small changes in a 5.5 million character string
(the complete works of shakespeare) in around 10ms (or 30ms with the highest compression level). Boom.
See `performance.py <https://github.com/samuelcolvin/xdelta3-python/blob/master/performance.py>`_.

.. |BuildStatus| image:: https://travis-ci.org/samuelcolvin/xdelta3-python.svg?branch=master
   :target: https://travis-ci.org/samuelcolvin/xdelta3-python
.. |Coverage| image:: https://codecov.io/gh/samuelcolvin/xdelta3-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/samuelcolvin/xdelta3-python
.. |pypi| image:: https://img.shields.io/pypi/v/xdelta3.svg
   :target: https://pypi.python.org/pypi/xdelta3
