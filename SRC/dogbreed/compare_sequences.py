# SRC/dogbreed/compare_sequences.py
from __future__ import annotations
from typing import Tuple, Dict, List, Iterable, Union
from Bio import Align, SeqIO, pairwise2
from Bio.SeqRecord import SeqRecord

# Configure a deterministic global aligner (no pairwise2)
_aligner = Align.PairwiseAligner()
_aligner.mode = "global"           # Needleman–Wunsch style
_aligner.match_score = 1.0
_aligner.mismatch_score = 0.0      # pure identity
_aligner.open_gap_score = -1.0
_aligner.extend_gap_score = -0.5

def _norm(seq: str) -> str:
    """Uppercase, strip, validate DNA sequence."""
    s = (seq or "").strip().upper()
    if not s:
        raise ValueError("Empty sequence")
    # allow common DNA symbols; tweak if your tests expect more
    allowed = set("ACGTN-")
    bad = {c for c in s if c not in allowed}
    if bad:
        raise ValueError(f"Invalid characters: {''.join(sorted(bad))}")
    return s


def align_pair(seq1: str, seq2: str):
    """
    Align two sequences and return the alignment object.
    """
    s1, s2 = _norm(seq1), _norm(seq2)
    return max(_aligner.align(s1, s2), key=lambda a: a.score)

def percent_identity(seq1: str, seq2: str) -> float:
    """
    Compute the percent identity between two sequences.
    """
    s1, s2 = _norm(seq1), _norm(seq2)
    aln = pairwise2.align.globalxx(s1, s2, one_alignment_only=True)[0]
    a_str, b_str = aln[0], aln[1]

    matches = sum(1 for a, b in zip(a_str, b_str) if a == b and a != "-" and b != "-")
    total = sum(1 for a, b in zip(a_str, b_str) if a != "-" and b != "-")
    return (matches / total) * 100.0 if total else 0.0

def compare_two(seq1: str, seq2: str) -> Dict[str, float]:
    """
    Compare two sequences and return a dict of comparison metrics.
    """
    return {"percent_identity": round(percent_identity(seq1, seq2), 2)}

def read_fasta(path: str):
    """
    Read a FASTA file and return a list of SeqRecords.
    """
    return list(SeqIO.parse(path, "fasta"))

def compare_fasta(path: str) -> Tuple[str, str, float]:
    """Compare the first two sequences in a FASTA and return (id1, id2, %id)."""
    recs = read_fasta(path)
    if len(recs) < 2:
        raise ValueError("Need at least two sequences")
    pid = percent_identity(str(recs[0].seq), str(recs[1].seq))
    return (recs[0].id, recs[1].id, round(pid, 2))


RecordsLike = Union[str, Iterable[SeqRecord], Iterable[Tuple[str, str]]]

def _iter_records(records: RecordsLike) -> Iterable[SeqRecord]:
    """
Yield (id, seq) pairs from:
- a FASTA filepath
- an iterable of Bio SeqRecords
- an iterable of (id, seq) tuples
    """
    if isinstance(records, str):
        for rec in read_fasta(records):
            yield rec.id, str(rec.seq)
    else:
        for item in records:
            if isinstance(item, SeqRecord):
                yield item.id, str(item.seq)
            else:
                rec_id, rec_seq = item
                yield str(rec_id), str(rec_seq)

def compare_sequences(query_seq: str, records: RecordsLike) -> List[Dict[str, Union[str, float]]]:  
    """
    Return a list of comparison results between the query sequence and each record.
    """
    q = _norm(query_seq)
    scores: List[Tuple[str, float]] = []
    for rec_id, rec_seq in _iter_records(records):
        pid = percent_identity(q, rec_seq)
        scores.append((rec_id, round(pid, 2)))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def closest_match(query_seq: str, records: RecordsLike) -> str:
    """
    Convenience wrapper: return the ID of the top-scoring record.
    """
    ranked = compare_sequences(query_seq, records)
    return ranked[0][0] if ranked else ""