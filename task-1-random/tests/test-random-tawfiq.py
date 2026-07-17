# Method tested: parse_duration from youtube_dl/utils.py
# parse_duration converts a duration string into total seconds as a float
# it handles formats like "1:30", "01:02:03", "1h30m", "1h30m10s"
# if the string is not a valid duration it returns None

from unittest import result

from hypothesis import given, settings
import hypothesis.strategies as st
import sys
import os

# Add youtube-dl to path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import parse_duration


# Test 1: Output is always a number or None, never anything else
# Property: no matter what random string goes in,
# the result must strictly be int, float, or None — nothing else
@given(st.text())
@settings(max_examples=50)
def test_parse_duration_returns_number_or_none(s):
    result = parse_duration(s)
    # result must be either None or a numeric type
    assert result is None or isinstance(result, (int, float))


from youtube_dl.utils import month_by_name
# Test 2: Output is always between 1 and 12 or None
# Property: a valid month number must always be
# between 1 (January) and 12 (December) inclusive
@given(st.text())
@settings(max_examples=50)
def test_month_by_name_returns_valid_month_or_none(s):
    result = month_by_name(s)
    # result must be None or a number between 1 and 12
    assert result is None or (isinstance(result, int) and 1 <= result <= 12)





from youtube_dl.utils import limit_length
# Test 3: Output length is always less than or equal to the given limit
# Property: no matter what string and length go in,
# the result must never exceed the specified maximum length
@given(
st.text(alphabet=st.characters(blacklist_categories=('Cs',))),
st.integers(min_value=3, max_value=1000)
)
@settings(max_examples=50)
def test_limit_length_output_within_limit(s, length):
    result = limit_length(s, length)
    # output length must never exceed the specified
    assert len(result) <= length



from youtube_dl.utils import parse_filesize
# Test 4: Output is always a number or None, never anything else
# Property: no matter what random string goes in,
# the result must strictly be a number or None — never negative
@given(st.text())
@settings(max_examples=50)
def test_parse_filesize_returns_positive_number_or_none(s):
    result = parse_filesize(s)
    # result must be None or a non-negative number
    assert result is None or (isinstance(result, (int, float)) and result >= 0)
