# Method: parse_duration from youtube_dl/utils.py
# Phase 04 - Logic Coverage, contributed by Tawfiq
#
# parse_duration contains only single-clause predicates arranged in a 3-level
# nested if/else chain. Flat Active/Inactive Clause Coverage would collapse into
# plain predicate coverage if applied line by line. Instead the criteria are
# applied to the induced compound predicate that controls whether the worded
# regex branch at line 3976 is reached and matches:
#
#     m1 = first regex (colon format)    line 3945
#     m2 = second regex (unit format)    line 3972
#     m3 = third regex (worded format)   line 3976
#
#     compound to reach line 3977:  (not m1) AND (not m2) AND m3
#
# This is how logic coverage differs for a nested structure compared to a flat
# predicate: the clauses are distributed across three nesting levels and are
# only observable under short-circuit semantics. When m1 is True, m2 and m3 are
# never evaluated at all; when m2 is True, m3 is never evaluated. An inner
# clause therefore cannot be made "inactive" in the textbook sense when an outer
# clause short-circuits the predicate, so Inactive Clause Coverage is
# demonstrated only where the clause is genuinely observable.
#
# Criteria selected:
#   Group 1: Clause Coverage (CC)
#   Group 2: Correlated Active Clause Coverage (CACC)
#   Group 3: General Inactive Clause Coverage (GICC)
#
# All expected return values were verified by executing the real source before
# writing assertions.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import parse_duration


# LC1 - non-string input, guard branch.
# Covers `if not isinstance(s, compat_basestring): return None` True direction.
# Baseline already covers this but it is needed for CC (m1 clause is never
# reached, which is a distinct observable state from m1 being reached and False).
# CC (all regex decisions unreached); GICC (m2 and m3 inactive, not reachable).
def test_lc1_non_string_returns_none():
    assert parse_duration(123) is None


# LC2 - garbage string, all three regexes fail.
# m1=False, m2=False, m3=False -> returns None.
# CC (m1=F, m2=F, m3=F);
# CACC (m3 deciding: m1 and m2 both False, m3 False -> None);
# GICC (m3 inactive with m3 False, predicate False).
def test_lc2_no_match_returns_none():
    assert parse_duration('garbage') is None


# LC3 - colon HH:MM:SS format, first regex matches.
# m1=True -> branch taken immediately, m2 and m3 never evaluated.
# 1*3600 + 2*60 + 3 = 3723.0
# CC (m1=T);
# CACC (m1 deciding: flip m1 True->False drives to a different path);
# GICC (m2 and m3 inactive because m1 short-circuits; shown with m1=T predicate
# is short-circuited, inner clauses cannot vary).
def test_lc3_colon_hms_format():
    assert parse_duration('1:02:03') == 3723.0


# LC4 - colon format with milliseconds sub-group.
# m1=True, milliseconds group captured.
# 1*60 + 30 + 0.5 = 90.5
# CC (m1=T with ms sub-group, distinct from LC3);
# confirms the ms computation path inside the first regex branch.
def test_lc4_colon_with_milliseconds():
    assert parse_duration('1:30.5') == 90.5


# LC5 - unit format "1h30m", first regex fails, second matches.
# m1=False, m2=True -> branch taken, m3 never evaluated.
# 1*3600 + 30*60 = 5400.0
# CC (m2=T);
# CACC (m2 deciding: m1 False, m2 True -> result; vs LC2 where m2 False).
def test_lc5_unit_format_hours_minutes():
    assert parse_duration('1h30m') == 5400.0


# LC6 - unit format seconds only, second regex matches.
# m1=False, m2=True (seconds sub-group).
# 30.0
# CC (m2=T with secs only, distinct from LC5);
# GICC (m3 inactive because m2 short-circuits).
def test_lc6_unit_format_seconds():
    assert parse_duration('30s') == 30.0


# LC7 - decimal hours "1.5 hours", both first and second regexes fail, third matches.
# The second regex only accepts integer digits ([0-9]+), so "1.5 hours" fails it.
# The third regex accepts decimals ([0-9.]+), so it matches here.
# m1=False, m2=False, m3=True -> line 3977 executed.
# 1.5 * 3600 = 5400.0
# This is the ONLY test that covers the missing branch (3976->3977).
# CC (m3=T); CACC (m3 deciding vs LC2: same m1/m2 state, flip m3 True->False);
# GICC (m3 inactive is LC2 above with m3=False, predicate False).
def test_lc7_decimal_hours_worded_format():
    assert parse_duration('1.5 hours') == 5400.0


# LC8 - decimal minutes "2.5 mins", both first and second regexes fail, third matches.
# m1=False, m2=False, m3=True -> line 3977 executed.
# 2.5 * 60 = 150.0
# Additional confirmation of the worded branch with the mins group captured.
# CC (m3=T, mins group vs hours group in LC7).
def test_lc8_decimal_minutes_worded_format():
    assert parse_duration('2.5 mins') == 150.0