import xdelta3


def test_encode():
    v1 = b'this is a short string to test with. It is suitable for delta encoding.'
    v2 = b'this is a different short string to test with. It is suitable for delta encoding.'
    result = xdelta3.encode(v1, v2)
    assert result == b'\xd6\xc3\xc4\x00\x00\x01G\x00\x14Q\x00\t\x04\x02different\x1a\n\x13>\x00\t'
