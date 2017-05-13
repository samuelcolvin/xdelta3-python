# xdelta3-python

Fast delta encoding in python using xdelta3.

## How fast?

_xdelta3-python_ is a thing wrapper around 
[xdelta 3.1.1](https://github.com/jmacd/xdelta/tree/a089d04bf19d21a8ac5e03a9066e5a2e36e0b87a)
which is a highly optimised c library for delta encoding calculation and compression.
 
It can encode a delta and decode it again for 5 small changes in a 5.4M character string
(the complete works of shakespeare) in 50ms. Boom. See `performance.py`.  
