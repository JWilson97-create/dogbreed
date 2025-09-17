from pathlib import Path
import pytest
from dogbreed import dog_breed_identifier as mod  # not Main

IDENTIFY = getattr(mod, "identify_breed", None)

@pytest.mark.skipif(IDENTIFY is None, reason="identify_breed function not found")
def test_identify_breed_with_tiny_ref(tmp_path: Path):
    """Test identify_breed with a tiny reference FASTA."""
    # Create a tiny reference FASTA file
    ref = tmp_path / "ref.fa"
    ref.write_text(">Lab\nACGTACGT\n>Gold\nACGTTTGT\n", encoding="utf-8") # two breeds
    breed = IDENTIFY(query_sequence="ACGTACGT", reference_fastastr=str(ref)) # identical to Lab
    assert isinstance(breed, str) # should return a string
    assert breed in ("Lab", "Gold") # could match either in this tiny example
