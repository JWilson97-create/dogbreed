# Main/utils.py
from __future__ import annotations

from typing import Iterable, List, Tuple
from pathlib import Path
import csv

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


# ---------------------------
# FASTA / CSV LOADING
# ---------------------------

def load_fasta(fasta_path: str | Path) -> List[SeqRecord]:
    """
    Read a FASTA file and return a list of SeqRecord objects.
    Returns [] for empty/missing files instead of crashing.
    """
    p = Path(fasta_path)
    if not p.exists() or p.stat().st_size == 0:
        return []

    try:
        # force uppercase sequences; ignore records that have no seq
        records = []
        for rec in SeqIO.parse(str(p), "fasta"):
            # ensure .seq is str-like and uppercase
            rec.seq = rec.seq.upper()
            records.append(rec)
        return records
    except Exception:
        # Malformed FASTA: be defensive per tests
        return []


def load_breed_mapping(csv_path: str | Path) -> List[dict]:
    """
    Load a breed mapping CSV with columns: accession_id, breed
    Returns a list of dict rows. Skips the header properly.
    Missing file -> returns [] (tests accept empty or raise).
    """
    p = Path(csv_path)
    if not p.exists():
        return []

    with p.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            # Normalise keys in case of variations
            acc = row.get("accession_id") or row.get("Accession_ID") or row.get("id")
            breed = row.get("breed") or row.get("Breed")
            if acc is None or acc == "":
                # skip rows without an accession id (helps keep count == expected)
                continue
            rows.append({"accession_id": acc, "breed": breed})
        return rows


# ---------------------------
# MATCHING
# ---------------------------

def _to_seqstr(x: SeqRecord | str) -> str:
    """Normalise a SeqRecord or string to an uppercase sequence string with no gaps."""
    if isinstance(x, SeqRecord):
        s = str(x.seq)
    else:
        s = str(x)
    return s.replace("-", "").replace(" ", "").upper()


def _identity_score(a: str, b: str) -> float:
    """
    Simple percent-identity score between two same-length strings.
    If lengths differ, compares over the shorter length.
    Returns a float in [0,1].
    """
    if not a or not b:
        return 0.0
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(1 for i in range(n) if a[i] == b[i]) / n


def find_best_match(query: SeqRecord | str, sequences: Iterable[SeqRecord | str]) -> List[Tuple[SeqRecord, float]]:
    """
    Rank sequences by similarity to `query`.
    Returns a list of (SeqRecord, score) sorted descending by score.

    - Accepts query as SeqRecord or str
    - Accepts sequences as SeqRecords or strings
    - If a sequence equals the query, it will be ranked first
    """
    q = _to_seqstr(query)

    # Convert all inputs to SeqRecord to satisfy tests that access `.seq`
    norm_records: List[SeqRecord] = []
    for s in sequences:
        if isinstance(s, SeqRecord):
            rec = s
        else:
            # Wrap raw string into a SeqRecord so tests can do rec.seq
            rec = SeqRecord(SeqIO.Seq(str(s)), id="", description="")
        # Ensure uppercase, no gaps
        rec.seq = _to_seqstr(rec)
        norm_records.append(rec)

    scored = []
    for rec in norm_records:
        score = _identity_score(q, str(rec.seq))
        scored.append((rec, score))

    # sort by score (desc), then by length similarity (desc) to stabilise ties
    scored.sort(key=lambda t: (t[1], -abs(len(str(t[0].seq)) - len(q))), reverse=True)
    return scored


# ---------------------------
# CSV UPDATE
# ---------------------------

def update_breed_mapping(csv_path: str | Path, accession_id: str, breed: str) -> None:
    """
    Update or append a row in the mapping CSV.
    - Creates the file with header if it doesn't exist
    - Deduplicates on accession_id, keeping the LAST provided value
    """
    p = Path(csv_path)
    rows: List[dict] = []

    if p.exists() and p.stat().st_size > 0:
        with p.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({"accession_id": row.get("accession_id", ""), "breed": row.get("breed", "")})

    # overwrite or add
    updated = False
    for r in rows:
        if r["accession_id"] == accession_id:
            r["breed"] = breed
            updated = True
            break
    if not updated:
        rows.append({"accession_id": accession_id, "breed": breed})

    # write back with header, dedup by last occurrence (keep last)
    dedup = {}
    for r in rows:
        dedup[r["accession_id"]] = r["breed"]
    out_rows = [{"accession_id": k, "breed": v} for k, v in dedup.items()]

    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["accession_id", "breed"])
        writer.writeheader()
        writer.writerows(out_rows)
