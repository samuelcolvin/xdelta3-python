import base64
import os
import string
from pathlib import Path

import pytest

import xdelta3

value_one = b'this is a short string to test with. It is suitable for delta encoding.'
value_two = b'this is a different short string to test with. It is suitable for delta encoding.'
expected_delta = b'\xd6\xc3\xc4\x00\x00\x01G\x00\x14Q\x00\t\x04\x02different\x1a\n\x13>\x00\t'


def test_encode_decode():
    delta = xdelta3.encode(value_one, value_two)
    assert delta == expected_delta
    value_two2 = xdelta3.decode(value_one, delta)
    assert value_two == value_two2


def test_long_random():
    v1 = base64.b32encode(os.urandom(1000))
    v2 = b'x' + v1 + b'x'
    delta = xdelta3.encode(v1, v2)
    v22 = xdelta3.decode(v1, delta)
    assert v2 == v22


def test_decode_error():
    with pytest.raises(xdelta3.XDeltaError) as exc_info:
        xdelta3.decode(expected_delta, value_one)
    assert exc_info.value.args[0] == 'Error occur executing xdelta3: XD3_INVALID_INPUT'


def test_no_delta():
    with pytest.raises(xdelta3.NoDeltaFound) as exc_info:
        xdelta3.encode(b'hello', b'goodbye')
    assert exc_info.value.args[0] == 'No delta found shorter than the input value'


def test_different_compression():
    all_ascii = (string.ascii_letters + string.digits).encode()
    v1 = all_ascii * 1000
    v2 = all_ascii * 900 + string.ascii_letters.encode() * 100 + all_ascii * 100
    delta_a = xdelta3.encode(v1, v2, xdelta3.Flags.COMPLEVEL_9)
    v2_a = xdelta3.decode(v1, delta_a)
    assert v2 == v2_a

    delta_b = xdelta3.encode(v1, v2, xdelta3.Flags.COMPLEVEL_1)
    v2_b = xdelta3.decode(v1, delta_b)
    assert v2 == v2_b
    assert len(delta_a) < len(delta_b)


def test_version():
    # can't easily test output as capsys doesn't capture output of print_version
    xdelta3.print_version()


def test_readme():
    value_one = b'wonderful string to demonstrate xdelta3, much of these two strings is the same.'
    value_two = b'different string to demonstrate xdelta3, much of these two strings is the same.'
    delta = xdelta3.encode(value_one, value_two)

    value_two_rebuilt = xdelta3.decode(value_one, delta)
    assert value_two_rebuilt == value_two


def test_large_decode():
    this_dir = Path(__file__).parent
    try:
        b1 = (this_dir / 'b1.bin').read_bytes()
        b2 = (this_dir / 'b2.bin').read_bytes()
    except FileNotFoundError as e:
        raise RuntimeError('file required for test not found, run `make download-test-files`') from e

    d = xdelta3.encode(b1, b2)
    b3 = xdelta3.decode(b1, d)
    assert b2 == b3
