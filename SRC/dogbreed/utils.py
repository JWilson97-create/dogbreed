from pathlib import Path
from typing import Dict, List, Tuple
from Bio import SeqIO
import csv


def load_fasta(fasta_path: Path) -> Dict[str, str]:
    """
    Load sequences from FASTA into {id: sequence}.
    Handles empty or malformed files gracefully.
    """
    sequences = {}
    if not fasta_path.exists():
        return sequences

    try:
        for record in SeqIO.parse(str(fasta_path), "fasta"):
            # Only keep valid IDs
            if record.id.strip():
                sequences[record.id] = str(record.seq)
    except Exception:
        # Malformed FASTA → return empty dict instead of crashing
        return {}

    return sequences


def load_breed_mapping(csv_path: Path) -> Dict[str, str]:
    """
    Load mapping {accession_id: breed} from CSV.
    Handles missing or malformed files.
    """
    mapping = {}
    if not csv_path.exists():
        return mapping

    try:
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "accession_id" in row and "breed" in row:
                    mapping[row["accession_id"]] = row["breed"]
    except Exception:
        return {}

    return mapping


def find_best_match(query: str, reference: Dict[str, str]) -> List[Tuple[str, float]]:
    """
    Find the best match for a query sequence in reference dict.
    Returns ranked list [(id, percent_identity), ...].
    """
    scores = []
    for acc, seq in reference.items():
        matches = sum(q == s for q, s in zip(query, seq))
        pid = (matches / max(len(query), len(seq))) * 100 if seq else 0.0
        scores.append((acc, pid))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def update_breed_mapping(csv_path: Path, updates: Dict[str, str]) -> None:
    """
    Update or add breeds in the mapping CSV.
    Overwrites old values if accession already exists.
    """
    rows = []
    seen = set()

    # Load existing
    if csv_path.exists():
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                acc = row["accession_id"]
                if acc in updates:
                    row["breed"] = updates[acc]
                rows.append(row)
                seen.add(acc)

    # Add new rows
    for acc, breed in updates.items():
        if acc not in seen:
            rows.append({"accession_id": acc, "breed": breed})

    # Write back
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["accession_id", "breed"])
        writer.writeheader()
        writer.writerows(rows)
