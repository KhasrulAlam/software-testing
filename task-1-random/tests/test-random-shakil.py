from hypothesis import given, settings
import hypothesis.strategies as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))


# Test 1: Output never ends with the removed suffix
# Property: if the suffix was removed, the result must not end with it anymore
# Method tested: remove_end from youtube_dl/utils.py
# remove_end removes a specific suffix from a string if it ends with it
# if the string does not end with the suffix it returns the string unchanged

from youtube_dl.utils import remove_end

@given(st.text(), st.text())
@settings(max_examples=50)
def test_remove_end_suffix_removed(s, end):
    result = remove_end(s, end)
    # if input ended with suffix, output must not end with it
    if s.endswith(end) and end:
        assert not result.endswith(end)

# Test 2: Output never starts with the removed prefix
# Property: if the prefix was removed, the result must not start with it anymore
# Method tested: remove_start from youtube_dl/utils.py
# remove_start removes a specific prefix from a string if it starts with it
# if the string does not start with the prefix it returns the string unchanged

from youtube_dl.utils import remove_start

@given(st.text(), st.text())
@settings(max_examples=50)
def test_remove_start_prefix_removed(s, start):
    result = remove_start(s, start)
    # if input started with prefix, output must not start with it
    if s.startswith(start) and start:
        assert not result.startswith(start)

# Test 3: Output never contains illegal filename characters
# Property: no matter what random string goes in,
# characters like / \ : * ? " < > | must never appear in the output
# Method tested: sanitize_filename from youtube_dl/utils.py
# sanitize_filename cleans a string so it can be safely used as a filename
# by removing or replacing illegal characters like / \ : * ? " < > |

from youtube_dl.utils import sanitize_filename

@given(st.text())
@settings(max_examples=50)
def test_sanitize_filename_no_illegal_chars(s):
    result = sanitize_filename(s)
    illegal_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in illegal_chars:
        assert char not in result


# Test 4: Output is always a string or None, never anything else
# Property: no matter what value goes in,
# the result must strictly be a string or None
# Method tested: strip_or_none from youtube_dl/utils.py
# strip_or_none removes leading and trailing whitespace from a string
# if the value is not a string or is None it returns None instead of crashing

from youtube_dl.utils import strip_or_none

@given(st.one_of(st.text(), st.integers(), st.none(), st.floats(allow_nan=False)))
@settings(max_examples=50)
def test_strip_or_none_returns_string_or_none(v):
    result = strip_or_none(v)
    # result must be either None or a string
    assert result is None or isinstance(result, str)