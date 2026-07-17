# Software Testing Project — Group 20

Software Testing, Summer 2026, TUHH (Sibylle Schupp / Daniel Rashedi).

**System under test:** [youtube-dl](https://github.com/ytdl-org/youtube-dl).

This repository contains our multi-phase testing suite for a set of helper functions in youtube-dl's `utils.py`. It was originally developed on TUHH GitLab as a group project and is mirrored here as a personal copy of the work.

**Members:**
- S M Khasrul Alam Shakil
- Saimon Chowdhury Fahim
- Md Tawfiq Bashar

## Method assignments

Each member owns their methods end-to-end across all phases (own tests, own commits):

| Member | Methods |
|---|---|
| Shakil | `sanitize_filename`, `remove_start`, `remove_end`, `strip_or_none` |
| Saimon | `int_or_none`, `float_or_none`, `str_to_int`, `parse_count` |
| Tawfiq | `parse_duration`, `month_by_name`, `limit_length`, `parse_filesize` |

## Repository structure

```
software-testing/
  task-1-random/tests/      Phase 1: Random Testing (Hypothesis)
  task-2-isp/tests/         Phase 2: Input Space Partitioning
  task-3-graph/tests/       Phase 3: Graph Coverage
  task-4-logic/tests/       Phase 4: Logic Coverage
  task-5-syntax/            Phase 5: Syntax Coverage (mutation testing + Uppaal model)
  report-submission-files/  Phase write-ups (.md), screenshots, task PDFs
  environment.yml           Conda environment definition
  .gitignore
```

Each `task-N-*/tests/` folder holds one Python test file per member, e.g. `test-random-shakil.py`, `test-isp-saimon.py`, `test-graph-tawfiq.py`, `test-logic-shakil.py`. Filenames use hyphens, so they must be listed explicitly on the `pytest` command line rather than relying on directory auto-discovery.

### About the system under test (`youtube-dl/`)

The youtube-dl source is **not included** in this repository. It is a separate open-source project, and keeping our repo focused on our own work (tests and documentation) keeps it clean and clearly attributable.

To run the tests, clone youtube-dl into the project root so the folder layout matches what the commands below expect:

```
git clone https://github.com/ytdl-org/youtube-dl.git
```

A note on line numbers: our phase documentation (Tasks 3, 4, 5) references specific line numbers in `youtube_dl/utils.py`. Because upstream youtube-dl changes over time, a fresh clone may not line up exactly with those references. If you need the exact source version we tested against, check out the commit of youtube-dl that was current during Summer 2026 rather than the latest `master`.

Two Python version / statement-count baselines were in use across the group:
- Saimon: Python 3.10, 2456 statements
- Shakil and Tawfiq: Python 3.9, 2453 statements

This is a known, accepted discrepancy; each member's coverage tables are internally consistent within their own environment.

## Environment setup

```
conda env create -f environment.yml
conda activate youtube-dl-test
```

If `pip` misbehaves inside the conda environment, prefer:
```
conda install -c conda-forge <package>
```
or
```
python -m pip install <package>
```

## Running the test suite

All commands below are run from inside the `youtube-dl/` folder (which you cloned in the step above), so that `--cov=youtube_dl.utils` resolves correctly.

```
cd youtube-dl
pytest ../task-1-random/tests/test-random-shakil.py ../task-1-random/tests/test-random-saimon.py ../task-1-random/tests/test-random-tawfiq.py ../task-2-isp/tests/test-isp-shakil.py ../task-2-isp/tests/test-isp-saimon.py ../task-2-isp/tests/test-isp-tawfiq.py ../task-3-graph/tests/test-graph-shakil.py ../task-3-graph/tests/test-graph-saimon.py ../task-3-graph/tests/test-graph-tawfiq.py ../task-4-logic/tests/test-logic-shakil.py ../task-4-logic/tests/test-logic-saimon.py ../task-4-logic/tests/test-logic-tawfiq.py --cov=youtube_dl.utils --cov-branch
```

Note: youtube-dl's own test suite (under `youtube-dl/test/`) is intentionally **excluded** from all commands above. It is network-dependent, has 1500+ offline failures, and takes hours to run; it is not part of this project's deliverables.

## Phase summary

| Phase | Technique | Status |
|---|---|---|
| 1 | Random Testing (Hypothesis) | Done |
| 2 | Input Space Partitioning | Done |
| 3 | Graph Coverage | Done |
| 4 | Logic Coverage | Done |
| 5 | Syntax Coverage (mutation testing with `mutatest`, formal modelling in Uppaal) | Done |

Each phase's write-up (`.md` documentation, per-phase equivalence class tables, RIP analysis, etc.) lives in `report-submission-files/`. For the course, these were also submitted via StudIP alongside the corresponding `.zip`, per the submission instructions.

## Known gotchas

- Non-ASCII characters in test files can silently fail on Windows (cp1252 encoding). Use Unicode escapes (`\u00e9`) instead of literal characters.
- Hyphenated test filenames (`test-graph-shakil.py`) are not auto-discovered by pytest; always pass explicit file paths.
- `coverage.json`, `.coverage`, and `htmlcov/` are git-ignored to avoid cross-machine conflicts.
- The `youtube-dl/` folder is git-ignored here, since it is an external dependency you clone separately rather than part of this project's source.
- youtube-dl's own test suite writes sample media files (e.g. `test_*.mp4`, `test_*.info.json`) to whatever directory it's run from if invoked directly; these are not part of this project and should not be committed.
