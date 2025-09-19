from pathlib import Path
import pytest
from dogbreed.generate_alignment_input import generate_alignment_input


def test_generate_alignment_input_creates_expected_files(tmp_path: Path):
    fasta_path = tmp_path / "dog_sequences.fa"
    map_path = tmp_path / "breed_mapping.csv"
    outdir = tmp_path

    # Dummy FASTA
    fasta_path.write_text(">id1\nAAAA\n>id2\nCCCC\n", encoding="utf-8")

    # Dummy mapping
    map_path.write_text("accession_id,breed\nid1,Labrador\nid2,Poodle\n", encoding="utf-8")

    # Run
    out_fasta = generate_alignment_input(fasta_path, map_path, outdir)

    assert Path(out_fasta).exists()
    contents = Path(out_fasta).read_text()

    # Breed names should replace IDs
    assert "Labrador" in contents
    assert "Poodle" in contents
    assert "id1" not in contents
    assert "id2" not in contents


def test_generate_alignment_input_with_missing_id(tmp_path: Path):
    fasta_path = tmp_path / "dog_sequences.fa"
    map_path = tmp_path / "breed_mapping.csv"
    outdir = tmp_path

    # FASTA with one missing from map
    fasta_path.write_text(">id1\nAAAA\n>id3\nTTTT\n", encoding="utf-8")

    # Mapping only includes id1
    map_path.write_text("accession_id,breed\nid1,Labrador\n", encoding="utf-8")

    out_fasta = generate_alignment_input(fasta_path, map_path, outdir)
    contents = Path(out_fasta).read_text()

    # id1 replaced with breed name
    assert "Labrador" in contents
    # id3 should still appear (no mapping found)
    assert "id3" in contents
