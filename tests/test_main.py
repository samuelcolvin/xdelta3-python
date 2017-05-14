import pytest

import xdelta3

value_one = b'this is a short string to test with. It is suitable for delta encoding.'
value_two = b'this is a different short string to test with. It is suitable for delta encoding.'


def test_encode_decode():
    delta = xdelta3.encode(value_one, value_two)
    value_two2 = xdelta3.decode(value_one, delta)
    assert value_two == value_two2


def test_encode():
    result = xdelta3.encode(value_one, value_two)
    assert result == b'\xd6\xc3\xc4\x00\x00\x01G\x00\x14Q\x00\t\x04\x02different\x1a\n\x13>\x00\t'


def test_no_delta():
    with pytest.raises(xdelta3.NoDeltaFound) as exc_info:
        xdelta3.encode(b'hello', b'goodbye')
    assert exc_info.value.args[0] == 'No delta found shorter than the input value'


def test_readme():
    value_one = b'wonderful string to demonstrate xdelta3, much of these two strings is the same.'
    value_two = b'different string to demonstrate xdelta3, much of these two strings is the same.'
    delta = xdelta3.encode(value_one, value_two)
    print(f'New string length: {len(value_two)}, delta length: {len(delta)}')

    value_two_rebuilt = xdelta3.decode(value_one, delta)
    assert value_two_rebuilt == value_two
