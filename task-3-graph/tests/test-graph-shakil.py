# -*- coding: utf-8 -*-
# Method: sanitize_filename from youtube_dl/utils.py
# Phase 03 - Graph Coverage (Node + Edge), contributed by Shakil
#
# Each test targets specific branches inside sanitize_filename that the
# Phase 01 / Phase 02 suite never exercised. Non-ASCII inputs are written as
# \u escapes so the intended code points survive any source-file encoding.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import sanitize_filename


# GC1 - Timestamp handling branch.
# Covers the re.sub(r'[0-9]+(?::[0-9]+)+', ...) edge that rewrites "n:n:n".
def test_gc1_timestamp_colons_become_underscores():
    assert sanitize_filename('1:2:3') == '1_2_3'


# GC2 - Restricted accent-replacement + NFKC normalisation branches.
# '\u00e9' is the composed character 'e-acute', a key in ACCENT_CHARS.
# Covers `if restricted and char in ACCENT_CHARS` and the NFKC normalise edge.
def test_gc2_restricted_accent_is_transliterated():
    assert sanitize_filename('Band\u00e9', restricted=True) == 'Bande'


# GC3 - Restricted quote and restricted colon branches together.
# Covers char == '"' -> '' (restricted) and char == ':' -> '_-' (restricted).
def test_gc3_restricted_quote_and_colon():
    assert sanitize_filename('a":b', restricted=True) == 'a_-b'


# GC4 - Restricted special-character / whitespace branch.
# Covers `if restricted and (char in special set or char.isspace())` -> '_'
def test_gc4_restricted_space_and_special_become_underscore():
    assert sanitize_filename('a b&c', restricted=True) == 'a_b_c'


# GC5 - Restricted high-codepoint branch + empty-result fallback.
# '\u4e2d' is a CJK char (category 'Lo', ord > 127, not in 'CM' -> '_').
# Covers `if restricted and ord(char) > 127` and the final `if not result` edge.
def test_gc5_restricted_high_codepoint_and_empty_fallback():
    assert sanitize_filename('\u4e2d', restricted=True) == '_'


# GC6 - Dash-prefix rewrite vs. is_id short-circuit.
# Covers `if result.startswith('-'): result = '_' + result[1:]` and the
# `if not is_id:` edge being skipped (taken false) when is_id=True.
def test_gc6_dash_prefix_and_is_id_skip():
    assert sanitize_filename('-abc') == '_abc'              # cleanup block runs
    assert sanitize_filename('-abc', is_id=True) == '-abc'  # cleanup skipped