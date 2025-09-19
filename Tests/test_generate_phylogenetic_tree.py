from pathlib import Path
import pytest
from dogbreed.phylogenetic_tree import generate_phylogenetic_tree


def test_generate_phylogenetic_tree_creates_files(tmp_path: Path):
    fasta_path = tmp_path / "alignment.fa"
    outdir = tmp_path

    # Dummy FASTA with 3 sequences
    fasta_path.write_text(
        ">A\nAAAA\n>B\nCCCC\n>C\nGGGG\n", encoding="utf-8"
    )

    output_files = generate_phylogenetic_tree(fasta_path, outdir, "tree.nwk", "tree.png")

    # Should return Newick + PNG
    assert isinstance(output_files, list)
    assert len(output_files) == 2

    nwk_file, png_file = output_files

    # Both files should exist
    assert Path(nwk_file).exists()
    assert Path(png_file).exists()

    # Newick file should contain a tree-like structure with parentheses
    nwk_content = Path(nwk_file).read_text().strip()
    assert "(" in nwk_content and ")" in nwk_content

    # PNG file should not be empty
    assert Path(png_file).stat().st_size > 0
