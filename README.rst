xdelta3-python
==============

|BuildStatus| |Coverage| |pypi|

Fast delta encoding in python using xdelta3.

How fast?
---------

_xdelta3-python_ is a thing wrapper around
`xdelta 3.1.1 <https://github.com/jmacd/xdelta/tree/a089d04bf19d21a8ac5e03a9066e5a2e36e0b87a>`_
which is a highly optimised c library for delta encoding calculation and compression.

It can encode a delta and decode it again for 5 small changes in a 5.4M character string
(the complete works of shakespeare) in around 30ms. Boom. See ``performance.py``.

.. |BuildStatus| image:: https://travis-ci.org/samuelcolvin/xdelta3-python.svg?branch=master
   :target: https://travis-ci.org/samuelcolvin/xdelta3-python
.. |Coverage| image:: https://codecov.io/gh/samuelcolvin/xdelta3-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/samuelcolvin/xdelta3-python
.. |pypi| image:: https://img.shields.io/pypi/v/xdelta3.svg
   :target: https://pypi.python.org/pypi/xdelta3
