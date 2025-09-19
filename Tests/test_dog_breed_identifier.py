from pathlib import Path
import pytest

from dogbreed.dog_breed_identifier import DogBreedIdentifier
from dogbreed.phylogenetic_tree import generate_phylogenetic_tree as generate_tree


def test_identifier_creates_results(tmp_path: Path):
    fasta_path = tmp_path / "dog_sequences.fa"
    mystery_path = tmp_path / "mystery.fa"
    out_dir = tmp_path / "results"
    out_dir.mkdir()

    # Dummy FASTA files
    fasta_path.write_text(">id1\nAAAA\n>id2\nCCCC\n")
    mystery_path.write_text(">mystery\nAAAA\n")

    identifier = DogBreedIdentifier(fasta_path, mystery_path, out_dir)
    results = identifier.identify()

    # Should return a non-empty list
    assert isinstance(results, list)
    assert len(results) > 0

    # Each result should be a tuple (id, score)
    best_id, best_score = results[0]
    assert isinstance(best_id, str)
    assert isinstance(best_score, float)

    # Since mystery matches id1 perfectly, id1 should be best match
    assert best_id == "id1"
    assert best_score == 100.0


def test_build_tree(tmp_path: Path):
    fasta_path = tmp_path / "dog_sequences.fa"
    mystery_path = tmp_path / "mystery.fa"
    out_dir = tmp_path / "results"
    out_dir.mkdir()

    # Dummy FASTA files
    fasta_path.write_text(">id1\nAAAA\n>id2\nCCCC\n")
    mystery_path.write_text(">mystery\nAAAA\n")

    identifier = DogBreedIdentifier(fasta_path, mystery_path, out_dir)
    output_files = identifier.build_tree()

    # Should return Newick + PNG paths
    assert isinstance(output_files, list)
    assert len(output_files) == 2
    for f in output_files:
        assert Path(f).exists()
