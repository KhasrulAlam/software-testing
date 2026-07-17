# Project – Phase 03 Submission
**Software Testing – Graph Coverage**

---

**Group:** 20  
**Members:** 
- S M Khasrul Alam Shakil
- Saimon Chowdhury Fahim
- Md Tawfiq Bashar

---

> **Instructions:** Do not modify the task descriptions or section headings.
> Fill in your answers only where indicated. Replace placeholder text but leave
> everything else intact. Each answer should be annotated with the contributing
> group member where applicable.

---

## Task 03 – Graph Coverage

Add your test files to the repository under `task-3-graph/` and make **individual commits**.

---

### 1 – Coverage Measurement

Measure the coverage of your **full test suite** (project tests + all tests from Phases 01 and 02) using **two graph coverage criteria** of your choice.

Describe each result in 2–3 sentences. Include a `pytest-cov` screenshot for each.

> We measured our accumulated test suite (Phase 01 random tests + Phase 02 ISP tests, 30 tests total, all passing) against `youtube_dl/utils.py` using two graph coverage criteria: **Node Coverage** (statement coverage) and **Edge Coverage** (branch coverage). The youtube-dl built-in test suite was excluded because it is network-dependent, produces 1,500+ failures offline, and takes hours to run; our project tests are the meaningful unit-level suite here.

**Coverage criterion 1:** `Statement Coverage`
> The suite executes 489 of 2453 statements in `utils.py`, giving 20% node coverage. The percentage is low not because our target functions are poorly tested, but because `utils.py` holds hundreds of unrelated utility functions that inflate the denominator. Coverage at the level of our individually targeted functions is far higher. 

![alt text](<screenshot/shakil/Graph Coverage/statement_coverage.png>)

---

**Coverage criterion 2:** `Branch Coverage`

> With branch tracking enabled the coverage falls to 15%, over 1034 total branches with only 19 partially taken. Edge coverage sits below node coverage because many conditional paths inside the functions we touch (error handling, alternate-format branches, restricted-mode variants) are never triggered by the current inputs, leaving those edges unexercised.

![alt text](<screenshot/shakil/Graph Coverage/branch_coverage.png>)

---

### 2 – Test Suite Extension

Choose **one** of the following two options and document your work below.

> ⚠️ Pick coverage criteria that do not already reach 100% — there must be room for improvement.

---

**Option A – Increase coverage (at least 6 new tests per group member)**

For each new test, state the target method, the coverage criterion it advances, and the effect on the overall coverage value.

Per-test coverage effect was measured by running each test in isolation (no Hypothesis random tests in the run), because the Phase 01 random suite touches the same functions with different inputs each run, causing a few lines of run-to-run noise larger than one deterministic test's signal. Run alone, each test is stable and its footprint is exact. The base column uses the first test of each member as reference.

**Student 1 – S M Khasrul Alam Shakil**

Method: `sanitize_filename` | Aggregate effect: Miss 1964 → 1958, BrPart 19 → 13, branch coverage 15% → 16%

| # | Method | Criterion targeted | Coverage effect |
|---|--------|--------------------|-----------------|
| GC1 | sanitize_filename | Edge: timestamp `re.sub` rewrite (`n:n:n` -> `n_n_n`) | base path: 424 stmts, 0 branches resolved |
| GC2 | sanitize_filename | Node 2128: ACCENT_CHARS replace + NFKC normalise | +2 stmts, +1 branch resolved |
| GC3 | sanitize_filename | Edge: restricted `"`->`''` and `:`->`_-` | +3 stmts, +2 branches resolved |
| GC4 | sanitize_filename | Node 2138: restricted special/whitespace -> `_` | +2 stmts, +1 branch resolved |
| GC5 | sanitize_filename | Node 2140: restricted `ord>127` + empty fallback | +2 stmts, +0 branch resolved |
| GC6 | sanitize_filename | Edge 2150->2162: dash-prefix + `is_id=True` skip | +1 stmt, +1 branch resolved |
| … | … | … | … |


```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import sanitize_filename

# GC1 - Timestamp handling branch.
def test_gc1_timestamp_colons_become_underscores():
    assert sanitize_filename('1:2:3') == '1_2_3'

# GC2 - Restricted accent-replacement + NFKC normalisation branches.
def test_gc2_restricted_accent_is_transliterated():
    assert sanitize_filename('Band\u00e9', restricted=True) == 'Bande'

# GC3 - Restricted quote and restricted colon branches.
def test_gc3_restricted_quote_and_colon():
    assert sanitize_filename('a":b', restricted=True) == 'a_-b'

# GC4 - Restricted special-character / whitespace branch.
def test_gc4_restricted_space_and_special_become_underscore():
    assert sanitize_filename('a b&c', restricted=True) == 'a_b_c'

# GC5 - Restricted high-codepoint branch + empty-result fallback.
def test_gc5_restricted_high_codepoint_and_empty_fallback():
    assert sanitize_filename('\u4e2d', restricted=True) == '_'

# GC6 - Dash-prefix rewrite vs. is_id short-circuit.
def test_gc6_dash_prefix_and_is_id_skip():
    assert sanitize_filename('-abc') == '_abc'              # cleanup block runs
    assert sanitize_filename('-abc', is_id=True) == '-abc'  # cleanup skipped

```

---

**Student 2 – [Saimon Chowdhury Fahim]**

| # | Method | Criterion targeted | Coverage effect |
|---|--------|--------------------|-----------------|
| GC1 | parse_count | Node: `if s is None` guard (early return) | base path: 409 stmts, BrPart 4 |
| GC2 | parse_count | Edge: numeric-match True -> str_to_int -> int_or_none | +13 stmts, +6 branches reached |
| GC3 | parse_count | Node: comma-strip `re.sub` in str_to_int | +13 stmts, +6 branches reached |
| GC4 | parse_count | Edge: numeric False -> lookup_unit_table success ('K') | +9 stmts, +2 branches reached |
| GC5 | parse_count | Node: decimal num group + float multiply ('2.5M') | +9 stmts, +2 branches reached |
| GC6 | parse_count | Edge: `if not m: return None` in lookup_unit_table | +7 stmts, +2 branches reached |
| … | … | … | … |

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import parse_count

# GC1 - None guard branch.
def test_gc1_none_returns_none():
    assert parse_count(None) is None

# GC2 - Pure-numeric branch via str_to_int.
def test_gc2_plain_integer_string():
    assert parse_count('1234') == 1234

# GC3 - Comma-grouped number through str_to_int.
def test_gc3_comma_grouped_number():
    assert parse_count('1,234') == 1234

# GC4 - Suffix path via lookup_unit_table (success).
def test_gc4_thousand_suffix():
    assert parse_count('1K') == 1000

# GC5 - Decimal + suffix through lookup_unit_table.
def test_gc5_decimal_million_suffix():
    assert parse_count('2.5M') == 2500000

# GC6 - Non-matching input -> lookup_unit_table no-match branch.
def test_gc6_non_matching_returns_none():
    assert parse_count('abc') is None
```

---
**Student 3 – [Md Tawfiq Bashar]**

| # | Method | Criterion targeted | Coverage effect |
|---|--------|--------------------|-----------------|
| GC1 | parse_duration | Node: `if not isinstance(...)` non-string guard | base path: 406 stmts, BrPart 4 |
| GC2 | parse_duration | Edge: all 3 regexes fail -> final `return None` | +9 stmts, +4 branches reached |
| GC3 | parse_duration | Edge: first regex (colon HH:MM:SS) match | +7 stmts, +2 branches reached |
| GC4 | parse_duration | Node: first-regex `ms` group + `float(ms)/10**len(ms)` | +7 stmts, +2 branches reached |
| GC5 | parse_duration | Edge: second regex (compact unit "1h30m") | +9 stmts, +3 branches reached |
| GC6 | parse_duration | Edge: third regex (worded "2 mins") | +9 stmts, +3 branches reached |
| … | … | … | … |

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from youtube_dl.utils import parse_duration


# GC1 - Non-string guard branch.
def test_gc1_non_string_returns_none():
    assert parse_duration(123) is None

# GC2 - All formats fail -> final return None branch.
def test_gc2_unparseable_returns_none():
    assert parse_duration('garbage') is None

# GC3 - First regex: colon HH:MM:SS match.
def test_gc3_colon_hms_format():
    assert parse_duration('1:02:03') == 3723.0

# GC4 - First regex with milliseconds sub-group.
def test_gc4_colon_with_milliseconds():
    assert parse_duration('1:30.5') == 90.5

# GC5 - Second regex: compact unit format "1h30m".
def test_gc5_unit_format_hours_minutes():
    assert parse_duration('1h30m') == 5400.0

# GC6 - Third regex: worded minutes "2 mins".
def test_gc6_worded_minutes_format():
    assert parse_duration('2 mins') == 120.0
```
---

**Option B – Reveal a new bug**

> Describe the bug, its context in the code, a failing test that exposes it, and a potential fix.

**Bug description:**
> _Your answer here._

**Failing test:**
```python
# The test that exposes the bug
```

**Proposed fix:**
```python
# The fix (code diff or corrected snippet)
```

---

## AI Review Task – SymPrompt

As a group, apply the **SymPrompt** approach from the paper *Code-Aware Prompting* to guide your LLM in constructing coverage-improving tests. Pick the methods selected by one group member in the individual task above.

**LLM used:**
>  ChatGPT (GPT-4o)

**SymPrompt steps performed:**
> We applied SymPrompt to `parse_duration` from `youtube_dl/utils.py`, the method targeted by Tawfiq above. SymPrompt works in three steps as described in the paper.

> Step I (Path Constraint Collection): We manually traversed the AST of `parse_duration` and identified 6 basis execution paths, each with its branch constraints and expected return value:

 | Path | Constraint | Returns |
 |------|-----------|---------|
 | P1 | s is not a string | None |
 | P2 | s is a string, empty after strip | None |
 | P3 | first regex matches (colon HH:MM:SS form) | float seconds |
 | P4 | first fails, second matches (compact unit "1h30m") | float seconds |
 | P5 | first two fail, third matches (worded "2 mins") | float seconds |
 | P6 | non-empty string, no regex matches | None |
 |...|...|...|

> Step II (Context Construction): Each prompt included the method signature, its return behaviour, and the exact import pattern needed to call it in a pytest context.

> Step III (Test Generation): We sent one prompt per path to ChatGPT in a single iterative conversation. Each message stated the path constraints and expected return value. Earlier generated tests remained visible in the conversation, matching the iterative prompting procedure described in the paper.

**Prompts used:**
> Message 1: Provided the method signature, import pattern, and asked for a test where s is not a string (returns None).

> Message 2: Asked for a test where s is a string but empty after stripping (returns None).

> Message 3: Asked for a test where s matches the colon HH:MM:SS format e.g. "1:02:03" (returns 3723.0).

> Message 4: Asked for a test where the colon format fails but the compact unit format matches e.g. "1h30m" (returns 5400.0).

> Message 5: Asked for a test where the first two formats fail but the worded format matches e.g. "2 mins" (returns 120.0).

> Message 6: Asked for a test where no format matches e.g. "garbage" (returns None).

**Generated tests:**
```python
# LLM: ChatGPT (GPT-4o) | Method: parse_duration

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
```

**Coverage results for the LLM-generated tests:**
> All 6 tests pass (Pass@1 = 1.0), all correctly call `parse_duration` (FM Call@1 = 1.0, Correct@1 = 1.0). Per-test coverage was measured in isolation on the 2453-statement checkout (Python 3.9). SP1 is used as the base since it covers only the entry path before any parsing begins.

 | # | Test | Path covered | Stmts covered | BrPart | +Stmts vs SP1 | +Branches |
 |---|------|-------------|:-------------:|:------:|:-------------:|:---------:|
 | SP1 | non_string_returns_none | P1: type guard | 406 | 7 | base | base |
 | SP2 | whitespace_string_returns_none | P2: empty-after-strip guard | 408 | 8 | +2 | +1 |
 | SP3 | colon_format_hms | P3: first regex match | 413 | 9 | +7 | +2 |
 | SP4 | compact_unit_format | P4: second regex match | 415 | 10 | +9 | +3 |
 | SP5 | worded_format | P5: third regex match | 415 | 10 | +9 | +3 |
 | SP6 | invalid_format_returns_none | P6: all regexes fail | 415 | 11 | +9 | +4 |
 |...|...|...|...|...|...|...|

> The SymPrompt approach produced 6 correct passing tests covering all 6 basis paths of `parse_duration`. Each path-specific prompt successfully guided ChatGPT to the right input and expected return value. SP3 through SP6 add the most coverage by walking through the multi-regex parsing logic. SP6 uniquely resolves one additional partial branch over SP4 and SP5, corresponding to the all-regexes-fail path. This matches the paper's RQ1 finding that path constraint prompts guide the model to cover a wider range of execution paths than a generic prompt would produce.

---

## Contribution Overview

Indicate which group member contributed to which sub-task by placing an **×** in the corresponding cell.

| Sub-task | Member 1 (Shakil) | Member 2 (Saimon) | Member 3 (Tawfiq) |
|----------|:-----------------:|:-----------------:|:-----------------:|
<<<<<<< HEAD
| Coverage measurement (2 criteria) | × | x | x |
| Test suite extension (Option A or B) | × | × | × |
| AI Review Task (SymPrompt) | x | x | × |
=======
| Coverage measurement (2 criteria) | × | × | × |
| Test suite extension (Option A or B) | × | × | × |
| AI Review Task (SymPrompt) | × | × | × |
>>>>>>> 1056ebb6b96715c3450693c42beddd3d9313f13a
