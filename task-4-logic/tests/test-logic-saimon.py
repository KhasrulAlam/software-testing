# Method: int_or_none from youtube_dl/utils.py
# Phase 04 - Logic Coverage, contributed by Saimon
#
# int_or_none has only single-clause predicates, so flat Active / Inactive
# Clause Coverage would collapse into plain predicate coverage. Instead we use
# the 2-level nested structure the method was selected for:
#
#     if get_attr:            # line 3874   clause A = bool(get_attr)
#         if v is not None:   # line 3875   clause B = (v is not None)
#             v = getattr(v, get_attr, None)   # line 3876
#
# Reaching line 3876 requires the compound predicate (A and B). We apply the
# logic criteria to that induced compound. Under short-circuit AND, a clause is
# only "inactive" when the other clause is False, which forces the predicate
# False; so an inactive clause with a True predicate is infeasible here. That is
# how Inactive Clause Coverage differs for this nesting versus a flat predicate.
#
# Criteria selected:
#   Group 1: Combinatorial Coverage (CoC)        - all 4 rows of (A, B)
#   Group 2: Correlated Active Clause Coverage (CACC)
#   Group 3: General Inactive Clause Coverage (GICC)

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'youtube-dl'))

from types import SimpleNamespace
from youtube_dl.utils import int_or_none


# LC1 - compound row A=T, B=T.
# get_attr is truthy and v is not None, so the nest is fully entered and
# getattr pulls '42' off the object, which converts to 42.
# Covers branches (3874->3875) and (3875->3876).
# Criteria: CoC (row TT); CACC (A-deciding pair with LC3, B-deciding pair with LC2).
def test_lc1_get_attr_true_value_not_none():
    obj = SimpleNamespace(count='42')
    assert int_or_none(obj, get_attr='count') == 42


# LC2 - compound row A=T, B=F.
# get_attr is truthy but v is None, so the inner if is False and getattr is
# skipped; v stays None and the (None, '') guard returns the default.
# Covers branches (3874->3875) and (3875->3877).
# Criteria: CoC (row TF); CACC (B is the deciding clause vs LC1);
#           GICC (clause A inactive, A true, predicate false).
def test_lc2_get_attr_true_value_none():
    assert int_or_none(None, get_attr='count') is None


# LC3 - compound row A=F, B=T.
# get_attr is falsy so the nest is skipped entirely; v is the string '42',
# which is not None and converts to 42.
# Covers the outer-if False path (3874->3877).
# Criteria: CoC (row FT); CACC (A is the deciding clause vs LC1);
#           GICC (clause B inactive, B true, predicate false).
def test_lc3_get_attr_false_value_not_none():
    assert int_or_none('42') == 42


# LC4 - compound row A=F, B=F.
# get_attr is falsy and v is None; the nest is skipped and the guard returns
# the default.
# Criteria: CoC (row FF);
#           GICC (clause A inactive with A false; clause B inactive with B false).
def test_lc4_get_attr_false_value_none():
    assert int_or_none(None) is None