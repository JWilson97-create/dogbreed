from pathlib import Path
from typing import Union
import csv
from Bio import SeqIO


def generate_alignment_input(
    fasta_path: Union[str, Path],
    map_path: Union[str, Path],
    output_dir: Union[str, Path]
) -> str:
    """
    Generate an alignment FASTA file with breed names as sequence headers.
    Falls back to accession ID if no mapping is found.
    """
    fasta_path = Path(fasta_path)
    map_path = Path(map_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load breed mapping (accession_id -> breed)
    mapping = {}
    with open(map_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapping[row["accession_id"]] = row["breed"]

    # Rewrite sequences with breed names (fallback to accession if missing)
    records = []
    for record in SeqIO.parse(fasta_path, "fasta"):
        acc_id = record.id  # keep original accession ID
        if acc_id in mapping:
            record.id = mapping[acc_id]
            record.description = mapping[acc_id]
        else:
            # fallback: accession ID
            record.id = acc_id
            record.description = acc_id
        records.append(record)

    # Save new FASTA file
    out_fasta = output_dir / "alignment_with_names.fa"
    SeqIO.write(records, str(out_fasta), "fasta")
    return str(out_fasta)
