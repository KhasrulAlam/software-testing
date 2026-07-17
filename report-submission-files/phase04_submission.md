# Project – Phase 04 Submission
**Software Testing – Logic Coverage**

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

## Task 04 – Logic Coverage

Each group member selects **one method** containing at least **2 predicates**, with at least one predicate having **3 or more clauses**. If no such predicate exists, a nested `if-else` or `while` structure with at least **2 levels of nesting** may be used instead.

Add your test files to the repository under `task-4-logic/` and make **individual commits**.

---

### Individual Work (per group member)

**Student 1 – [S M Khasrul Alam Shakil]**

**Selected method:** `Santize_filename`

**a) Method selection and predicate/clause structure:**

> Identify all predicates and their clauses. If you chose a nested structure instead, explain how logic coverage criteria apply differently compared to flat predicates.

> `sanitize_filename` cleans a string so it can be used as a filename. The core logic lives in the inner helper `replace_insane`, which is applied to every character. The method contains several predicates, and one of them is a flat 3-clause predicate, so the requirement is met the clean way without needing the nested-structure option.

Predicates inside `replace_insane`:

| Line | Predicate | Clauses |
|------|-----------|---------|
| 2127 | `restricted and char in ACCENT_CHARS` | 2 |
| 2129 | `char == '?' or ord(char) < 32 or ord(char) == 127` | 3 |
| 2137 | `restricted and (char in '!&\'()[]{}$;`^,#' or char.isspace())` | 3 |
| 2139 | `restricted and ord(char) > 127` | 2 |
|...|...|...|

The selected predicate for logic coverage is the one at **line 2137**:

```python
if restricted and (char in '!&\'()[]{}$;`^,#' or char.isspace()):
    return '_'
```

We label its three clauses:

- `a` = `restricted`
- `b` = `char in '!&\'()[]{}$;`^,#'` (character is a special character)
- `c` = `char.isspace()` (character is whitespace)

So the predicate is `P = a AND (b OR c)`.

One structural note that shapes the criteria choice: clauses `b` and `c` are mutually exclusive, because a punctuation character is never whitespace. This makes 2 of the 8 clause combinations infeasible, which is why Combinatorial Coverage is not the right Group 1 pick here. A second note: for an AND predicate, a clause is only inactive when the other side forces the predicate to False, so an inactive clause paired with a True predicate is infeasible. Inactive Clause Coverage therefore covers the feasible inactive cases only.


---

**b) Baseline branch and line coverage (before new tests):**

> Measured on the existing suite (Task 1 random + Task 2 ISP + Task 3 graph),
branch coverage enabled, restricted to the `sanitize_filename` line range.

| Metric | Value | Detail |
|--------|-------|--------|
| Line coverage | 97.0% | 32 of 33 statements |
| Branch coverage | 96.4% | 27 of 28 branches |
| Missing line | 2156 | inside the `-_` prefix cleanup |
| Missing branch | (2155 to 2156) | True direction of `restricted and result.startswith('-_')` |

The method starts almost fully covered, with one uncovered branch at line 2155. The selected predicate at line 2137 was already covered by earlier tests, so the logic tests below confirm that predicate, and one extra test closes the remaining branch at line 2155.


![alt text](<screenshot/shakil/Logic Test/screenshot_baseline_shakil.png>)
---

**c) Logic coverage test cases (3 criteria):**

Choose **one** criterion from each of the three groups below and create tests satisfying each:

- **Group 1:** Predicate Coverage (PC), Clause Coverage (CC), Combinatorial Coverage (CoC)
- **Group 2:** Active Clause Coverage (ACC / GACC / RACC / CACC)
- **Group 3:** Inactive Clause Coverage (ICC / GICC / RICC)

*Criteria selected:*
1. Group 1: Clause Coverage (CC)
2. Group 2: Correlated Active Clause Coverage (CACC)
3. Group 3: General Inactive Clause Coverage (GICC)

Each character under test is placed between plain letters so its per-character
result survives the underscore-collapse and strip steps and stays visible in the
final output. All expected return values were verified against the method source
before writing the assertions.

```python
# Logic coverage test cases (Shakil) - sanitize_filename
# Predicate at line 2137:  P = a AND (b OR c)
#   a = restricted, b = char in special set, c = char.isspace()

from youtube_dl.utils import sanitize_filename


# LC1 - a=T, b=T, c=F, P=T. '&' is special, restricted on, so it -> '_'.
# CC (a=T, b=T); CACC (a deciding vs LC2; b deciding vs LC3);
# GICC (clause c inactive, c false, predicate true).
def test_lc1_restricted_special_char():
    assert sanitize_filename('a&b', restricted=True) == 'a_b'


# LC2 - a=F, b=T, c=F, P=F. restricted off, so '&' is kept.
# CC (a=F); CACC (a deciding vs LC1);
# GICC (clause c inactive, c false, predicate false).
def test_lc2_unrestricted_special_char_kept():
    assert sanitize_filename('a&b', restricted=False) == 'a&b'


# LC3 - a=T, b=F, c=F, P=F. '+' is neither special nor space, so it is kept.
# CC (b=F, c=F); CACC (b deciding vs LC1; c deciding vs LC5);
# GICC (clause a inactive, a true, predicate false).
def test_lc3_restricted_plain_char_kept():
    assert sanitize_filename('a+b', restricted=True) == 'a+b'


# LC4 - a=F, b=F, c=F, P=F. nothing triggers replacement.
# CC (a=F, b=F, c=F);
# GICC (clause a inactive, a false, predicate false).
def test_lc4_unrestricted_plain_char_kept():
    assert sanitize_filename('a+b', restricted=False) == 'a+b'


# LC5 - a=T, b=F, c=T, P=T. a space is whitespace, restricted on, so it -> '_'.
# CC (c=T); CACC (c deciding vs LC3);
# GICC (clause b inactive, b false, predicate true).
def test_lc5_restricted_whitespace():
    assert sanitize_filename('a b', restricted=True) == 'a_b'


# LC6 - a=F, b=F, c=T, P=F. restricted off, so the space is kept.
# CC (c=T, a=F); GICC (clause b inactive, b false, predicate false).
def test_lc6_unrestricted_whitespace_kept():
    assert sanitize_filename('a b', restricted=False) == 'a b'


# LC7 - Branch-coverage top-up for the only missing branch, line 2155:
#     if restricted and result.startswith('-_'): result = result[2:]
# '-&foo' restricted -> '-' kept, '&' -> '_', giving '-_foo', whose '-_'
# prefix is then stripped to 'foo'. Drives branch (2155->2156).
def test_lc7_restricted_dash_underscore_prefix_stripped():
    assert sanitize_filename('-&foo', restricted=True) == 'foo'
```

---

**d) Coverage criterion contribution per test:**

| Test name | Clause values (a, b, c), P | Criteria satisfied |
|-----------|----------------------------|--------------------|
| `test_lc1_restricted_special_char` | T, T, F -> T | CC, CACC, GICC |
| `test_lc2_unrestricted_special_char_kept` | F, T, F -> F | CC, CACC, GICC |
| `test_lc3_restricted_plain_char_kept` | T, F, F -> F | CC, CACC, GICC |
| `test_lc4_unrestricted_plain_char_kept` | F, F, F -> F | CC, GICC |
| `test_lc5_restricted_whitespace` | T, F, T -> T | CC, CACC, GICC |
| `test_lc6_unrestricted_whitespace_kept` | F, F, T -> F | CC, GICC |
| `test_lc7_restricted_dash_underscore_prefix_stripped` | branch 2155->2156 | branch top-up |
|...|...|...|

How each criterion is met across the set:

- **CC:** clause `a` is true in LC1/LC3/LC5 and false in LC2/LC4/LC6; clause `b`
  is true in LC1/LC2 and false in the rest; clause `c` is true in LC5/LC6 and
  false in the rest. Every clause takes both values.
- **CACC:** `a` is the deciding clause in LC1 vs LC2 (minor clauses held at
  b=T, c=F); `b` is deciding in LC1 vs LC3 (held at a=T, c=F); `c` is deciding
  in LC5 vs LC3 (held at a=T, b=F). Each pair flips only the major clause and
  flips the predicate.
- **GICC:** `a` inactive is shown in LC3 and LC4 (both predicate false; the
  true case is infeasible for an AND); `b` inactive is shown in LC5 (predicate
  true) and LC6 (predicate false); `c` inactive is shown in LC1 (predicate
  true) and LC2 (predicate false).

---

**e) Branch and line coverage after new tests — change analysis:**

> _What are the new coverage values? How and why did branch/line coverage change (or not change)?_
> 
Measured on the combined suite (Task 1 + Task 2 + Task 3 + Task 4
file of mine), branch coverage enabled, restricted to the `sanitize_filename` line
range.

| Metric | Before | After |
|--------|--------|-------|
| Line coverage | 97.0% (32/33) | 100.0% (33/33) |
| Branch coverage | 96.4% (27/28) | 100.0% (28/28) |
| Missing lines | 2156 | none |
| Missing branches | (2155 to 2156) | none |

Analysis: LC1 to LC6 sit on the predicate at line 2137, which the existing suite already covered, so they confirm that predicate under the three logic criteria without moving the numbers on their own. The measurable change comes from LC7, which targets the one previously uncovered branch at line 2155. It covers line 2156 and branch (2155 to 2156), taking the method from 97.0% to 100.0% line coverage and from 96.4% to 100.0% branch coverage. After the run the missing list for `sanitize_filename` contains no lines and no branches, so the method is now fully covered on both criteria.

![alt text](<screenshot/shakil/Logic Test/screenshot_updated_shakil.png>)

---

**Student 2 – [Saimon Chowdhury Fahim]**

**Selected method:** `int_or_none`

**a) Method selection and predicate/clause structure:**
> `int_or_none` converts a value to an int, with optional attribute extraction,
scaling, and a base for string parsing. None of my four assigned methods
(`int_or_none`, `float_or_none`, `str_to_int`, `parse_count`) contains a
3-clause predicate; all of their conditions are single-clause. `int_or_none`
was selected because it has a genuine 2-level nested structure, which the task
allows as an alternative to a flat 3-clause predicate:

```
3874   if get_attr:
3875       if v is not None:
3876           v = getattr(v, get_attr, None)
3877   if v in (None, ''):
3878       return default
```

Because each individual condition is single-clause, flat Active Clause Coverage
or Inactive Clause Coverage would collapse into plain predicate coverage if
applied line by line. Instead, the criteria are applied to the **induced
compound predicate** that controls whether line 3876 executes:

```
A = bool(get_attr)        (line 3874)
B = (v is not None)       (line 3875)
compound:  A AND B
```

This is how logic coverage criteria differ for a nested structure compared to a
flat predicate: there is no single line containing multiple clauses to analyze
directly, so the clauses are pulled from across the nesting levels and combined
under the short-circuit AND semantics that the nesting itself implements. A
direct consequence of that AND semantics is that a clause can only be inactive
when the predicate is forced False by the other clause, so "inactive clause
with predicate True" is infeasible for this structure. Inactive Clause Coverage
below is demonstrated only on the feasible cases.

**b) Baseline branch and line coverage (before new tests):**
> Measured on the existing suite (Task 1 random + Task 2 ISP + Task 3 graph),
branch coverage enabled, restricted to the `int_or_none` line range.

| Metric | Value | Detail |
|--------|-------|--------|
| Line coverage | 80.0% | 8 of 10 statements |
| Branch coverage | 50.0% | 3 of 6 branches |
| Missing lines | 3875, 3876 | the entire `get_attr` nest |
| Missing branches | (3874,3875), (3875,3876), (3875,3877) | all three arcs of the nest |

No existing test ever passes `get_attr`, so the whole nested block is dark.
This is the largest coverage gap of the three selected methods and gives the
clearest before/after signal.

![alt text](<screenshot/saimon/Logic Test/screenshot baseline-saimon.PNG>)


**c) Logic coverage test cases (3 criteria):**

*Criteria selected:*
1. Group 1: Combinatorial Coverage (CoC)
2. Group 2: Correlated Active Clause Coverage (CACC)
3. Group 3: General Inactive Clause Coverage (GICC)

CoC is used instead of Clause Coverage because the compound has only 2 clauses,
so all 4 rows are feasible and cheap to cover; CoC gives the strongest possible
result here. Every expected return value was traced through the real source
before being written into an assertion.

```python
# Logic coverage test cases (Saimon) - int_or_none
# Induced compound predicate for reaching line 3876:
#   A = bool(get_attr), B = (v is not None)

from types import SimpleNamespace
from youtube_dl.utils import int_or_none


# LC1 - A=T, B=T. get_attr truthy and v not None: nest fully entered,
# getattr pulls '42' off the object, which converts to 42.
# Covers branches (3874->3875) and (3875->3876).
# CoC (row TT); CACC (A deciding vs LC3; B deciding vs LC2).
def test_lc1_get_attr_true_value_not_none():
    obj = SimpleNamespace(count='42')
    assert int_or_none(obj, get_attr='count') == 42


# LC2 - A=T, B=F. get_attr truthy but v is None: inner if is False, getattr
# skipped, v stays None, default returned.
# Covers branches (3874->3875) and (3875->3877).
# CoC (row TF); CACC (B deciding vs LC1);
# GICC (clause A inactive, A true, predicate false).
def test_lc2_get_attr_true_value_none():
    assert int_or_none(None, get_attr='count') is None


# LC3 - A=F, B=T. get_attr falsy: nest skipped entirely; v is '42', not
# None, converts to 42.
# Covers the outer-if False path (3874->3877).
# CoC (row FT); CACC (A deciding vs LC1);
# GICC (clause B inactive, B true, predicate false).
def test_lc3_get_attr_false_value_not_none():
    assert int_or_none('42') == 42


# LC4 - A=F, B=F. get_attr falsy and v is None: nest skipped, default
# returned.
# CoC (row FF);
# GICC (clause A inactive with A false; clause B inactive with B false).
def test_lc4_get_attr_false_value_none():
    assert int_or_none(None) is None
```

**d) Coverage criterion contribution per test:**

| Test name | Clause values (A, B), compound | Criteria satisfied |
|-----------|--------------------------------|---------------------|
| `test_lc1_get_attr_true_value_not_none` | T, T -> T | CoC, CACC, GICC |
| `test_lc2_get_attr_true_value_none` | T, F -> F | CoC, CACC, GICC |
| `test_lc3_get_attr_false_value_not_none` | F, T -> F | CoC, CACC, GICC |
| `test_lc4_get_attr_false_value_none` | F, F -> F | CoC, GICC |

How each criterion is met across the set:

- **CoC:** all 4 combinations of (A, B) appear, one per test. With only 2
  clauses this is the complete combinatorial table, no rows are skipped.
- **CACC:** A is the deciding clause in LC1 vs LC3 (B held at True, A flips
  and the result flips); B is the deciding clause in LC1 vs LC2 (A held at
  True, B flips and the result flips).
- **GICC:** A inactive is shown in LC2 (A true, predicate false) and LC4 (A
  false, predicate false); B inactive is shown in LC3 (B true, predicate
  false) and LC4 (B false, predicate false). The "A inactive with predicate
  true" case does not appear because it is infeasible for an AND predicate.

**e) Branch and line coverage after new tests — change analysis:**
> 
Measured on the combined suite (Task 1 + Task 2 + Task 3 + Task 4
file of mine), branch coverage enabled, restricted to the `int_or_none` line range.
This run was executed on my machine (Python 3.10.20, 2456-statement
checkout) rather than the group's Python 3.9 reference machine. The baseline
numbers measured here matched the reference-machine baseline exactly (line
range, missing lines, and missing branches were identical before the new
tests), so the method's coverage is not affected by the version difference and
the before/after comparison below is valid.

| Metric | Before | After |
|--------|--------|-------|
| Line coverage | 80.0% (8/10) | 100.0% (10/10) |
| Branch coverage | 50.0% (3/6) | 100.0% (6/6) |
| Missing lines | 3875, 3876 | none |
| Missing branches | (3874,3875), (3875,3876), (3875,3877) | none |

Analysis: the 4 tests cover all 4 rows of the induced compound predicate
(A, B), which together exercise every branch of the `get_attr` nest. LC1 and
LC2 cover the True direction of the outer `get_attr` check (3874 to 3875);
LC1 covers the inner `v is not None` True direction into the getattr call
(3875 to 3876); LC2 covers the inner False direction (3875 to 3877); LC3 and
LC4 cover the outer `get_attr` False direction, which skips the nest entirely.
Since no earlier test in the suite ever passed `get_attr`, this nest was the
only gap in the method, and these 4 tests close it completely. Line coverage
rises from 80.0% to 100.0% and branch coverage rises from 50.0% to 100.0%,
the largest improvement of the three selected methods in this group.


![alt text](<screenshot/saimon/Logic Test/screenshot updated-saimon.PNG>)


---

**Student  – [Md Tawfiq Bashar]**

**Selected method:** `parse_duration`

**a) Method selection and predicate/clause structure:**
> `parse_duration` converts a duration string into a total number of seconds as a
float. None of my assigned methods (`parse_duration`, `month_by_name`,
`limit_length`, `parse_filesize`) contains a flat 3-clause predicate. All
conditions are single-clause. `parse_duration` was selected because it contains
a genuine 3-level nested if/else chain, which the task allows as an alternative
to a flat 3-clause predicate:

```
3945   if m:                         # level 1: first regex (colon format)
           ...
3947   else:
3948       m = re.match(...)          # second regex (unit format)
3972       if m:                      # level 2
               ...
3974       else:
3975           m = re.match(...)      # third regex (worded decimal format)
3976           if m:                  # level 3
3977               hours, mins = m.groups()
3978           else:
3979               return None
```

Because each individual condition is single-clause, applying Active or Inactive
Clause Coverage line by line would collapse into plain predicate coverage. Instead
the criteria are applied to the induced compound predicate that controls whether
line 3977 executes:

```
m1 = first regex (colon format) matches          (line 3945)
m2 = second regex (unit format) matches          (line 3972)
m3 = third regex (worded decimal format) matches (line 3976)

compound to reach line 3977:  (not m1) AND (not m2) AND m3
```

This is how logic coverage criteria differ for a nested structure compared to a
flat predicate: the clauses are distributed across three nesting levels and are
only observable under short-circuit semantics. When m1 is True, m2 and m3 are
never evaluated at all; when m2 is True, m3 is never evaluated. An inner clause
cannot therefore be made inactive in the textbook sense when an outer clause
short-circuits execution. Inactive Clause Coverage below is demonstrated only
at the points where each clause is genuinely observable.

One structural property worth noting: the third regex uniquely accepts decimal
hours and minutes (pattern `[0-9.]+`), while the second regex only accepts
integers (`[0-9]+`). This means inputs like `'2 hours'` actually match the
second regex and never reach the third branch. Only decimal inputs such as
`'1.5 hours'` reach line 3976. This was verified empirically during test
development and is a direct consequence of the nesting structure.

**b) Baseline branch and line coverage (before new tests):**
> Measured on the existing suite (Task 1 random + Task 2 ISP + Task 3 graph),
branch coverage enabled, restricted to the `parse_duration` line range.

| Metric | Value | Detail |
|--------|-------|--------|
| Line coverage | 94.7% | 18 of 19 statements |
| Branch coverage | 90.0% | 9 of 10 branches |
| Missing line | 3977 | the worded decimal format result assignment |
| Missing branch | (3976,3977) | True direction of the third regex match |

The existing graph coverage tests (Task 3) already exercised the colon and unit
format branches. The worded decimal branch at line 3976 was never triggered
because all earlier test inputs using plain integer words matched the second
regex before reaching the third.


![alt text](<screenshot/Tawfiq/Logic/screenshot_baseline_tawfiq.png>)

**c) Logic coverage test cases (3 criteria):**

*Criteria selected:*
1. Group 1: Clause Coverage (CC)
2. Group 2: Correlated Active Clause Coverage (CACC)
3. Group 3: General Inactive Clause Coverage (GICC)

All expected return values were verified by executing the real source before
writing assertions. The key discovery during verification was that decimal
notation (e.g. `'1.5 hours'`) is required to reach the third regex, because
plain integer words (e.g. `'2 hours'`) are absorbed by the second regex.

```python
# Logic coverage test cases (Tawfiq) - parse_duration
# Induced compound for reaching line 3977:
#   (not m1) AND (not m2) AND m3

from youtube_dl.utils import parse_duration


# LC1 - non-string input, guard branch before any regex.
# Covers the isinstance guard True direction. All three regex decisions
# are unreachable from here.
# CC (all regex clauses in an unreachable state, distinct observable state);
# GICC (m2 and m3 not reachable, effectively inactive).
def test_lc1_non_string_returns_none():
    assert parse_duration(123) is None


# LC2 - garbage string, all three regexes fail.
# m1=False, m2=False, m3=False -> returns None.
# CC (m1=F, m2=F, m3=F);
# CACC (m3 deciding: m1 and m2 both False, m3=False gives None);
# GICC (m3 inactive with m3=False, predicate False).
def test_lc2_no_match_returns_none():
    assert parse_duration('garbage') is None


# LC3 - colon HH:MM:SS format, first regex matches.
# m1=True, m2 and m3 never evaluated.
# 1*3600 + 2*60 + 3 = 3723.0
# CC (m1=T);
# CACC (m1 deciding: m1=True takes the first branch vs m1=False in LC5/LC7);
# GICC (m2 and m3 inactive because m1 short-circuits the nest).
def test_lc3_colon_hms_format():
    assert parse_duration('1:02:03') == 3723.0


# LC4 - colon format with milliseconds sub-group.
# m1=True, milliseconds group captured.
# 1*60 + 30 + 0.5 = 90.5
# CC (m1=T with ms sub-group, distinct path from LC3).
def test_lc4_colon_with_milliseconds():
    assert parse_duration('1:30.5') == 90.5


# LC5 - unit format "1h30m", first regex fails, second matches.
# m1=False, m2=True, m3 never evaluated.
# 1*3600 + 30*60 = 5400.0
# CC (m2=T);
# CACC (m2 deciding: m1=False, m2=True gives result vs m2=False in LC7).
def test_lc5_unit_format_hours_minutes():
    assert parse_duration('1h30m') == 5400.0


# LC6 - unit format seconds only, second regex matches.
# m1=False, m2=True.
# 30.0
# CC (m2=T with secs only, distinct from LC5);
# GICC (m3 inactive because m2 short-circuits).
def test_lc6_unit_format_seconds():
    assert parse_duration('30s') == 30.0


# LC7 - decimal hours "1.5 hours", first and second regexes fail, third matches.
# The second regex only accepts integer digits ([0-9]+h), so "1.5 hours" fails
# it. The third regex accepts decimals ([0-9.]+), so it matches here.
# m1=False, m2=False, m3=True -> line 3977 executed.
# 1.5 * 3600 = 5400.0
# This is the ONLY test that covers the missing branch (3976->3977).
# CC (m3=T);
# CACC (m3 deciding vs LC2: m1=False m2=False, flip m3 True->False);
# GICC (m3 inactive with m3=False shown in LC2, predicate False).
def test_lc7_decimal_hours_worded_format():
    assert parse_duration('1.5 hours') == 5400.0


# LC8 - decimal minutes "2.5 mins", first and second regexes fail, third matches.
# m1=False, m2=False, m3=True -> line 3977 executed.
# 2.5 * 60 = 150.0
# CC (m3=T, mins group vs hours group in LC7).
def test_lc8_decimal_minutes_worded_format():
    assert parse_duration('2.5 mins') == 150.0
```

**d) Coverage criterion contribution per test:**

| Test name | Clause values (m1, m2, m3) | Criteria satisfied |
|-----------|----------------------------|--------------------|
| `test_lc1_non_string_returns_none` | unreachable | CC, GICC |
| `test_lc2_no_match_returns_none` | F, F, F | CC, CACC, GICC |
| `test_lc3_colon_hms_format` | T, -, - | CC, CACC, GICC |
| `test_lc4_colon_with_milliseconds` | T, -, - | CC |
| `test_lc5_unit_format_hours_minutes` | F, T, - | CC, CACC |
| `test_lc6_unit_format_seconds` | F, T, - | CC, GICC |
| `test_lc7_decimal_hours_worded_format` | F, F, T | CC, CACC, GICC |
| `test_lc8_decimal_minutes_worded_format` | F, F, T | CC |

How each criterion is met across the set:

- **CC:** m1 is True in LC3/LC4 and False in LC2/LC5/LC6/LC7/LC8; m2 is True
  in LC5/LC6 and False in LC2/LC7/LC8 (not evaluated when m1=True); m3 is
  True in LC7/LC8 and False in LC2 (not evaluated when m1 or m2 is True).
  Every clause takes both values where it is observable.
- **CACC:** m1 is the deciding clause in LC3 vs LC5 (m1 flips, result path
  changes); m2 is the deciding clause in LC5 vs LC7 (m1=False held, m2 flips,
  result changes); m3 is the deciding clause in LC7 vs LC2 (m1=False and
  m2=False held, m3 flips, result changes from 5400.0 to None).
- **GICC:** m1 inactive is shown in LC5/LC6 (m1=False, predicate False because
  m2=True) and LC7/LC8 (m1=False, predicate True because m3=True); m2 inactive
  is shown in LC3 (m1 short-circuits, m2 not evaluated); m3 inactive is shown
  in LC2 (m3=False, predicate False) and in LC5/LC6 (m2 short-circuits, m3
  not evaluated). The "inactive clause with predicate True" case for outer
  clauses is infeasible under short-circuit AND semantics, which is the core
  difference from flat-predicate ICC.


**e) Branch and line coverage after new tests — change analysis:**
> 
Measured on the combined suite (Task 1 + Task 2 + Task 3 + Task 4
file of mine), branch coverage enabled, restricted to the `parse_duration` line range.
Run on the group's Python 3.9 reference machine (2453-statement checkout).

| Metric | Before | After |
|--------|--------|-------|
| Line coverage | 94.7% (18/19) | 100.0% (19/19) |
| Branch coverage | 90.0% (9/10) | 100.0% (10/10) |
| Missing lines | 3977 | none |
| Missing branches | (3976,3977) | none |

Analysis: LC1 to LC6 cover paths through the first and second regex branches,
which were already covered by earlier tests. They confirm those paths under the
three logic criteria without moving the numbers on their own. The measurable
change comes from LC7 and LC8, which provide the first inputs that fail both
the colon and unit regexes and match the third worded decimal regex. LC7 covers
line 3977 and branch (3976 to 3977), and LC8 provides a second confirmation
through the same branch with the minutes group. Line coverage rises from 94.7%
to 100.0% and branch coverage rises from 90.0% to 100.0%. After the run the
missing list for `parse_duration` contains no lines and no branches.

![alt text](<screenshot/Tawfiq/Logic/screenshot_updated_tawfiq.png>)


---

*(add a block per additional group member)*

---

> **Note:** This phase has **no AI Review sub-task**. The Differential Prompting task
> (based on Research Paper 05) is dropped, as Paper 05 falls outside the adjusted course
> schedule — so there is no AI Review documentation to submit for Task 04.

---

## Contribution Overview

Fill in the **Member** column headers with each group member's name. **Adapt the rows
to your own work** — replace the example method names with the methods you actually
selected (one row per group member), add or remove rows as needed, and mark with an **×**
who contributed to which sub-task. Add a short note where it helps clarify the split of work.

| Sub-task / Item | Shakil | Saimon | Tawfiq | 
|-----------------|:--------:|:--------:|:--------:|
| Method 1: `Santize_filename` (selection & predicate analysis) | × |  |  |
| Method 2: `int_or_none` (selection & predicate analysis) |  | × |  |
| Method 3: `parse_duration` (selection & predicate analysis) |  |  | × | 
| Baseline coverage measurement (b) | × | × | × |
| Logic coverage test cases (c) | × | × | × |
| Coverage annotation per test (d) | × | × | × |
| Post-test coverage analysis (e) | × | × | × |
