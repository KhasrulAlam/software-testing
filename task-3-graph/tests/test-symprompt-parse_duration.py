# Method: parse_duration from youtube_dl/utils.py
# Phase 03 - AI Review Task (SymPrompt), contributed by Tawfiq
# LLM: ChatGPT | Method: parse_duration

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import parse_duration


# SP1 - Path P1: s is not a string -> returns None immediately
def test_parse_duration_non_string_returns_none():
    assert parse_duration(123) is None


# SP2 - Path P2: s is a string but empty after strip -> returns None
def test_parse_duration_whitespace_string_returns_none():
    assert parse_duration('   \t\n  ') is None


# SP3 - Path P3: colon HH:MM:SS format matches first regex
def test_parse_duration_colon_format_hms():
    assert parse_duration('1:02:03') == 3723.0


# SP4 - Path P4: first regex fails, compact unit format matches second
def test_parse_duration_compact_unit_format():
    assert parse_duration('1h30m') == 5400.0


# SP5 - Path P5: first two fail, worded format matches third regex
def test_parse_duration_worded_format():
    assert parse_duration('2 mins') == 120.0


# SP6 - Path P6: no regex matches -> returns None
def test_parse_duration_invalid_format_returns_none():
    assert parse_duration('garbage') is None