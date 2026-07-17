# Method: remove_start from youtube_dl/utils.py
# Phase 02 - Input Space Partitioning

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from hypothesis import given
import hypothesis.strategies as st
from youtube_dl.utils import remove_start


# TV1: q1=None, q2=non-empty, starts_with=n/a → must return None
@given(st.just(None), st.text(min_size=1))
def test_tv1_s_is_none(s, start):
    assert remove_start(s, start) is None


# TV2: q1=empty, q2=non-empty, starts_with=n/a → must return empty string unchanged
@given(st.just(""), st.text(min_size=1))
def test_tv2_s_is_empty(s, start):
    assert remove_start(s, start) == ""


# TV3: q1=non-empty, q2=empty, starts_with=n/a → must return s unchanged
@given(st.just("hello world"), st.just(""))
def test_tv3_start_is_empty(s, start):
    assert remove_start(s, start) == "hello world"


# TV4: q1=non-empty, q2=non-empty, starts_with=yes partial → must remove prefix
@given(st.just("hello world"), st.just("hello"))
def test_tv4_starts_with_partial_match(s, start):
    result = remove_start(s, start)
    assert result == " world"


# TV5: q1=non-empty, q2=non-empty, starts_with=yes full match → must return empty string
@given(st.just("hello"), st.just("hello"))
def test_tv5_starts_with_full_match(s, start):
    result = remove_start(s, start)
    assert result == ""


# TV6: q1=non-empty, q2=non-empty, starts_with=no match → must return s unchanged
@given(st.just("world"), st.just("hello"))
def test_tv6_no_match(s, start):
    assert remove_start(s, start) == "world"