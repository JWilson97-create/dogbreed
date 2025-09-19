import csv
from pathlib import Path
from typing import Dict


def update_breed_mapping_file(csv_path: Path, updates: Dict[str, str]) -> None:
    """
    Update the breed mapping CSV with new or updated accession_id → breed pairs.

    - If an accession_id exists, update its breed.
    - If it does not exist, add it as a new row.
    - Preserves all other existing rows.
    """
    csv_path = Path(csv_path)

    # Load existing rows into a dict
    existing = {}
    if csv_path.exists():
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing[row["accession_id"]] = row["breed"]

    # Apply updates (overwrites or adds new)
    for acc_id, breed in updates.items():
        existing[acc_id] = breed

    # Write back to CSV
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["accession_id", "breed"])
        writer.writeheader()
        for acc_id, breed in existing.items():
            writer.writerow({"accession_id": acc_id, "breed": breed})

