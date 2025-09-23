from typing import Iterator, Dict, Tuple

def iter_fasta(path: str) -> Iterator[Tuple[str, str]]:
    """
    Stream FASTA records.
    Returns an iterator of (header, sequence) tuples.
    Note: currently only returning IDs, not descriptions.

    Works on plain text or .gz files.
    """
    import gzip

    # Select the right open() based on file extension
    opener = gzip.open if str(path).endswith((".gz", ".gzip")) else open
    header, seq_lines = None, []

    with opener(path, "rt") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue                    # skip empty lines
            if line.startswith(">"):
                # We’ve hit the next record:
                if header is not None:
                    # Emit the previous record before overwriting header
                    yield header, "".join(seq_lines)
                header, seq_lines = line[1:].split()[0], []   # strip '>'
            else:
                seq_lines.append(line.upper())

        # End-of-file: flush the final record
        if header is not None:
            yield header, "".join(seq_lines)

def read_fasta(path: str) -> Dict[str, str]:
    """Load FASTA as a dict rather than an iterator."""
    return dict(iter_fasta(path))