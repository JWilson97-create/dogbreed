from pathlib import Path
import os, sys, importlib
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

mod = importlib.import_module("Main.generate_alignment_input")
ENTRY = getattr(mod, "main", None) or getattr(mod, "generate_alignment_input", None)


@pytest.mark.skipif(ENTRY is None, reason="generate_alignment_input entry function not found")
def test_generate_alignment_input_writes_expected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Run the ENTRY function and check that alignment input files are written."""
    # Set up temp data and results dirs
    data = tmp_path / "data"
    results = tmp_path / "Results"
    data.mkdir()
    results.mkdir()

    # Minimal per-sequence FASTA files expected by your script
    (data / "AY656744.fasta").write_text(">AY656744.1 Springer\nACGTACGT\n", encoding="utf-8")
    (data / "CM023446.fasta").write_text(">CM023446.1 Golden\nACGTTTGT\n", encoding="utf-8")
    (data / "MW916023.fasta").write_text(">MW916023.1 Labrador\nACGGGGNN\n", encoding="utf-8")

    # Redirect default folders if your script reads env vars
    monkeypatch.setenv("DOG_DATA_DIR", str(data))
    monkeypatch.setenv("DOG_RESULTS_DIR", str(results))

    # Support both styles: ENTRY() or ENTRY(data_dir, results_dir)
    try:
        ENTRY()
    except TypeError:
        ENTRY(str(data), str(results))

    # It should create some alignment input (name is your script’s choice)
    produced = list(results.glob("*alignment*.*")) + list(results.glob("*input*.*"))
    assert produced, "No alignment input files were written"
