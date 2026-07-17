# Method: parse_duration from youtube_dl/utils.py
# Phase 03 - Graph Coverage (Node + Edge), contributed by Tawfiq
#
# parse_duration tries three regex formats in sequence (colon HH:MM:SS,
# unit "1h30m", and worded "2 mins"), guarded by type and validity checks.
# Each test drives a distinct branch. Inputs are chosen to behave identically
# across youtube-dl versions.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import parse_duration


# GC1 - Non-string guard branch.
# Covers `if not isinstance(s, compat_basestring): return None` (True edge).
def test_gc1_non_string_returns_none():
    assert parse_duration(123) is None


# GC2 - All formats fail -> final return None branch.
# Covers the deepest else where none of the three regexes match.
def test_gc2_unparseable_returns_none():
    assert parse_duration('garbage') is None


# GC3 - First regex: colon HH:MM:SS match.
# Covers `if m:` for the first (colon) regex and the days/hours/mins/secs
# duration computation. 1*3600 + 2*60 + 3 = 3723.
def test_gc3_colon_hms_format():
    assert parse_duration('1:02:03') == 3723.0


# GC4 - First regex with milliseconds sub-group.
# Covers the optional `ms` capture and the `float(ms)/10**len(ms)` term.
# 1*60 + 30 + 0.5 = 90.5.
def test_gc4_colon_with_milliseconds():
    assert parse_duration('1:30.5') == 90.5


# GC5 - Second regex: compact unit format "1h30m".
# Covers the else branch into the unit regex and its `if m:` match path.
# 1*3600 + 30*60 = 5400.
def test_gc5_unit_format_hours_minutes():
    assert parse_duration('1h30m') == 5400.0


# GC6 - Third regex: worded minutes "2 mins".
# Covers the innermost else into the worded hours/mins regex and its match.
# 2*60 = 120.
def test_gc6_worded_minutes_format():
    assert parse_duration('2 mins') == 120.0