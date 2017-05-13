"""
To run
    curl https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt > shakespeare.txt
    cp shakespeare.txt shakespeare_changed.txt
    vim shakespeare_changed.txt (and make some changes to shakespeare_changed.txt)
    python performance.py

Result: roughly 8ms per change plus 10ms overhead.
"""

from pathlib import Path
from time import time
import xdelta3


v1 = Path('shakespeare.txt').read_bytes()
v2 = Path('shakespeare_changed.txt').read_bytes()

start = time()
delta = xdelta3.encode(v1, v2)
v22 = xdelta3.decode(v1, delta)
time_taken = (time() - start) * 1000
print(f'matching:        {v2 == v22}')
print(f'original length: {len(v1)}')
print(f'changed length:  {len(v2)}')
print(f'delta length:    {len(delta)}')
print(f'dtime taken to encode and decode: {time_taken:0.0f}ms')
