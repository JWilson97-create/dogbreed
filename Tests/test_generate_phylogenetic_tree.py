from pathlib import Path
import os, sys, importlib
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

mod = importlib.import_module("Main.generate_phylogenetic_tree") # dynamic import
ENTRY = getattr(mod, "main", None) or getattr(mod, "generate_phylogenetic_tree", None)  # support both names


@pytest.mark.skipif(ENTRY is None, reason="generate_phylogenetic_tree entry function not found") # skip if not found


def test_generate_tree_writes_outputs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Run the ENTRY function and check that tree files are written."""
    # Set up temp data and results dirs
    data = tmp_path / "data"
    results = tmp_path / "Results"
    data.mkdir()
    results.mkdir()

    # Tiny alignment file if your script expects one
    aln = results / "alignment_input.fasta" # or dog_sequences*.fa
    aln.write_text(">A\nANACGT\n>B\nNACGAA\n>C\nTTTTTT\n", encoding="utf-8") # write a tiny FASTA

    monkeypatch.setenv("DOG_DATA_DIR", str(data)) # set env vars for dirs
    monkeypatch.setenv("DOG_RESULTS_DIR", str(results)) # set env vars for dirs 

    # Support both call styles
    try:
        ENTRY()
    except TypeError:
        ENTRY(str(data), str(results)) # call with args if needed

    out = list(results.glob("*.png")) + list(results.glob("*.nwk")) + list(results.glob("*.tree*"))
    assert out, "No tree outputs written"
