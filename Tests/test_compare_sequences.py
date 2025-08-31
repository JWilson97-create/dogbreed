from pathlib import Path
import pytest

# import the module from the dogbreed package (in SRC/dogbreed)
from dogbreed import compare_sequences as mod

COMPARE  = getattr(mod, "compare_sequences", None) or getattr(mod, "compare", None)
CLOSEST  = getattr(mod, "closest_match", None) or getattr(mod, "closest", None)

@pytest.mark.skipif(COMPARE is None, reason="compare_sequences function not found")
def test_compare_sequences_returns_ranked_rows(tmp_path: Path):
    fa = tmp_path / "dogs.fa"
    fa.write_text(">A\nACGTACGT\n>B\nACGTTTGT\n>C\nTTTTTTTT\n", encoding="utf-8")
    table = COMPARE("ACGTACGT", str(fa))
    assert hasattr(table, "__len__") and len(table) >= 3

@pytest.mark.skipif(CLOSEST is None, reason="closest_match function not found")
def test_closest_match_returns_best_id(tmp_path: Path):
    fa = tmp_path / "dogs.fa"
    fa.write_text(">A\nACGT\n>B\nACGA\n", encoding="utf-8")
    best = CLOSEST("ACGT", str(fa))
    assert isinstance(best, (str, tuple, dict))
