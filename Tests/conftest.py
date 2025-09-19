import pytest
from pathlib import Path


@pytest.fixture
def tmp_fasta(tmp_path: Path) -> Path:
    fasta = tmp_path / "seqs.fa"
    fasta.write_text(
        ">id1\nACGTACGTAGCT\n>id2\nACGTACGTAGCT\n",
        encoding="utf-8"
    )
    return fasta


@pytest.fixture
def empty_fasta(tmp_path: Path) -> Path:
    """Empty FASTA file."""
    fasta = tmp_path / "empty.fa"
    fasta.write_text("", encoding="utf-8")
    return fasta


@pytest.fixture
def bad_fasta(tmp_path: Path) -> Path:
    """Malformed FASTA file (missing > headers)."""
    fasta = tmp_path / "bad.fa"
    fasta.write_text("this is not fasta format", encoding="utf-8")
    return fasta


@pytest.fixture
def tmp_csv(tmp_path: Path) -> Path:
    """Temporary CSV mapping file with two breeds."""
    csv_file = tmp_path / "breed_mapping.csv"
    csv_file.write_text(
        "accession_id,breed\nid1,Labrador\nid2,Poodle\n",
        encoding="utf-8"
    )
    return csv_file


@pytest.fixture
def weird_csv(tmp_path: Path) -> Path:
    """Malformed CSV missing headers."""
    csv_file = tmp_path / "weird.csv"
    csv_file.write_text("not_a_header,something\nxxx,yyy\n", encoding="utf-8")
    return csv_file
