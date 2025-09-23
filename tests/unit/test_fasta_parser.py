import textwrap
from types import GeneratorType
import pytest

from bioalign.io.fasta import iter_fasta, read_fasta


def write(tmp_path, name, content):
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def test_read_single_and_multi(tmp_path):
    p = write(
        tmp_path,
        "tiny.fasta",
        textwrap.dedent(
            """
            >seq0
            GTATC
            >seq1
            ATCCC
            """
        ).strip()
    )
    seqs = read_fasta(str(p))
    assert isinstance(seqs, dict)
    assert seqs["seq0"] == "GTATC"
    assert seqs["seq1"] == "ATCCC"
    assert len(seqs) == 2


def test_iter_basic_yields_pairs_and_exhausts(tmp_path):
    p = write(
        tmp_path,
        "tiny.fasta",
        ">seq0\nGTATC\n>seq1\nATCCC\n"
    )
    gen = iter_fasta(str(p))
    assert isinstance(gen, GeneratorType)
    assert next(gen) == ("seq0", "GTATC")
    assert next(gen) == ("seq1", "ATCCC")
    with pytest.raises(StopIteration):
        next(gen)


def test_wrapped_multiline_sequence_is_concatenated(tmp_path):
    p = write(
        tmp_path,
        "wrapped.fasta",
        textwrap.dedent(
            """
            >s description
            GTA
            TC
            G
            """
        ).strip()
    )
    # Iterator
    items = list(iter_fasta(str(p)))
    assert items == [("s", "GTATCG")]
    # Dict loader
    assert read_fasta(str(p)) == {"s": "GTATCG"}


def test_lowercase_is_normalized_to_uppercase(tmp_path):
    p = write(
        tmp_path,
        "mixed.fasta",
        ">id\nacgTn\n"
    )
    seqs = read_fasta(str(p))
    assert seqs["id"] == "ACGTN"


def test_ignores_blank_lines_and_trailing_spaces(tmp_path):
    p = write(
        tmp_path,
        "blanks.fasta",
        "\n>id   \n \n ACGT \n  \n"
    )
    assert read_fasta(str(p)) == {"id": "ACGT"}


def test_empty_file_yields_empty(tmp_path):
    p = write(tmp_path, "empty.fasta", "")
    assert read_fasta(str(p)) == {}
    assert list(iter_fasta(str(p))) == []


def test_header_with_no_sequence_emits_empty_sequence(tmp_path):
    p = write(tmp_path, "only_header.fasta", ">id\n")
    assert read_fasta(str(p)) == {"id": ""}


def test_no_final_newline_is_ok(tmp_path):
    p = write(tmp_path, "no_newline.fasta", ">id\nACGT")  # no trailing newline
    assert read_fasta(str(p)) == {"id": "ACGT"}


def test_iter_vs_read_roundtrip_equivalence(tmp_path):
    p = write(
        tmp_path,
        "multi.fasta",
        ">a\nAAA\n>bb\nCC\nC\n>c\nG\n"
    )
    as_iter = dict(iter_fasta(str(p)))
    as_read = read_fasta(str(p))
    assert as_iter == as_read == {"a": "AAA", "bb": "CCC", "c": "G"}

def test_multiseq_read_and_iter_with_wrapped_and_blanks(tmp_path):
    """
    Three records, including wrapped lines and blank lines between records.
    Verifies:
      - read_fasta returns all records with concatenated sequences
      - iter_fasta yields in file order and matches read_fasta
    """
    content = textwrap.dedent(
        """
        >seqA some description
        ACG
        T
        A

        >seqB
        g
        t
        A

        >seqC
        CC
        CC
        """
    ).strip() + "\n"
    p = tmp_path / "multi.fasta"
    p.write_text(content, encoding="utf-8")

    # read_fasta should normalize to uppercase and concatenate wrapped lines
    expected = {"seqA": "ACGTA", "seqB": "GTA", "seqC": "CCCC"}
    assert read_fasta(str(p)) == expected

    # iter_fasta should yield in file order
    gen = iter_fasta(str(p))
    assert isinstance(gen, GeneratorType)
    items = list(gen)
    assert items == [("seqA", "ACGTA"), ("seqB", "GTA"), ("seqC", "CCCC")]


def test_multiseq_many_programmatic_and_equivalence(tmp_path):
    """
    Ten records generated programmatically.
    Verifies:
      - read_fasta output equals dict(iter_fasta)
      - All records are present and sequences match
    """
    records = {f"id{i}": "A" * (i + 1) + "C" * i for i in range(10)}
    lines = []
    for k, v in records.items():
        # split into wrapped lines of width 3 to simulate typical FASTA wrapping
        wrapped = "\n".join(v[j:j+3] for j in range(0, len(v), 3))
        lines.append(f">{k}\n{wrapped}")
    content = "\n".join(lines) + "\n"

    p = tmp_path / "many.fasta"
    p.write_text(content, encoding="utf-8")

    by_dict = read_fasta(str(p))
    by_iter = dict(iter_fasta(str(p)))

    assert by_dict == records
    assert by_iter == records

def test_gzip_compressed(tmp_path):
    import gzip
    p = tmp_path / "tiny.fasta.gz"
    with gzip.open(p, "wt", encoding="utf-8") as fh:
        fh.write(">x\nac\n>y\ngt\n")
    assert read_fasta(str(p)) == {"x": "AC", "y": "GT"}
