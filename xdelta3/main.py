import sys
from enum import IntEnum

import _xdelta3
from _xdelta3 import NoDeltaFound, XDeltaError  # noqa

from .version import VERSION

__all__ = [
    'NoDeltaFound',
    'XDeltaError',
    'Flags',
    'encode',
    'decode',
    'print_version',
]


class Flags(IntEnum):
    """
    Config flags taken from xdelta3/xdelta3/xdelta3.h

    XD3_ prefix removed for conciseness
    """
    # used by VCDIFF tools, see xdelta3-main.h.
    JUST_HDR = 1 << 1
    # used by VCDIFF tools, see xdelta3-main.h.
    SKIP_WINDOW = 1 << 2
    # used by VCDIFF tools, see xdelta3-main.h.
    SKIP_EMIT = 1 << 3
    # flush the stream buffer to prepare for xd3_stream_close().
    FLUSH = 1 << 4

    # use DJW static huffman
    SEC_DJW = 1 << 5
    # use FGK adaptive huffman
    SEC_FGK = 1 << 6
    # use LZMA secondary
    SEC_LZMA = 1 << 24

    SEC_TYPE = SEC_DJW | SEC_FGK | SEC_LZMA

    # disable secondary compression of the data section.
    SEC_NODATA = 1 << 7
    # disable secondary compression of the inst section.
    SEC_NOINST = 1 << 8
    # disable secondary compression of the addr section.
    SEC_NOADDR = 1 << 9

    SEC_NOALL = SEC_NODATA | SEC_NOINST | SEC_NOADDR

    # enable checksum computation in the encoder.
    ADLER32 = 1 << 10
    # disable checksum verification in the decoder.
    ADLER32_NOVER = 1 << 11

    # disable ordinary data * compression feature, only search * the source, not the target.
    NOCOMPRESS = 1 << 13
    # disable the "1.5-pass * algorithm", instead use greedy * matching. Greedy is off by * default.
    BEGREEDY = 1 << 14
    # used by "recode".
    ADLER32_RECODE = 1 << 15

    # 4 bits to set the compression level the same as the command-line setting -1 through -9
    # (-0 corresponds to the NOCOMPRESS flag, and is independent of compression level). This is for
    # convenience, especially with xd3_encode_memory().

    COMPLEVEL_SHIFT = 20
    COMPLEVEL_MASK = 0xF << COMPLEVEL_SHIFT
    COMPLEVEL_1 = 1 << COMPLEVEL_SHIFT
    COMPLEVEL_2 = 2 << COMPLEVEL_SHIFT
    COMPLEVEL_3 = 3 << COMPLEVEL_SHIFT
    COMPLEVEL_6 = 6 << COMPLEVEL_SHIFT
    COMPLEVEL_9 = 9 << COMPLEVEL_SHIFT


def encode(original: bytes, new_value: bytes, flags: int=Flags.COMPLEVEL_9) -> bytes:
    """
    Encode a delta of new_value from original.

    Note the main two arguments original (aka. source) and new_value (aka input) are reversed
    here compared to xdelta3 methods as IMHO this makes more sense.

    :param original: source byte string
    :param new_value: new byte string differing partially from original
    :param flags: see Flags above
    :return: delta byte string
    """
    return _xdelta3.execute(new_value, original, flags, 0)


def decode(original: bytes, delta: bytes, flags: int=Flags.COMPLEVEL_9) -> bytes:
    """
    Decode a delta to calculate a new value from the original and a delta.

    Note the main two arguments original (aka. source) and delta (aka input) are reversed
    here compared to xdelta3 methods as IMHO this makes more sense.

    :param original: source byte string
    :param delta: delta defining changes the original string
    :param flags: see Flags above
    :return: new byte string from applying delta to original
    """
    return _xdelta3.execute(delta, original, flags, 1)


def print_version():
    """
    Print version info for xdelta3-python and the xdelta3 c library.
    """
    print('xdelta3-python:', VERSION, file=sys.stderr)
    print('xdelta3-c library:', file=sys.stderr)
    _xdelta3.version()
