import sys, os
ROOT = os.path.abspath(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "SRC")


import warnings
from Bio import BiopythonDeprecationWarning
warnings.filterwarnings("ignore", category=BiopythonDeprecationWarning)
from pathlib import Path
import pytest
import csv

# --- FASTA fixtures ---
@pytest.fixture
def tmp_fasta(tmp_path: Path) -> Path:
    p = tmp_path / "test.fa"
    p.write_text(
        ">seq1\nACGTACGTACGT\n"
        ">seq2\nACGTACCTACGT\n"
    )
    return p

@pytest.fixture
def empty_fasta(tmp_path: Path) -> Path:
    p = tmp_path / "empty.fa"
    p.write_text("")
    return p

@pytest.fixture
def bad_fasta(tmp_path: Path) -> Path:
    p = tmp_path / "bad.fa"
    p.write_text("seq1\nNOHEADER\n>seq2\nACGT")
    return p

# --- CSV fixtures ---
@pytest.fixture
def tmp_csv(tmp_path: Path) -> Path:
    rows = [
        {"accession_id": "id1", "breed": "Labrador Retriever"},
        {"accession_id": "id2", "breed": "German Shepherd"},
    ]
    p = tmp_path / "breed_mapping.csv"
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["accession_id", "breed"])
        w.writeheader(); w.writerows(rows)
    return p

@pytest.fixture
def weird_csv(tmp_path: Path) -> Path:
    p = tmp_path / "weird.csv"
    p.write_text("accession_id,breed,extra\nid1,Labrador,foo\n,NoID,bar\n")
    return p
