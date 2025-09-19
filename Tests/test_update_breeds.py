from pathlib import Path
import csv
import pytest
from dogbreed.update_breeds import update_breed_mapping_file


def read_csv(path: Path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def test_update_breed_mapping_adds_and_updates(tmp_path: Path):
    csv_path = tmp_path / "breed_mapping.csv"

    # Initial CSV
    csv_path.write_text("accession_id,breed\nid1,Labrador\n", encoding="utf-8")

    updates = {
        "id1": "Golden Retriever",  # update existing
        "id2": "Poodle"             # add new
    }

    update_breed_mapping_file(csv_path, updates)
    rows = read_csv(csv_path)

    breeds = {row["accession_id"]: row["breed"] for row in rows}

    # id1 updated
    assert breeds["id1"] == "Golden Retriever"
    # id2 added
    assert breeds["id2"] == "Poodle"
    # CSV should contain exactly 2 rows
    assert len(breeds) == 2
