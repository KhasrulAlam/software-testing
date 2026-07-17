# Method: parse_count from youtube_dl/utils.py
# Phase 03 - Graph Coverage (Node + Edge), contributed by Saimon
#
# parse_count routes through two helpers: str_to_int (pure-numeric path) and
# lookup_unit_table (K/M/kk suffix path). Each test below drives a distinct
# branch across those three functions. All inputs are ASCII.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import parse_count


# GC1 - None guard branch.
# Covers `if s is None: return None` (the True edge at the top of parse_count).
def test_gc1_none_returns_none():
    assert parse_count(None) is None


# GC2 - Pure-numeric branch via str_to_int.
# Covers `if re.match(r'^[\d,.]+$', s): return str_to_int(s)` (True edge),
# plus str_to_int's compat_str branch and int_or_none conversion.
def test_gc2_plain_integer_string():
    assert parse_count('1234') == 1234


# GC3 - Comma-grouped number through str_to_int.
# Covers the `re.sub(r'[,\.\+]', '', int_str)` separator-stripping path in
# str_to_int, exercised via the numeric branch of parse_count.
def test_gc3_comma_grouped_number():
    assert parse_count('1,234') == 1234


# GC4 - Suffix path via lookup_unit_table (success).
# Covers the numeric-match False edge (falls through to lookup_unit_table) and
# the successful match path that computes int(float(num) * mult) for unit 'K'.
def test_gc4_thousand_suffix():
    assert parse_count('1K') == 1000


# GC5 - Decimal + suffix through lookup_unit_table.
# Covers the optional decimal group in the num regex and the float
# multiplication, e.g. 2.5 * 1000**2.
def test_gc5_decimal_million_suffix():
    assert parse_count('2.5M') == 2500000


# GC6 - Non-matching input -> lookup_unit_table no-match branch.
# Covers `if not m: return None` inside lookup_unit_table (reached because the
# numeric regex fails and there is no valid unit).
def test_gc6_non_matching_returns_none():
    assert parse_count('abc') is None