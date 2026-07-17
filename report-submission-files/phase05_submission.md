# Project – Phase 05 Submission
**Software Testing – Syntax Coverage**

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

## Task 05 – Syntax Coverage

---

### 1 – Mutation Tool Selection

As a group, select **one mutation testing tool** for Python. Possible tools include (but are not limited to): `mutmut`, `cosmic-ray`, `MutPy`, `mutatest`, `PyMuTester`.

**Selected tool:**
> `mutatest` version 3.0.2. We first tried `mutmut`, but it requires OS-level fork support and cannot run natively on Windows (only inside WSL), which is not part of our environment. `mutatest` is tested on Linux, Windows, and macOS, installs cleanly with `pip install mutatest` in our conda environment, and works directly on Python's AST, reporting mutations by category (e.g. `Compare`, `CompareIs`, `BinOp`), which maps cleanly onto the mutation operator table used in this task.

---

### 2 – Mutation Operator Analysis

Run the tool and determine the number of **killed mutants** for at least **n distinct mutation operators**, where *n* is the number of group members.

| Mutation operator | Total mutants | Killed | Survived | Kill rate |
|-------------------|--------------|--------|----------|-----------|
| CompareIs (`is` / `is not`) | 5 | 3 | 2 | 60.0% |
| Compare (`==`, `!=`, `<`, `<=`, `>`, `>=`) | 40 | 28 | 12 | 70.0% |
| BinOp (`+`, `-`, `*`, `/`, `//`, `%`, `**`) | 258 | 55 | 203 | 21.3% |


![alt text](<screenshot/shakil/Syntax Coverage/screenshot_mutation.png>)


>These totals come from a single `mutatest` run in full mode (`-m f`), whitelisted to these three categories (`-w cs cp bn`), sampling 60 of 98 available locations in `youtube_dl/utils.py` with a fixed random seed (`-r 42`), against our combined test suite from Tasks 1-4 (67 tests, all passing).

>Note on the BinOp result: the low 21.3% kill rate is almost entirely driven by 203 surviving `Pow` mutants inside `parse_filesize` (lines 3661-3706), which contains a large static unit-conversion table (e.g. `1024 ** 2`, `1024 ** 3`). This method is one of Tawfiq's Task 1-4 assignments but was not the method selected for Task 4's logic coverage RIP work. Restricted only to our three RIP-focus methods below, BinOp kill rates are much healthier (see Section 3).
---

### 3 – RIP Analysis (per mutation operator)

For each of the operators above, pick **one distinct affected method** and analyse a representative mutation instance with respect to **Reachability**, **Infection**, and **Propagation**. 

---
**Operator 1 – CompareIs**

**Method:** `int_or_none` 

*Mutation applied (line, original → mutated):*
> Line 3881: `return (int(v) if base is None else int(v, base=base)) * invscale // scale`
> `base is None` → `base is not None`

**Reachability:** Under what conditions does execution reach the mutation point?
> Execution reaches line 3881 whenever `int_or_none` is called with a value `v` that is not `None` and not the empty string (the guard on line 3877 returns early otherwise), and the call does not raise before this point.

**Infection:** How does the mutated expression produce a different program state?
> Most calls in our test suite pass no `base` argument, so `base` defaults to `None`. In the original code, `base is None` is `True`, so `int(v)` is evaluated. Under the mutation, `base is not None` is `False` for these same calls, so the `else` branch runs instead: `int(v, base=base)`, which is `int(v, base=None)`. Passing `base=None` explicitly to `int()` raises a `TypeError`, which is caught by the surrounding `except` clause, so `v` is set to the function's `default` value instead of the parsed integer.

**Propagation:** How does the infected state affect the final output or observable behaviour?
> The function's return value changes from the correctly parsed integer (e.g. `42`) to `default` (`None` unless otherwise specified), which is directly observable in any test asserting a specific returned integer.

**Does the existing test suite kill this mutant?**
> Yes. `test-logic-saimon.py::test_lc1_get_attr_true_value_not_none` calls `int_or_none(obj, get_attr='count')` and asserts the result equals `42`. Under the mutation this call raises internally and returns `None` instead, so the assertion fails. Confirmed by `mutatest`: DETECTED at (3881, 26).

---

**Operator 2 – Compare**

**Method:** `sanitize_filename` 

*Mutation applied:*
> Line 2131 (inside `replace_insane`): `elif char == '"':` → `elif char != '"':`

**Reachability:**
> `replace_insane` is called once per character of the input string via `''.join(map(replace_insane, s))`. The comparison at line 2131 is reached for any character that did not already match the accent-character branch, the `?`/control-character branch, or the earlier conditions on line 2129.

**Infection:**
> For an input character that literally is `"`, the original condition `char == '"'` evaluates `True`, so the function returns `''` (restricted) or `'` (unrestricted). The mutated condition `char != '"'` evaluates `False` for that same character, so this branch is skipped, and the character falls through to later checks instead of being replaced.

**Propagation:**
> The `"` character is no longer stripped or replaced in the output string, so the final sanitized filename differs from the expected result whenever the input contains a double quote.

**Does the existing test suite kill this mutant?**
> Yes. `test-graph-shakil.py::test_gc3_restricted_quote_and_colon` calls `sanitize_filename('a":b', restricted=True)` and asserts the result equals `'a_-b'`. Under the mutation the quote is left in place instead of removed, so the result no longer matches. Confirmed by `mutatest`: DETECTED at (2131, 13).

---

**Operator 3 – BinOp**

**Method:** `parse_duration`

*Mutation applied:*
> Line 3986: `+ (float(ms) / 10 ** len(ms) if ms else 0))` → `10 ** len(ms)` replaced with `10 + len(ms)`

**Reachability:**
> This line is only reached when `ms` (a fractional-seconds group) was captured by one of the three duration regexes, e.g. for an input like `'1:30.5'` where `.5` is the milliseconds part.

**Infection:**
> The original code divides the captured milliseconds string by a power of ten matching its digit length, converting `'5'` into `0.5` (`5 / 10**1`). The mutation replaces the exponentiation with addition: `5 / (10 + 1) = 5 / 11 ≈ 0.4545`. The computed fractional-second value differs from the correct one.

**Propagation:**
> This incorrect fractional value is added into the total `duration` returned by the function, so the final returned number of seconds is wrong whenever a milliseconds component is present in the input.

**Does the existing test suite kill this mutant?**
> Yes. `test-graph-tawfiq.py::test_gc4_colon_with_milliseconds` calls `parse_duration('1:30.5')` and asserts the result equals `90.5`. Under this mutation the computed value differs from `90.5`, so the assertion fails. Confirmed by `mutatest`: DETECTED at (3986, 23), mutation to `Add`.

> Note: not every sub-mutation at this same location is caught. `mutatest` also tried replacing `**` with `//`, `/`, and `*` at this exact spot, and all three of those survived, since our test suite only checks one specific `ms` value (`'5'`) and does not happen to expose the difference for those particular operator substitutions. This is a genuine, documented gap in our test suite's coverage of this line.

---

### 4 – Uppaal Automaton

Pick **one method or class** with integer-valued inputs/outputs and derive a finite automaton modelling its behaviour in Uppaal.

**Selected method/class:** `urshift(val, n)` from `youtube_dl/utils.py`:

**Automaton description / Uppaal screenshot:**
```python
def urshift(val, n):
    return val >> n if val >= 0 else (val + 0x100000000) >> n
```
This method was chosen because it is restricted to integer inputs and output (no strings, no `None` handling), which maps directly onto Uppaal's integer domain, unlike our other focus methods (`sanitize_filename`, `int_or_none`, `parse_duration`), which operate on strings.

**Modelling simplification:** Uppaal's integer variables are bounded and cannot represent `0x100000000` (2^32) directly. We scaled the model down while preserving the exact same branching structure: `val` ranges over `[-8, 7]` and the wraparound constant `OFFSET = 16` (representing 2^4) replaces `0x100000000` (2^32). The relationship `offset = 2^(bit-width)` is preserved, only the bit-width is shrunk from 32 to 4 so the state space stays small enough to verify.

**Automaton description / Uppaal screenshot:**
![alt text](<screenshot\shakil\Syntax Coverage\subtask-4_editor_tab.png>)


The model (template `Automaton`, process instance `Proc`) has 3 locations and 4 edges:

| Location | Role |
|---|---|
| `Init` | Initial location. Nondeterministically selects an input pair `(v, k)` where `v : int[-8,7]` and `k : int[0,3]`. |
| `Positive` | Reached when `v >= 0`. Computes `result = v >> k`. |
| `Negative` | Reached when `v < 0`. Computes `result = (v + OFFSET) >> k`. |

| Edge | Guard | Update |
|---|---|---|
| `Init → Positive` | `v >= 0` | `val = v, n = k, result = v >> k` |
| `Init → Negative` | `v < 0` | `val = v, n = k, result = (v + OFFSET) >> k` |
| `Positive → Init` | (none) | (none) |
| `Negative → Init` | (none) | (none) |

We manually verified the computation against the real Python function using the Symbolic Simulator: `v=3, k=1` (Positive branch) gave `result=1`, matching `3 >> 1 = 1`. `v=-3, k=1` (Negative branch) gave `result=6`, matching `(-3 + 16) >> 1 = 13 >> 1 = 6`.
---

### 5 – Formal Requirements and Query Verification

Formulate **at least 2 formal requirements** for your model and express them as Uppaal queries. Run the queries and report the results.

![alt text](<screenshot\shakil\Syntax Coverage\subtask-4_verifier_tab.png>)

**Requirement 1:**
> The model never reaches a state with no enabled outgoing transitions (deadlock freedom).

*Uppaal query:*
```
A[] not deadlock
```
*Result:*
> Satisfied. No counterexample was generated, since the property holds. Both `Init` (via its two outgoing edges) and `Positive`/`Negative` (via their unconditional return edges) always have an enabled transition.

---

**Requirement 2:**
> It is possible for the model to take the negative-input branch (the `Negative` location is reachable, i.e. it is not dead code in the model).

*Uppaal query:*
```
E<> state.goal
```
*Result:*
> Satisfied. `Negative` is reachable, since the input domain `v : int[-8,7]` includes negative values and the `Init → Negative` edge is guarded only by `v < 0`.

---

### 6 – Expression Mutation in the Model

Apply **one mutation operator** from the provided table to **one expression** in your Uppaal model. Re-run your queries.

![alt text](<screenshot\shakil\Syntax Coverage\subtask-6_editor_tab.png>)
![alt text](<screenshot\shakil\Syntax Coverage\subtask-6_verifier_tab.png>)

**Mutation applied:**
> We applied an AOR (Arithmetic Operator Replacement) mutation from Table 2 to the `Init → Negative` edge's update expression. The original `result = (v + OFFSET) >> k` was changed to `result = (v - OFFSET) >> k` (`+` replaced with `-`).

**Query results after mutation:**
> Both requirements remained satisfied after the mutation:
> - `A[] not deadlock`: still satisfied.
> - `E<> Proc.Negative`: still satisfied.
>
> This is a real, useful finding rather than an unexpected one: neither requirement inspects the value of `result`, only reachability and deadlock-freedom of locations. The mutation clearly changes the computed value (e.g. for `v=-3`, the correct result is `6`, but the mutant computes `(-3 - 16) >> 1 = -10`, a negative and incorrect value), but this incorrect computation does not affect whether `Negative` is reachable or whether the model deadlocks. This mutant "survives" both of our formal requirements, showing that reachability/deadlock-style properties alone are not sufficient to catch data-computation bugs; a requirement that inspects `result` directly would be needed to kill this mutant.

**Counterexample / killing test vector (if applicable):**
> Not applicable. Since both queries remained satisfied, no counterexample or violation was produced.

---

### 7 – Transition Rerouting

Reroute **one transition** in your model (connect it to a different destination state). Re-run your queries.

![alt text](<screenshot\shakil\Syntax Coverage\subtask-7_editor_tab.png>)
![alt text](<screenshot\shakil\Syntax Coverage\subtask-7_verifier_tab.png>)
**Transition changed:**
>The `Init → Negative` edge (guard `v < 0`, update `val = v, n = k, result = (v + OFFSET) >> k`) was rerouted to instead point from `Init` to `Positive`, while keeping the same guard and update. This means whenever a negative `v` is selected, the model now moves to `Positive` (still computing the correct negative-branch arithmetic in `result`, but landing in the wrong location), and no edge leads into `Negative` any more.

**Query results after rerouting:**
> - `A[] not deadlock`: still satisfied. `Init` and `Positive` still form a working loop, so the model never gets stuck, even though `Negative` is now unreachable.
> - `E<> Proc.Negative`: **not satisfied** (flipped from satisfied to violated). Since no edge leads into `Negative` any more, it is now unreachable dead code in the model.
>
> This shows the rerouting mutation was caught by Requirement 2, in contrast to the arithmetic mutation in Section 6, which was not caught by either requirement.

**Counterexample / killing test vector (if applicable):**
> Not directly applicable in the usual sense. `E<> Proc.Negative` is a reachability query; when it is not satisfied, Uppaal reports that no path exists to prove non-reachability, rather than producing a counterexample trace (a counterexample trace only makes sense for a violated invariant, not a failed existential reachability check).

---

## Contribution Overview

Fill in the **Member** column headers with each group member's name and mark with an **×**
who contributed to which sub-task. **Adapt the RIP rows** to your work — replace
"Operator N" with the actual operator name you analysed (one row per operator), and add or
remove rows to match the number of operators / group members.

| Sub-task / Item | Shakil | Saimon | Tawfiq |
|-----------------|:--------:|:--------:|:--------:|
| Mutation tool selection | × | × | × |
| Mutation operator analysis | × | × | × |
| RIP analysis — CompareIs | | × | |
| RIP analysis — Compare | × | | |
| RIP analysis — BinOp | | | × |
| Uppaal automaton | × | × | × |
| Formal requirements & queries | × | × | × |
| Expression mutation in model | × | × | × |
| Transition rerouting | × | × | × |
