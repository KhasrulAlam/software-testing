# -*- coding: utf-8 -*-
# Method: sanitize_filename from youtube_dl/utils.py
# Phase 04 - Logic Coverage, contributed by Shakil
#
# Target predicate (inside replace_insane, line 2137):
#
#     if restricted and (char in '!&\'()[]{}$;`^,#' or char.isspace()):
#         return '_'
#
# This is a flat 3-clause predicate. Clauses:
#     a = restricted
#     b = char in the special-character set
#     c = char.isspace()
# So P = a AND (b OR c).
#
# Note: b and c are mutually exclusive (a punctuation char is never whitespace),
# so 2 of the 8 clause combinations are infeasible. We therefore use Clause
# Coverage for Group 1 instead of Combinatorial Coverage. For the AND predicate,
# an inactive clause forces P false, so "inactive clause with true predicate" is
# infeasible; GICC covers the feasible inactive cases only.
#
# Each test embeds the character under test between plain letters 'a' and 'b'
# (or before 'foo') so the per-character result survives the underscore-collapse
# and strip steps and stays observable in the final output.
#
# Criteria selected:
#   Group 1: Clause Coverage (CC)
#   Group 2: Correlated Active Clause Coverage (CACC)
#   Group 3: General Inactive Clause Coverage (GICC)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import sanitize_filename


# LC1 - a=T, b=T, c=F, P=T. '&' is a special char, restricted on, so it -> '_'.
# Criteria: CC (a=T, b=T); CACC (a deciding vs LC2; b deciding vs LC3);
#           GICC (clause c inactive, c false, predicate true).
def test_lc1_restricted_special_char():
    assert sanitize_filename('a&b', restricted=True) == 'a_b'


# LC2 - a=F, b=T, c=F, P=F. restricted off, so the special char '&' is kept.
# Criteria: CC (a=F); CACC (a deciding vs LC1);
#           GICC (clause c inactive, c false, predicate false).
def test_lc2_unrestricted_special_char_kept():
    assert sanitize_filename('a&b', restricted=False) == 'a&b'


# LC3 - a=T, b=F, c=F, P=F. '+' is neither special nor space, so it is kept
# even though restricted is on.
# Criteria: CC (b=F, c=F); CACC (b deciding vs LC1; c deciding vs LC5);
#           GICC (clause a inactive, a true, predicate false).
def test_lc3_restricted_plain_char_kept():
    assert sanitize_filename('a+b', restricted=True) == 'a+b'


# LC4 - a=F, b=F, c=F, P=F. nothing triggers replacement.
# Criteria: CC (a=F, b=F, c=F);
#           GICC (clause a inactive, a false, predicate false).
def test_lc4_unrestricted_plain_char_kept():
    assert sanitize_filename('a+b', restricted=False) == 'a+b'


# LC5 - a=T, b=F, c=T, P=T. a space is whitespace, restricted on, so it -> '_'.
# Criteria: CC (c=T); CACC (c deciding vs LC3);
#           GICC (clause b inactive, b false, predicate true).
def test_lc5_restricted_whitespace():
    assert sanitize_filename('a b', restricted=True) == 'a_b'


# LC6 - a=F, b=F, c=T, P=F. restricted off, so the space is kept.
# Criteria: CC (c=T, a=F); GICC (clause b inactive, b false, predicate false).
def test_lc6_unrestricted_whitespace_kept():
    assert sanitize_filename('a b', restricted=False) == 'a b'


# LC7 - Branch-coverage top-up, not part of the line-2137 predicate.
# Targets the only missing branch in the method, line 2155:
#     if restricted and result.startswith('-_'):
#         result = result[2:]
# Input '-&foo' restricted -> '-' kept, '&' -> '_', giving '-_foo', which then
# has its '-_' prefix stripped to 'foo'. This drives branch (2155->2156) and
# raises branch coverage of the method to 100%.
def test_lc7_restricted_dash_underscore_prefix_stripped():
    assert sanitize_filename('-&foo', restricted=True) == 'foo'