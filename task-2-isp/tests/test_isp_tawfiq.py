# Method: limit_length from youtube_dl/utils.py
# Phase 02 - Input Space Partitioning

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from hypothesis import given
import hypothesis.strategies as st
from youtube_dl.utils import limit_length


# TV1: q1=None, q2=normal limit, string_vs_limit=n/a → must return None
@given(st.just(None), st.just(10))
def test_tv1_none_input(s, length):
    assert limit_length(s, length) is None


# TV2: q1=empty, q2=normal limit, string_vs_limit=shorter → must return empty unchanged
@given(st.just(""), st.just(10))
def test_tv2_empty_string(s, length):
    assert limit_length(s, length) == ""


# TV3: q1=non-empty, q2=very large limit, string_vs_limit=shorter → must return s unchanged
@given(st.just("Hello World"), st.just(10000))
def test_tv3_string_shorter_than_limit(s, length):
    assert limit_length(s, length) == "Hello World"


# TV4: q1=non-empty, q2=normal limit, string_vs_limit=equal → must return s unchanged
@given(st.just("Hello"), st.just(5))
def test_tv4_string_equal_to_limit(s, length):
    assert limit_length(s, length) == "Hello"


# TV5: q1=non-empty, q2=normal limit, string_vs_limit=longer → must truncate with ellipses
@given(st.just("Hello World"), st.just(8))
def test_tv5_string_longer_than_limit(s, length):
    result = limit_length(s, length)
    assert result == "Hello..."
    assert len(result) == 8


# TV6: q1=non-empty, q2=very small limit (3), string_vs_limit=longer → must return "..." only
@given(st.just("Hello World"), st.just(3))
def test_tv6_very_small_limit(s, length):
    result = limit_length(s, length)
    assert result == "..."
