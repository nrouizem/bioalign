# ADR 0001: Linear gaps in v0

## Context
Linear gap penalties (constant penalty scaled by length) are the simplest to implement and align with standard classroom examples. However, in biological reality, gap opening is costlier than gap extension. Affine penalties (`A + B*(L-1)`) are widely used in practice and considered industry standard.

## Decision
For v0, adopt linear gap penalties for simplicity and clarity. The implementation will include a `GapScheme` abstraction so that affine gaps can be introduced later without rewriting the DP recurrence logic.

## Consequences
- ✅ Simpler initial implementation.
- ✅ Aligns with course learning goals and allows me to focus on DP fundamentals first.
- ✅ Clear upgrade path to affine via `GapScheme`.
- ❌ Not the industry standard; users may expect affine by default.
- ❌ Benchmark comparisons with Biopython will diverge on affine-sensitive cases.
