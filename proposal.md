# Proposal for BioAlign

## Outline

1. Introduction/Objective
2. Learning Objectives
3. AI-Conscious Development 
4. Scope of v0
5. Future Directions
6. Software Design
7. Process & Gates
8. Portfolio Polish


## Introduction/Objective

1. Motivation: I am currently taking two bioinformatics classes and want to deepen my understanding by implementing some of the algorithms I've been learning. At the same time, I want to strengthen my software engineering intuition and skills, hence making this a full project with a proposal, an API, tests + CI, and documentation. By keeping the project public, I also aim to make it accessible for classmates (as a reference) and potential employers (as part of my portfolio).
2. Objectives:
    - Correct re-implementation of Needleman-Wunsch and Smith-Waterman (at least for v0; possibly more later)
    - Clean, usable API
    - Thorough test suite, including parity tests and property tests, plus performance comparisons with Biopython
    - Basic CLI
    - AI-consciousness: explicitly document and reflect on where AI is used in development
    - Learning objectives: track and reflect on the SWE and bioinformatics skills I want to build (see below)
3. Constraints: I’m taking two bioinformatics courses, applying to jobs, and working on other projects concurrently, so time is constrained. I'm also prioritizing learning and clarity/correctness over performance, so I'm not expecting anything to match Biopython in speed.
4. Intended audience: this is mostly for myself for now; my goal is to learn these algorithms well and improve my SWE understanding. I'm also keeping in mind anyone who might be interested in seeing some of my work.
5. Success criteria (v0):
    - Parity with Biopython on test cases
    - Green CI (tests, lint, type checks)
    - At least one polished concept note/demo on my website


## Learning Objectives

- Deepen algorithmic understanding
    - Implement NW and SW (global, semi-global, local)
    - Understand scoring schemes, gap penalties, and traceback mechanics
- Strengthen software engineering skills
    - Practice designing modular architecture
    - Learn to write testable code with reproducibility in mind
    - Develop CI/CD understanding with modern Python tooling
- Learn how to balance AI assistance
    - Document all AI use
    - Implement algorithms myself first to ensure understanding
    - Use AI for polishing, scaffolding, or boilerplate/repetitive code
- Develop documentation + communication skills
    - Write clear docstrings + README instructions for reproducibility
    - Publish concept notes and short demos on my website that explain the algorithms in plain language
- Learn in public
    - All work is publicly visible, including (and especially) mistakes and how I addressed them, adjusted objectives, etc.


## AI-Conscious Development

- Philosophy
    - Given the revolutionary nature of AI, it is essential to learn to leverage it, while recognizing that it is no more than a tool, however powerful. I therefore want to be intentional about how I use it, particularly given that this is a learning project.
    - Key: I want to understand the algorithms myself; I've used AI to help me understand them, but I will implement them myself
    - AI is incredibly useful for speed-up and polish, but my understanding and learning comes first
- First pass myself, second pass assisted
    - Implement algorithms + logic myself
    - Once a working version exists (or I'm sufficiently stuck), allow AI to review, polish, simplify, etc.
- Where AI is permitted
    - Scaffolding boilerplate (CLI, fleshing out docstrings, config files, polishing README and other text such as this doc)
    - Generating repetitive test cases
    - Suggesting cleanups/refactors
    - Code review
    - Answering specific questions I have about best practices in SWE, feedback on project structure and modularity, etc. Basically, anything that is in service of me maximizing my learning through this project.
- Where AI is limited
    - Algorithm derivations (DP recurrences, scoring rules)
    - First implementation of alignment logic
    - Interpreting eval metrics
- Reflection & documentation
    - Document every meaningful use of AI (what it did, why I accepted/rejected it) in `AI_USAGE.md`
    - At the end, reflect on how AI impacted my learning: when did it save time vs. when did it obscure understanding or enable laziness?


## Scope of v0

- Implement Needleman–Wunsch and Smith–Waterman (linear gaps)
- Simple FASTA parsing
- Achieve functional parity with Biopython on representative test cases, with explicit notes where classroom conventions differ
- Provide a clean API and a minimal CLI for usability
- Develop a thorough test suite:
    - Functional tests (unit, property, parity with Biopython)
    - Performance smoke tests (e.g., 200×200 inputs)
- Include basic evaluation metrics: identity %, gap counts, simple calibration plot
- Set up CI (tests, lint, type checks, coverage threshold)
- Provide initial documentation: README + at least one concept note/demo published on my website


## Future Directions

**Likely extensions**
- Affine gap penalties (Gotoh’s algorithm)
- Expanded evaluation metrics: statistical significance tests, visualization (dot plots, alignment viewers)

**Exploratory projects**
- Homology search: basic/mini implementations inspired by BLAST and FASTA
- GPU acceleration: prototype banded or affine-gap alignment on GPU (JAX or CuPy)
- FastAPI service: expose alignment as a REST endpoint, practice deployment/observability


## Software Design

**1. Context & Constraints**
- Problem statement: A lightweight pairwise alignment toolkit focusing on correctness, clarity, and software design.
- Non-goals (v0): GPU acceleration, affine gaps, homology search

**2. Architecture Overview**
- Style: A modular monolith with hexagonal boundaries and a functional core with a thin OO shell: core DP algorithms are pure functions; I/O (FASTA/CLI/REST) are adapters; the package remains a single deployable unit

**3. Key Design Decisions (ADRs)**
- ADR-001: Linear gaps only in v0; affine postponed.

**4. Module Layout**
- `bioalign/core/`
    - `dp.py` - DP fill + recurrence
    - `init.py` - Boundary conditions for global / local / semi-global modes (first row/col rules and any mode-specific penalties)
    - `traceback.py` - Path reconstruction with a documented tie-break policy (e.g., diag > up > left); returns aligned strings and CIGAR
    - `scoring.py` - Scoring primitives: simple match/mismatch now; hook for substitution matrices later
    - `types.py` - Small data types: `Mode`, `GapScheme`, `FreeEnds`, `AlignResult`
- `bioalign/io/`
    - `formats.py` - Formatting & conversion helpers (pretty alignment lines, CIGAR)
    - `fasta.py` - Minimal FASTA read/write utilities
- `bioalign/eval/`
    - `metrics.py` - Identity %, gap counts/opens/extends, basic "alignment quality" helpers; small calibration utilities
    - `bench.py` - Perf smoke probes (cells/sec, rough memory), not microbenchmarks
- `bioalign/cli/`
    - `main.py` — Typer commands (`align`, `score-batch`, `profile`) that map 1:1 to the functional API
- `tests/`
    - `unit/` — Per-module granularity (dp, init, traceback, scoring, formats, metrics)
    - `parity/` — Biopython parity suite
    - `property/` — Symmetry, monotonicity, edge cases (empty strings)

**5. Data Structures & Types**
- `Mode = Literal["global","local","semi-global"]`
- `GapScheme(open, extend)`
- `AlignResult(score, S_aln, T_aln, …)`

**6. Algorithms (v0)**
- **a) Problem framing & notation**
    - **Inputs**: two sequences `S` (length `n`), `T` (length `m`); alphabet assumed to be uppercase DNA/protein (validate/normalize).
    - **Scoring**: `delta(x,y)` = match/mismatch (linear gaps in v0). `gap.open == gap.extend == g` (integer).
    - **Outputs**: `(S_aln, T_aln, score)` plus optional CIGAR.
    - **Matrix** convention: DP matrix `M` has shape `(m+1)×(n+1)`; row `i` indexes `T[:i]`, column `j` indexes `S[:j]`.

- **b) Initialization (mode-specific boundary conditions)**
    - **Global (NW)**:
        - `M[0, j] = j * g`, `M[i, 0] = i * g`.
        - Invariant: If either string empty, score is linear penalties for remaining length.
    - **Local (SW)**:
        - First row/col zeros: `M[0, j] = M[i, 0] = 0`.
        - Invariant: Scores never go below 0.
    - **Semi-global**:
        - Model free prefixes/suffixes via zero-penalty boundary on chosen edges (explicit flags `FreeEnds`). 
        - Clarify which edges are free vs penalized (`begin_S`, `begin_T`, `end_S`, `end_T`) and encode that in row/col init (not post-hoc padding).
        - Decision: Use init/transition rules, not output padding, to realize free ends.

- **c) Recurrence (linear gaps)**
    - **Transition candidates at `(i,j)` (for `i>0`, `j>0`)**:
        - `diag = M[i-1, j-1] + delta(S[j-1], T[i-1])`
        - `up = M[i-1, j] + g`
        - `left = M[i, j-1] + g`
    - **Cell value**:
        - Global/Semi-global: `M[i,j] = max(diag, up, left)`
        - Local: `M[i,j] = max(diag, up, left, 0)`
    - **Semi-global end-penalty tweaks**: if an edge is "free at end", ensure the corresponding transition into the last row/col applies zero penalty (document precisely which moves are affected).

- **d) Traceback policy (determinism)**
    - **Start cell**:
        - Global: `(m,n)`
        - Local: `argmax(M)`
        - Semi-global: best in last row/col per chosen free ends.
    - **Tie-break order (fixed)**: `diag > up > left`
    - **Stop condition**:
        - Global/Semi-global: when `(i==0 and j==0)` or when free-begin rules trigger stop.
        - Local: when `M[i,j] == 0`.
    - **Outputs**: aligned strings + CIGAR (M=match/mismatch, I=insertion to S, D=deletion from S).
    - **Edge cases**: zero-length inputs; all-gap paths; ambiguous ties—ensure reproducible choice.

- **e) Scoring function design**
    - **v0**: simple `delta(x,y)` (match/mismatch integers).
    - **Extensibility hook**: keep `delta` injectable (callable) so substitution matrices are a drop-in later.
    - **Validation**: alphabet check; unknown chars -> error.

- **f) Invariants / properties to test:**
    - Symmetry under sequence swap when `delta` and `g` are symmetric.
    - Monotonicity: making `g` more negative should not increase the optimal score.
    - Local mode: all `M[i,j] ≥ 0`.

**7. Config & API Surface**
- Configuration Model
    - Parameters passed explicitly via functional API or CLI flags.
    - Defaults are centralized and documented; no hidden globals.
    - Precedence: CLI > function args > config file (v1+) > defaults.

- Public API (v0)
    - **Functional API**: `align(S, T, mode, gap, free, delta, return_matrix, format)` → `AlignResult`.
    - **OO wrapper**: thin class around the functional API, no logic.
    - **Stability**: functional API + result object stable across v0.x releases.

- Parameters & Types
    - **Sequences**: strings (validated, uppercase).
    - **mode**: `global | local | semi-global`.
    - **gap**: integer (linear in v0; affine later).
    - **free**: four booleans (`begin_S`, `begin_T`, `end_S`, `end_T`), only valid in semi-global.
    - **delta**: callable or keyword for scoring scheme.
    - **return_matrix**: bool (default false; enables debug output).
    - **format**: `pretty | cigar | tsv | json`.

- Result Object
    - `score`: int
    - `S_aln`, `T_aln`: aligned strings (equal length)
    - `cigar`: optional string
    - `meta`: optional dict (mode, gap, free flags, etc.)
    - `matrix`: only if `return_matrix=True`

- CLI Commands
    - `align`: one-off alignment
    - `score-batch`: batch TSV/FASTA pairs
    - `profile`: simple performance probe

- CLI Common Flags
    - `--mode {global,local,semi-global}`
    - `--gap -2` (linear)
    - `--free-begin-S`, etc. (semi-global only)
    - `--matrix simple|BLOSUM62|path` (v1+)
    - `--format {pretty,cigar,tsv,json}`
    - `--return-matrix`
    - Input: `--S`, `--T`, or `--fasta`
    - Output: `--out results.tsv`

- Defaults
    - mode: `global`
    - gap: `-2`
    - matrix: `simple` (match=+1, mismatch=-1)
    - free-ends: all `false`
    - format: `pretty`
    - return_matrix: `false`

- Error Handling
    - Invalid combos (e.g. free-ends with non–semi-global) → `ValueError` with clear message.
    - Unknown characters: actionable error with index/char reported.


**8. Observability & Profiling**
- Philosophy
    - Keep observability light in v0: enough to diagnose correctness and basic performance regressions, without heavy logging.
    - Prioritize **determinism and reproducibility** over extensive metrics.

- Observability (v0)
    - **Verbose mode** (`--verbose`):
        - Echo chosen parameters (mode, gap, free-ends, scoring).
        - Report tie-break policy used in traceback.
    - **Logging**:
        - Default: silent except for errors.
        - Verbose: human-readable info-level logs.
        - No network logging; no telemetry.

- Profiling (v0)
    - **Profile command** (`bioalign profile`):
        - Reports DP matrix dimensions, total cells computed.
        - Cells/sec benchmark on synthetic inputs (e.g., 200×200).
        - Peak memory usage (rough estimate via Python `sys.getsizeof`).
    - **Perf guard test**:
        - Simple pytest mark for 200×200 run under a time threshold.
        - Not a microbenchmark; just regression prevention.

- Metrics Collected
    - Alignment score (always).
    - Cells computed (profile only).
    - Runtime (profile only).
    - Optional: gap count, match/mismatch breakdown (from `eval.metrics`).

- Future Directions
    - Add more detailed logging (trace-level step dumps) for teaching/debugging.
    - Structured logs (JSON) for automated evaluation.
    - Integration with profiling tools (cProfile, line_profiler).
    - Observability hooks for future FastAPI service (request logs, error tracking).


**9. Performance Considerations**
- Philosophy
    - **Correctness and clarity come first** in v0; performance is secondary.
    - Performance work should be limited to **preventing pathological slowdowns** and **catching regressions**.
- Baseline Expectations (v0)
    - Time complexity: O(n × m) for sequences of length n and m.
    - Space complexity: O(n × m) using a full DP matrix (`int32`).
    - Suitable for teaching and testing purposes on sequences up to ~1,000 bp.
- Guardrails
    - CI perf test: 200×200 alignment must complete under a fixed threshold (e.g., < 0.5s on standard hardware).
    - Avoid premature optimization; document slow cases instead of masking them.
- Implementation Practices
    - Use NumPy for matrix representation and arithmetic.
    - Avoid Python loops where vectorization is straightforward (but keep clarity).
    - Keep tie-break and traceback explicit, even if slightly slower, for readability.
- Future Directions
    - **Affine gaps**: introduce `M/I/D` matrices, more operations but same complexity class.
    - **Banded alignment**: reduce complexity to O(k × max(n,m)) where k is band width.
    - **Linear-space algorithms**: Hirschberg’s method to reduce memory use from O(n × m) to O(n + m).
    - **GPU acceleration**: prototype with JAX, CuPy, or PyTorch for large-scale performance.
    - **Parallelism**: explore block-level parallel fill, though not needed for v0 scale.

**10. Testing Strategy (summary)**

- Philosophy
    - Testing ensures correctness, reproducibility, and learning value.
    - Strategy balances unit coverage, property-based testing, and parity with Biopython.

- Unit Tests
    - Per-module tests (dp, init, traceback, scoring, formats, metrics).
    - Small hand-computed examples (2×2, 3×3 matrices) for init, recurrence, traceback.

- Parity Tests
    - Representative test cases checked against Biopython’s `PairwiseAligner`.
    - Explicit documentation of divergences (e.g., tie-break policy, semi-global conventions).

- Property Tests
    - **Symmetry**: swapping S and T gives consistent results.  
    - **Monotonicity**: stricter gap penalties should not yield higher scores.  
    - **Local alignment non-negativity**: all scores ≥ 0.  
    - **Round-trip**: CIGAR ↔ alignment strings consistency.

- Edge Cases
    - Empty sequences.  
    - All-gap alignments.  
    - Long homopolymers (e.g., "AAAAA" vs "AAA").  

- Performance Tests
    - Single smoke perf test: 200×200 matrix under a CI threshold.  
    - Not a microbenchmark—regression guard only.

- Coverage & CI
    - Aim for ~90% coverage on `core/*`.  
    - CI checks: lint, type, unit, parity, property, perf.  
    - Fail fast if critical invariants break.

- Future Directions
    - Fuzzing with random sequences to detect unexpected errors.  
    - More advanced property tests (e.g., alignment score ≥ all local substrings).  
    - Integration tests for CLI workflows (batch TSV/FASTA).


**11. Documentation Surfaces**
- Philosophy
    - Documentation is part of the learning process, not just polish.
    - Keep layers simple: API docs, usage docs, teaching notes.

- Surfaces (v0)
    1. **Docstrings**
        - Every public function/class has a concise docstring.
        - Follow NumPy-style format (Args, Returns, Raises).
        - Examples included for core API functions.

    2. **README.md**
        - High-level overview, installation, quickstart.
        - Minimal but polished, with alignment examples.

    3. **Concept Notes**
        - Separate `/docs/notes/` folder with blog-style explanations:
            - "How Needleman-Wunsch works"
            - "Global vs Local vs Semi-global"
            - "Gap penalties and biological intuition"
        - Published to personal site for learning in public.

    4. **Usage Guides**
        - `/docs/usage/` with short how-tos:
            - Running CLI commands.
            - Using functional API.
            - Comparing to Biopython.

    5. **Reference Docs**
        - Generated with Sphinx or mkdocs in v1+.
        - Not required for v0 but keep code docstring-ready.

- Future Directions
    - Auto-deploy docs to GitHub Pages.
    - Tutorial notebooks for teaching/demo purposes.
    - API reference site with versioned docs.

**12. Open Questions**

- What’s the most transparent way to expose semi-global free-end flags?
- Should FASTA parsing be in io/ or use an external lib?

## Process & Gates
- Development Process
    - **Iteration style**: short milestones, each producing a working increment (e.g., core DP, CLI, docs).  
    - **Version control**: main branch stable, feature branches for experiments.  
    - **Reviews**: self-reviews plus AI-assisted reviews logged in `AI_USAGE.md`.  
    - **Docs with code**: README, notes, and AI log updated continuously.

- Gates for v0
    - **Feature gate**: NW + SW implemented and callable from API/CLI.  
    - **Test gate**: ≥90% coverage on `bioalign/core`; Biopython parity suite green.  
    - **CI gate**: lint, type checks, and perf guard green.  
    - **Docs gate**: at least one concept note + one usage guide published.  
    - **Portfolio gate**: working demo posted on website.

- Learning Gates
    - Capture key lessons after each milestone (algorithms + SWE).  
    - Reflect on AI usage: when it accelerated vs when it hindered.  
    - Note SWE design intuitions gained (what you’d do differently).

- Exit Criteria (v0)
    - Core features correct, tested, documented.  
    - CI consistently green.  
    - Remaining work moved to Future Directions.  
    - Enough polish to showcase in portfolio.

## Portfolio Polish

- Philosophy
    - Project should not just work, but also present well to classmates and potential employers.  
    - Balance learning focus with presentation value.

- GitHub Repo
    - **README**: clear, concise, with alignment example and quickstart.  
    - **Badges**: CI status, coverage %.  
    - **Tags/Releases**: mark v0 release.  
    - **AI-consciousness**: link to `AI_USAGE.md` for transparency.  

- Documentation for Portfolio
    - At least one polished concept note published on personal website.  
    - Usage guide written with job-seeker audience in mind (shows clarity of communication).  
    - Cross-links: repo ↔ website ↔ concept notes.  

- Demos & Visuals
    - Example alignment screenshot in README.  
    - Optional: short asciinema or gif of CLI run.  
    - Plots of performance benchmarks (cells/sec vs input size).  

- Communication Surfaces
    - Blog-style posts: “Building BioAlign v0” or “Reimplementing NW/SW from scratch.”  
    - Share progress posts on LinkedIn/Twitter (learning in public).  

- Success Criteria (Portfolio)
    - Repo looks professional and maintained (CI green, docs present).  
    - Clear demo of functionality in README.  
    - Website shows both technical depth (notes) and communication ability.  
    - Evidence of reflection: AI-consciousness log visible and honest.  

- Future Directions
    - Add Jupyter notebook demos with visualizations.  
    - Publish a tutorial on using BioAlign for a real dataset.  
    - Prepare talk slides (meetup/conference style) from project content.  