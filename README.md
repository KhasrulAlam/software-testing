# Software Testing Project

**Software Testing** — Summer Semester 2026  
Hamburg University of Technology (TUHH)  
**Instructors:** Sibylle Schupp, Daniel Rashedi

This project explores a range of software testing techniques by applying them to a real-world open-source project rather than simplified examples. Our target system is **youtube-dl**, where we designed comprehensive test suites for a collection of helper functions in `youtube_dl/utils.py`.

The project was completed as a group assignment during the Software Testing course and is mirrored here as a personal copy of our work.

---

## Contributors

- **S M Khasrul Alam Shakil**
- **Saimon Chowdhury Fahim**
- **Md Tawfiq Bashar**

---

# Project Overview

The project is divided into five phases, each focusing on a different software testing technique. Applying all techniques to the same set of methods allowed us to compare their effectiveness in uncovering different classes of defects.

### Phase 1 — Random Testing

Using the **Hypothesis** property-based testing framework, we generated large numbers of random inputs and verified that expected properties always held. This approach is particularly effective at discovering unexpected edge cases.

### Phase 2 — Input Space Partitioning

For each method, we partitioned the input domain into equivalence classes and selected representative test cases from each partition. This technique provides broad input coverage with a relatively small number of tests.

### Phase 3 — Graph Coverage

Each method was analysed as a control-flow graph, and test cases were designed to achieve statement and branch coverage by exercising every executable path.

### Phase 4 — Logic Coverage

We analysed the Boolean predicates within each method and created test cases that exercised the individual logical conditions rather than only the overall outcomes.

### Phase 5 — Syntax Coverage

Mutation testing was performed using **mutatest**, introducing small code changes to evaluate the fault-detection capability of the test suites. Additionally, the `urshift` function was formally modelled in **Uppaal** and verified against a set of correctness properties.

Each contributor applied all five techniques to their assigned methods, making the work divided by functionality rather than by project phase.

---

# System Under Test

**Repository:** https://github.com/ytdl-org/youtube-dl

The project focuses on testing a collection of utility functions implemented in `youtube_dl/utils.py`.

---

# Method Assignments

Each contributor was responsible for the complete testing process (all five phases) for their assigned methods.

| Contributor | Assigned Methods |
|-------------|------------------|
| **Shakil** | `sanitize_filename`, `remove_start`, `remove_end`, `strip_or_none` |
| **Saimon** | `int_or_none`, `float_or_none`, `str_to_int`, `parse_count` |
| **Tawfiq** | `parse_duration`, `month_by_name`, `limit_length`, `parse_filesize` |

---

# Repository Structure

```text
software-testing/
├── task-1-random/tests/      # Phase 1: Random Testing (Hypothesis)
├── task-2-isp/tests/         # Phase 2: Input Space Partitioning
├── task-3-graph/tests/       # Phase 3: Graph Coverage
├── task-4-logic/tests/       # Phase 4: Logic Coverage
├── task-5-syntax/            # Phase 5: Mutation Testing & Uppaal
├── report-submission-files/  # Reports, screenshots, and submission documents
├── environment.yml           # Conda environment
└── .gitignore
```

Each `task-*/tests/` directory contains one Python test file per contributor (e.g., `test-random-shakil.py`, `test-logic-saimon.py`).

Since the filenames contain hyphens, they are **not automatically discovered by pytest** and must be specified explicitly on the command line.

---

# About the System Under Test

The **youtube-dl** source code is **not included** in this repository, as it is maintained independently. Keeping it separate ensures that this repository contains only our own testing artifacts and documentation.

Clone youtube-dl into the project root before running the tests:

```bash
git clone https://github.com/ytdl-org/youtube-dl.git
```

### Source Version

The project documentation references specific line numbers in `youtube_dl/utils.py`. Since the upstream repository continues to evolve, these references may not match the latest version.

For complete reproducibility, use the youtube-dl revision that was current during **Summer Semester 2026** rather than the latest release.

### Python Versions

Two slightly different environments were used during development.

| Contributor | Python | Statements |
|------------|:------:|----------:|
| Saimon | 3.10 | 2456 |
| Shakil & Tawfiq | 3.9 | 2453 |

This difference only affects coverage statistics and was accepted for the course. Each contributor's reported results remain internally consistent.

---

# Environment Setup

```bash
conda env create -f environment.yml
conda activate youtube-dl-test
```

If package installation fails inside the environment, prefer

```bash
conda install -c conda-forge <package>
```

or

```bash
python -m pip install <package>
```

---

# Running the Test Suite

Execute all commands from inside the cloned **youtube-dl** directory.

```bash
cd youtube-dl

pytest \
../task-1-random/tests/test-random-shakil.py \
../task-1-random/tests/test-random-saimon.py \
../task-1-random/tests/test-random-tawfiq.py \
../task-2-isp/tests/test-isp-shakil.py \
../task-2-isp/tests/test-isp-saimon.py \
../task-2-isp/tests/test-isp-tawfiq.py \
../task-3-graph/tests/test-graph-shakil.py \
../task-3-graph/tests/test-graph-saimon.py \
../task-3-graph/tests/test-graph-tawfiq.py \
../task-4-logic/tests/test-logic-shakil.py \
../task-4-logic/tests/test-logic-saimon.py \
../task-4-logic/tests/test-logic-tawfiq.py \
--cov=youtube_dl.utils \
--cov-branch
```

> **Note:** The original youtube-dl test suite (`youtube-dl/test/`) is intentionally excluded. It depends on network resources, contains more than 1,500 failing offline tests, and is outside the scope of this project.

---

# Project Summary

| Phase | Technique | Status |
|-------|-----------|:------:|
| 1 | Random Testing (Hypothesis) | ✅ |
| 2 | Input Space Partitioning | ✅ |
| 3 | Graph Coverage | ✅ |
| 4 | Logic Coverage | ✅ |
| 5 | Mutation Testing (`mutatest`) & Formal Verification (Uppaal) | ✅ |

The documentation for each phase—including reports, equivalence class analyses, RIP analyses, screenshots, and submission materials—is available in the `report-submission-files/` directory.

---

# Known Issues

- Use Unicode escape sequences (e.g., `\u00e9`) instead of literal non-ASCII characters to avoid Windows (`cp1252`) encoding issues.
- Hyphenated filenames are not automatically discovered by `pytest`; always specify test files explicitly.
- Generated coverage files (`coverage.json`, `.coverage`, `htmlcov/`) are excluded from version control.
- The cloned `youtube-dl/` directory is git-ignored because it is an external dependency.
- Running the original youtube-dl test suite may generate temporary media files (e.g., `test_*.mp4`, `test_*.info.json`). These files are unrelated to this project and should not be committed.
