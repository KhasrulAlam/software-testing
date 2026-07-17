# Project – Phase 02 Submission
**Software Testing – Input Space Partitioning**

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

## Task 02 – Input Space Partitioning

Each group member independently selects **one method** of the project and applies the input domain model (IDM) approach. Add your test files to the repository under `task-2-isp/` and make **individual commits**.

---

### Individual Method Selection (per group member)

**Student 1 – [S M Khasrul Alam Shakil]**

**Selected method:** `remove_start`

**a) Why is this method suitable for the IDM approach? (1–2 sentences)**
> remove_start takes two string parameters and its behavior clearly depends on whether s starts with start or not, whether either is None, and the relationship between string lengths. These distinct categories map naturally to equivalence classes.

**b) Describe the input domain of the method (2–3 sentences):**
> The function takes two parameters s and start. If s is None it returns None immediately. If s does not start with start it returns s unchanged. If s starts with start it returns s with start removed from the beginning. Both parameters are expected to be strings.

**c) Characteristics and partitions:**

*Interface-based characteristic:*

| Characteristic | Block 1 | Block 2 | Block 3 |
|---|---|---|---|
| `q1 = "type of s"` | `None` | empty string `""` | non-empty string |
| `q2 = "type of start"` | empty string `""` | non-empty string | |

*Functionality-based characteristic:*

| Characteristic | Block 1 | Block 2 | Block 3 |
|---|---|---|---|
| `q1 = "s starts with start"` | yes, s starts with start | no, s does not start with start | start is longer than s |
| `q2 = "position of match"` | full match (s equals start exactly) | partial match (start is prefix of longer s) | no match |

**d) Non-valid block combinations and constraints (1–2 sentences):**
> When s is None all functionality-based characteristics are irrelevant because the function returns None immediately. When start is an empty string every string technically starts with it so the match block always applies, but the result is always s unchanged since removing an empty prefix changes nothing.

**e) Representative values per block and selection strategy:**
> Strategy used: boundary value for None and empty. Typical value for normal string cases.

| Characteristic | Block | Representative value |
|---|---|---|
| `q1` type of s | None | `None` |
| `q1` type of s | empty | `""` |
| `q1` type of s | non-empty | `"Hello World"` |
| `q2` length limit | very small | `3` |
| `q2` length limit | normal | `10` |
| `q2` length limit | very large | `10000` |
| string vs limit | shorter than limit | `s="Hi"`, `length=10` |
| string vs limit | equal to limit | `s="Hello"`, `length=5` |
| string vs limit | longer than limit | `s="Hello World"`, `length=8` |

**f) `hypothesis` test vectors (relevant code excerpt):**
```python

# TV1: q1=None, q2=non-empty, starts_with=n/a → must return None
@given(st.just(None), st.text(min_size=1))
def test_tv1_s_is_none(s, start):
    assert remove_start(s, start) is None


# TV2: q1=empty, q2=non-empty, starts_with=n/a → must return empty string unchanged
@given(st.just(""), st.text(min_size=1))
def test_tv2_s_is_empty(s, start):
    assert remove_start(s, start) == ""


# TV3: q1=non-empty, q2=empty, starts_with=n/a → must return s unchanged
@given(st.just("hello world"), st.just(""))
def test_tv3_start_is_empty(s, start):
    assert remove_start(s, start) == "hello world"


# TV4: q1=non-empty, q2=non-empty, starts_with=yes partial → must remove prefix
@given(st.just("hello world"), st.just("hello"))
def test_tv4_starts_with_partial_match(s, start):
    result = remove_start(s, start)
    assert result == " world"


# TV5: q1=non-empty, q2=non-empty, starts_with=yes full match → must return empty string
@given(st.just("hello"), st.just("hello"))
def test_tv5_starts_with_full_match(s, start):
    result = remove_start(s, start)
    assert result == ""


# TV6: q1=non-empty, q2=non-empty, starts_with=no match → must return s unchanged
@given(st.just("world"), st.just("hello"))
def test_tv6_no_match(s, start):
    assert remove_start(s, start) == "world"
```

![alt text](<screenshot/shakil/Input Space Partitioning/isp_test-shakil.png>)

---

**Student 2 – [Saimon Chowdhury Fahim]**

**Selected method:** `int_or_none`

**a) Why is this method suitable for the IDM approach? (1–2 sentences)**
> int_or_none has multiple parameters with clearly different categories for the main input v such as None, empty string, valid integer string, float string, and non-numeric string, combined with a scale parameter that affects the output value. This makes it rich in both interface and functionality partitions.

**b) Describe the input domain of the method (2–3 sentences):**
> The main parameter v can be None, an empty string, a numeric string, an integer, a float, or a non-numeric string. The scale parameter divides the result and defaults to 1. The default parameter is returned when conversion fails. The invscale parameter multiplies the result. If get_attr is set the function first extracts an attribute from v. The function returns an integer or the default value.

**c) Characteristics and partitions:**

*Interface-based characteristic:*

| Characteristic | Block 1 | Block 2 | Block 3 | Block 4 |
|---|---|---|---|---|
| `q1 = "type of v"` | `None` | empty string `""` | integer | string |
| `q2 = "scale value"` | 1 (default) | greater than 1 |  |



*Functionality-based characteristic:*

| Characteristic | Block 1 | Block 2 | Block 3 |
|---|---|---|---|
| `q1 = "numeric content of v"` | valid integer string (`"42"`) | float string (`"3.14"`) | non-numeric string (`"abc"`) |
| `q2 = "sign of v"` | positive | negative | zero |


**d) Non-valid block combinations and constraints (1–2 sentences):**
> When v is None or empty string the function returns default immediately so numeric content and sign characteristics are irrelevant. Float strings cannot be converted to int directly and will return default so the sign characteristic does not apply to them meaningfully.

**e) Representative values per block and selection strategy:**
<<<<<<< HEAD
> Strategy used: boundary value for None, empty and zero. Typical value for normal numeric cases.

=======
> 
Strategy used: boundary value for None, empty and zero. Typical value for normal numeric cases.
>>>>>>> 1056ebb6b96715c3450693c42beddd3d9313f13a
| Characteristic | Block | Representative value |
|---|---|---|
| `q1` type | None | `None` |
| `q1` type | empty string | `""` |
| `q1` type | integer | `42` |
| `q1` type | string | `"42"` |
| `q2` scale | default (1) | `1` |
| `q2` scale | greater than 1 | `10` |
| numeric content | valid integer string | `"42"` |
| numeric content | float string | `"3.14"` |
| numeric content | non-numeric | `"abc"` |
| sign | positive | `"42"` |
| sign | negative | `"-42"` |
| sign | zero | `"0"` |




**f) `hypothesis` test vectors (relevant code excerpt):**
```python

# TV1: q1=None, q2=non-empty, starts_with=n/a → must return None
@given(st.just(None), st.text(min_size=1))
def test_tv1_s_is_none(s, start):
    assert remove_start(s, start) is None


# TV2: q1=empty, q2=non-empty, starts_with=n/a → must return empty string unchanged
@given(st.just(""), st.text(min_size=1))
def test_tv2_s_is_empty(s, start):
    assert remove_start(s, start) == ""


# TV3: q1=non-empty, q2=empty, starts_with=n/a → must return s unchanged
@given(st.just("hello world"), st.just(""))
def test_tv3_start_is_empty(s, start):
    assert remove_start(s, start) == "hello world"


# TV4: q1=non-empty, q2=non-empty, starts_with=yes partial → must remove prefix
@given(st.just("hello world"), st.just("hello"))
def test_tv4_starts_with_partial_match(s, start):
    result = remove_start(s, start)
    assert result == " world"


# TV5: q1=non-empty, q2=non-empty, starts_with=yes full match → must return empty string
@given(st.just("hello"), st.just("hello"))
def test_tv5_starts_with_full_match(s, start):
    result = remove_start(s, start)
    assert result == ""


# TV6: q1=non-empty, q2=non-empty, starts_with=no match → must return s unchanged
@given(st.just("world"), st.just("hello"))
def test_tv6_no_match(s, start):
    assert remove_start(s, start) == "world"



```

![alt text](<screenshot/saimon/Input Space Partitioning/test-isp-saimon.PNG>)
---

*(add a block per additional group member)*

**Student 3 – [Md Tawfiq Bashar]**

**Selected method:** `limit_length(s, length)`

**a) Why is this method suitable for the IDM approach? (1–2 sentences)**
> limit_length takes a string and an integer length limit and its behavior clearly depends on whether s is None, whether the string is shorter or longer than the limit, and what the limit value is. These distinct categories produce very different outputs making it a natural fit for ISP.


**b) Describe the input domain of the method (2–3 sentences):**
> The function takes s which can be None or a string, and length which is a positive integer. If s is None it returns None. If the length of s is within the limit it returns s unchanged. If s is longer than length it truncates s and appends ... so the total length equals length.

**c) Characteristics and partitions:**

*Interface-based characteristic:*

| Characteristic | Block 1 | Block 2 | Block 3 |
|---|---|---|---|
| `q1 = "type of s"` | `None` | empty string `""` | non-empty string |
| `q2 = "length limit value"` | very small (3 or less) | normal positive integer | very large integer |


*Functionality-based characteristic:*

| Characteristic | Block 1 | Block 2 | Block 3 |
|---|---|---|---|
| `q1 = "string length vs limit"` | string shorter than limit | string equal to limit | string longer than limit |
| `q2 = "truncation result"` | no truncation needed | truncated with ellipses appended | |

**d) Non-valid block combinations and constraints (1–2 sentences):**
> When s is None both length comparison and truncation characteristics are irrelevant. When s is empty the string is always shorter than or equal to any positive limit so truncation never applies. The truncation result block only applies when the string is longer than the limit.

**e) Representative values per block and selection strategy:**
> Strategy used: boundary value for None, empty, equal length and very small limit. Typical value for normal truncation cases.

| Characteristic | Block | Representative value |
|---|---|---|
| `q1` type of s | None | `None` |
| `q1` type of s | empty | `""` |
| `q1` type of s | non-empty | `"Hello World"` |
| `q2` length limit | very small | `3` |
| `q2` length limit | normal | `10` |
| `q2` length limit | very large | `10000` |
| string vs limit | shorter than limit | `s="Hi"`, `length=10` |
| string vs limit | equal to limit | `s="Hello"`, `length=5` |
| string vs limit | longer than limit | `s="Hello World"`, `length=8` |



**f) `hypothesis` test vectors (relevant code excerpt):**
```python

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




```

![alt text](<screenshot/Tawfiq/Input Space Partitioning/test-isp-tawfiq.png>)


---

## AI Review Task

As a group, choose one of the methods selected above and instruct an LLM to:
- derive multiple characteristics with value blocks,
- generate `hypothesis` test cases for those blocks,
- identify conflicting or constrained block combinations.

**LLM used:**
> Gemini

**Prompts used:**
> "For the test function parse_filesize from the youtube-dl project (https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/utils.py). Do the following tasks: derive multiple interface-based and functionality-based characteristics with value blocks and present them as tables, identify any conflicting or constrained block combinations that should not be tested together, and generate Python hypothesis test using pytest that covers different block combinations. Annotated the test with proper comment to indicate the blocks it covers."


**Generated characteristics and tests:**

Interface-based characteristics generated by Gemini:
| Characteristic | Block 1 | Block 2 | Block 3 | Block 4 | Block 5 |
|---|---|---|---|---|---|
| `q1 = "input data type"` | String | None | Non-string | | |
| `q2 = "string format"` | Number + space + unit (`"5 GB"`) | Number + unit no space (`"5GB"`) | Missing number (`"MB"`) | Missing unit (`"1024"`) | Empty string (`""`) |

Functionality-based characteristics generated by Gemini:
| Characteristic | Block 1 | Block 2 | Block 3 | Block 4 | Block 5 |
|---|---|---|---|---|---|
| `q1 = "numeric value type"` | Integer (`"10"`) | Decimal (`"1.5"`) | | | |
| `q2 = "unit case sensitivity"` | Uppercase (`"MB"`) | Lowercase (`"mb"`) | Mixed case (`"mB"`) | | |
| `q3 = "supported unit scale"` | Bytes (`B`) | Kilobytes (`KB`/`KiB`) | Megabytes (`MB`/`MiB`) | Gigabytes (`GB`/`GiB`) | Terabytes (`TB`/`TiB`) |

Conflicting combinations identified by Gemini:
None input and non-string inputs cannot be combined with any string format, numeric value type, or unit scale blocks. Missing number or empty string inputs cannot be combined with numeric value type blocks. Missing unit inputs cannot be combined with any unit scale block.

```python
import pytest
from hypothesis import given, strategies as st
from youtube_dl.utils import parse_filesize

UNIT_MULTIPLIERS = {
    'b': 1,
    'kb': 1024, 'kib': 1024,
    'mb': 1024**2, 'mib': 1024**2,
    'gb': 1024**3, 'gib': 1024**3,
    'tb': 1024**4, 'tib': 1024**4,
}

# Covers: input type=string, format=with/without space,
# numeric=integer and decimal, case=upper and lower, unit=all scales
@given(
    num=st.one_of(
        st.integers(min_value=1, max_value=10000),
        st.floats(min_value=0.1, max_value=10000.0, allow_nan=False, allow_infinity=False)
    ),
    unit=st.sampled_from(list(UNIT_MULTIPLIERS.keys())),
    has_space=st.booleans(),
    make_upper=st.booleans()
)
def test_parse_filesize_combinations(num, unit, has_space, make_upper):
    unit_str = unit.upper() if make_upper else unit.lower()
    space = " " if has_space else ""
    input_string = f"{num}{space}{unit_str}"
    expected_bytes = int(float(num) * UNIT_MULTIPLIERS[unit.lower()])
    result = parse_filesize(input_string)
    assert result == expected_bytes

def test_parse_filesize_invalid_inputs():
    # Covers: input type=None, format=empty string, format=unrecognized
    assert parse_filesize(None) is None
    assert parse_filesize("") is None
    assert parse_filesize("invalid_text") is None
```

**Viewpoint analysis – comparing LLM output with your own work:**
> Did the LLM identify meaningful characteristics? Were the generated tests correct and useful?

Gemini identified mostly the same characteristics as our group such as input type, string format, numeric value type and unit scale. However it missed the decimal separator characteristic (dot vs comma) which is explicitly supported in the real source code. The generated test also had incorrect expected values because Gemini assumed all units are 1024-based but the real code uses KB = 1000 and KiB = 1024, making its assertions wrong for SI units.

> Did it correctly handle constraints between blocks?

Gemini correctly identified the main constraints such as None and non-string inputs making all string characteristics irrelevant, and missing number or unit making their respective characteristics irrelevant. However it missed the constraint related to the comma decimal separator since it never identified that characteristic in the first place.


---

## Contribution Overview

Indicate which group member contributed to which sub-task by placing an **×** in the corresponding cell.

| Sub-task | Khasrul | Saimon | Tawfiq |
|----------|:--------:|:--------:|:--------:|
| Method selection & IDM (a–f) |×|×| | 
| Test implementation (6×n tests) |x|×|×| 
| AI Review Task (viewpoint analysis) | ||×| 
