from pathlib import Path
from typing import Union
import csv

PathLike = Union[str, Path]

def update_breed_mapping_file(csv_path: PathLike, accession_id: str, breed: str):
    p = Path(csv_path)

    rows = []
    if p.exists():
        with p.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
                
    
    updated = False
    for row in rows:
        if row["accession_id"] == accession_id:
            row["breed"] = breed
            updated = True
            break
    if not updated:
        rows.append({"accession_id": accession_id, "breed": breed})

    with p.open ("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["accession_id", "breed"])
        writer.writeheader()
        writer.writerows(rows)



