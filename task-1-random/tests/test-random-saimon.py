from hypothesis import given, settings
import hypothesis.strategies as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))


# Test 1: Output is always either an int or None, never anything else\
# Method tested: int_or_none from youtube_dl/utils.py
# Property: no matter what random value goes in,
# the result must strictly be int type or None — nothing else

from youtube_dl.utils import int_or_none

@given(st.one_of(st.integers(), st.text(), st.floats(allow_nan=False), st.none()))
@settings(max_examples=50)
def test_int_or_none_returns_int_or_none(v):
    result = int_or_none(v)
    assert result is None or isinstance(result, int)


# Test 2: Output is always a float or None, never anything else
# Method tested: float_or_none from youtube_dl/utils.py
# Property: no matter what random value goes in,
# the result must strictly be float type or None

from youtube_dl.utils import float_or_none

@given(st.one_of(st.integers(), st.text(), st.floats(allow_nan=False), st.none()))
@settings(max_examples=50)
def test_float_or_none_returns_float_or_none(v):
    result = float_or_none(v)
    assert result is None or isinstance(result, float)


# Test 3: Output is always an integer or None, never anything else
# Method tested: str_to_int from youtube_dl/utils.py
# Property: str_to_int converts a string to an integer
# it also handles comma separated numbers like "1,000,000"
# returns None if conversion is not possible

from youtube_dl.utils import str_to_int

@given(st.one_of(st.text(), st.integers(), st.none()))
@settings(max_examples=50)
def test_str_to_int_returns_int_or_none(v):
    result = str_to_int(v)
    assert result is None or isinstance(result, int)

# Test 4: Output is always a number or None, never anything else
# Method tested: parse_count from youtube_dl/utils.py
# Property: parse_count parses human readable count strings with K, M suffixes
# into actual numbers e.g. "1K" -> 1000, "2.5M" -> 2500000
# returns None if conversion is not possible
# the result must strictly be int, float, or None

from youtube_dl.utils import parse_count

@given(st.text())
@settings(max_examples=50)
def test_parse_count_returns_number_or_none(s):
    result = parse_count(s)
    assert result is None or isinstance(result, (int, float))

