
from pathlib import Path
import os, sys, importlib, csv
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) # add project root to sys.path    
if ROOT not in sys.path:
    sys.path.insert(0, ROOT) # add project root to sys.path

mod = importlib.import_module("Main.update_breeds") # dynamic import

# Support either function name
UPDATE_FN = (
    getattr(mod, "update_breed", None)
    or getattr(mod, "update_breed_mapping", None)
    or getattr(mod, "update_breed_mapping_file", None)
)


def _read_rows(p: Path):
    """Read all rows from a CSV file as a list of dictionaries."""
    with p.open(newline="") as f:
        return list(csv.DictReader(f)) # return list of rows


@pytest.mark.skipif(UPDATE_FN is None, reason="update_breed mapping function not found")
def test_update_breed_mapping_adds_and_updates(tmp_path: Path):
    """Add a new ID and update an existing one in the CSV."""
    csv_path = tmp_path / "breed_mapping.csv" # target CSV path
    csv_path.write_text("accession_id,breed\nid1,Lab\n", encoding="utf-8") # initial content

    # add new id
    UPDATE_FN(str(csv_path), "new_id", "Shiba Inu")
    rows = _read_rows(csv_path) # read back rows
    assert any(r["accession_id"] == "new_id" and r["breed"] == "Shiba Inu" for r in rows)

    # update existing
    UPDATE_FN(str(csv_path), "id1", "Golden Retriever") # update id1
    rows = _read_rows(csv_path) # read back rows
    breed = next(r["breed"] for r in rows if r["accession_id"] == "id1")  # get updated breed
    assert breed == "Golden Retriever"


@pytest.mark.skipif(UPDATE_FN is None, reason="update_breed mapping function not found")
def test_update_breed_mapping_creates_file_if_missing(tmp_path: Path):
    """If the CSV is missing, it should be created with the new entry."""
    target = tmp_path / "created.csv"
    UPDATE_FN(str(target), "abc", "Test Breed")
    rows = _read_rows(target) # read back rows
    assert rows == [{"accession_id": "abc", "breed": "Test Breed"}] # check content matches exactly 


@pytest.mark.skipif(UPDATE_FN is None, reason="update_breed mapping function not found")
def test_update_breed_mapping_double_write_overwrites(tmp_path: Path):
    """Two updates to the same ID should result in the last one being present."""
    csv_path = tmp_path / "bm.csv"
    UPDATE_FN(str(csv_path), "id1", "X")
    UPDATE_FN(str(csv_path), "id1", "Y") # second write
    rows = _read_rows(csv_path) # read back rows
    vals = [r["breed"] for r in rows if r["accession_id"] == "id1"] # get all breeds for id1
    assert vals[-1] == "Y" # the last write should win 
