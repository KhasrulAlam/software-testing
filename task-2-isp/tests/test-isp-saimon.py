# Method: int_or_none from youtube_dl/utils.py
# Phase 02 - Input Space Partitioning

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from hypothesis import given
import hypothesis.strategies as st
from youtube_dl.utils import int_or_none


# TV1: q1=None, q2=default scale, numeric=n/a, sign=n/a → must return None
@given(st.just(None))
def test_tv1_none_input(v):
    assert int_or_none(v) is None


# TV2: q1=empty string, q2=default scale, numeric=n/a, sign=n/a → must return None
@given(st.just(""))
def test_tv2_empty_string(v):
    assert int_or_none(v) is None


# TV3: q1=string, q2=scale=1, numeric=valid integer, sign=positive → must return 42
@given(st.just("42"))
def test_tv3_valid_positive_integer_string(v):
    assert int_or_none(v) == 42


# TV4: q1=string, q2=scale=1, numeric=valid integer, sign=negative → must return -42
@given(st.just("-42"))
def test_tv4_valid_negative_integer_string(v):
    assert int_or_none(v) == -42


# TV5: q1=string, q2=scale=10, numeric=valid integer, sign=positive → must return 4
@given(st.just("42"))
def test_tv5_valid_integer_with_scale(v):
    assert int_or_none(v, scale=10) == 4


# TV6: q1=string, q2=default scale, numeric=non-numeric, sign=n/a → must return None
@given(st.just("abc"))
def test_tv6_non_numeric_string(v):
    assert int_or_none(v) is None
