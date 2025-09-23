# BioAlign

*A lightweight Python package for pairwise sequence alignment.*

---

## Overview
BioAlign is a learning-in-public project where I re-implement core bioinformatics alignment algorithms (Needleman–Wunsch, Smith–Waterman) while practicing software engineering discipline.  
The repo includes a detailed [project proposal](proposal.md) and an [AI usage log](AI_USAGE.md) documenting how AI tools assisted in development.

**Goals for v0**
- Correct implementations of NW and SW
- Clean functional API + thin CLI
- Rigorous test suite with Biopython parity
- Continuous integration setup
- Public documentation and concept notes

---

## Current Status
This repository currently contains:
- `proposal.md` — project plan and design document
- `AI_USAGE.md` — log of AI involvement
- Initial package skeleton (`bioalign/`), not yet functional

---

## Roadmap
- [x] Implement NW + SW in `bioalign/core/`
- [ ] Add CLI (`bioalign/cli/`)
- [ ] Parity tests vs Biopython
- [ ] CI workflow (lint, type, test)
- [ ] Publish first demo on [notes.nrouizem.com](https://notes.nrouizem.com)

See the [proposal](proposal.md) for details.

---

## AI-Conscious Development
This project is developed with explicit attention to AI usage:
- Algorithms and logic are first implemented by hand
- AI is used for polish, scaffolding, and review
- All AI involvement is documented in [AI_USAGE.md](AI_USAGE.md)

---

## License
MIT License (intended; will be confirmed before v0 release).
