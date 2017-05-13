"""
To run
    curl https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt > shakespeare.txt
    cp shakespeare.txt shakespeare_changed.txt
    vim shakespeare_changed.txt (and make some changes to shakespeare_changed.txt)
    python performance.py

"""

from pathlib import Path
from time import time
from statistics import mean, stdev
import xdelta3


v1 = Path('shakespeare.txt').read_bytes()
v2 = Path('shakespeare_changed.txt').read_bytes()

times = []
for i in range(10):
    start = time()
    delta = xdelta3.encode(v1, v2)
    v22 = xdelta3.decode(v1, delta)
    time_taken = (time() - start) * 1000
    times.append(time_taken)
    print(f'{i + 1:3} result_match={v2 == v22} time={time_taken:0.1f}ms')

print(f'\noriginal length: {len(v1)}')
print(f'changed length:  {len(v2)}')
print(f'delta length:    {len(delta)}')
print(f'mean time taken to encode and decode: {mean(times):0.3f}ms, stdev {stdev(times):0.3f}ms')
