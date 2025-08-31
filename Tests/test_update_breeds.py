
from pathlib import Path
import os, sys, importlib, csv
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

mod = importlib.import_module("Main.update_breeds")

# Support either function name
UPDATE_FN = (
    getattr(mod, "update_breed", None)
    or getattr(mod, "update_breed_mapping", None)
    or getattr(mod, "update_breed_mapping_file", None)
)


def _read_rows(p: Path):
    with p.open(newline="") as f:
        return list(csv.DictReader(f))


@pytest.mark.skipif(UPDATE_FN is None, reason="update_breed mapping function not found")
def test_update_breed_mapping_adds_and_updates(tmp_path: Path):
    csv_path = tmp_path / "breed_mapping.csv"
    csv_path.write_text("accession_id,breed\nid1,Lab\n", encoding="utf-8")

    # add new id
    UPDATE_FN(str(csv_path), "new_id", "Shiba Inu")
    rows = _read_rows(csv_path)
    assert any(r["accession_id"] == "new_id" and r["breed"] == "Shiba Inu" for r in rows)

    # update existing
    UPDATE_FN(str(csv_path), "id1", "Golden Retriever")
    rows = _read_rows(csv_path)
    breed = next(r["breed"] for r in rows if r["accession_id"] == "id1")
    assert breed == "Golden Retriever"


@pytest.mark.skipif(UPDATE_FN is None, reason="update_breed mapping function not found")
def test_update_breed_mapping_creates_file_if_missing(tmp_path: Path):
    target = tmp_path / "created.csv"
    UPDATE_FN(str(target), "abc", "Test Breed")
    rows = _read_rows(target)
    assert rows == [{"accession_id": "abc", "breed": "Test Breed"}]


@pytest.mark.skipif(UPDATE_FN is None, reason="update_breed mapping function not found")
def test_update_breed_mapping_double_write_overwrites(tmp_path: Path):
    csv_path = tmp_path / "bm.csv"
    UPDATE_FN(str(csv_path), "id1", "X")
    UPDATE_FN(str(csv_path), "id1", "Y")
    rows = _read_rows(csv_path)
    vals = [r["breed"] for r in rows if r["accession_id"] == "id1"]
    assert vals[-1] == "Y"
