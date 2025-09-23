# AI Usage Log (BioAlign)

> Reflective log of where and how AI assisted. Entries are grouped by file, newest first.

## template.py

#### 2025-09-16
- **AI role:** plan|scaffold|refactor|review
- **Prompt Summary:** 
- **Accepted:** 
- **Rejected:** 
- **Verification:** 
- **Learning impact:** 


## bioalign/core/scoring.py

#### 2025-09-16
- **AI role:** plan
- **Prompt Summary:** "Describe how a scoring function might be implemented in such a project."
- **Accepted:** Fully
- **Rejected:** None
- **Verification:** tests pass
- **Learning impact:** Learned about the `Callable` type; learned that, because of the match/mismatch params, it makes most sense to return a function rather than a direct score.

## bioalign/core/types.py

#### 2025-09-16
- **AI role:** plan
- **Prompt Summary:** "Describe how the special types might be implemented."
- **Accepted:** Fully
- **Rejected:** None
- **Verification:** tests pass
- **Learning impact:** Learned about the `dataclass` schema.

## bioalign/tests/unit

#### 2025-09-23
- **AI role:** plan
- **Prompt Summary:** "Generate small tests for global, semi-global, and local alignments of two sequences, as well as FASTA parsing with tmp paths."
- **Accepted:** Some correct tests; also modified some incorrect tests
- **Rejected:** Incorrect tests
- **Verification:** tests pass; checked tests manually
- **Learning impact:** This was more about generating a starting test suite; I had to go through the tests by hand because some weren't correct, particularly semi-global tests.

## proposal.md

#### 2025-09-16
- **AI role:** plan
- **Prompt Summary:** "What might the {testing, performance, profiling, etc.} look like? Suggest several options."
- **Accepted:** general ideas that are in line with my objectives.
- **Rejected:** suggestions that were not apt for v0 or not in line with my objectives
- **Verification:** N/A
- **Learning impact:** Learned simple structures/patterns for core SWE concepts such as testing and profiling.

#### 2025-09-16
- **AI role:** plan, review
- **Prompt Summary:** "Review this proposal for clarity and suggest anything I might be missing."
- **Accepted:** general proposal structure, wording polish
- **Rejected:** various suggestions that didn't align with my goals
- **Verification:** N/A
- **Learning impact:** Learned how to structure a basic SWE project proposal.

## pyproject.toml

#### 2025-09-16
- **AI role:** review
- **Prompt Summary:** "Review pyproject.toml and suggest any changes for it to be in line with the current state of the project."
- **Accepted:** most suggestions
- **Rejected:** optional/unnecessary suggestions (such as a v1+ change)
- **Verification:** tests pass
- **Learning impact:** Not much; got to see what a small, structured pyproject.toml file looks like
