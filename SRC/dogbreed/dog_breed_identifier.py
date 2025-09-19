from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Tuple
import csv

from dogbreed.compare_sequences import compare_sequences
from dogbreed.phylogenetic_tree import generate_phylogenetic_tree as generate_tree
from Bio import SeqIO


class DogBreedIdentifier:
    def __init__(self, fasta_file: str, mystery_file: str, out_dir: str):
        self.fasta_file = Path(fasta_file)
        self.mystery_file = Path(mystery_file)
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

        # Results files
        self.named_fasta = self.out_dir / "dog_sequences_named.fa"

    def replace_ids_with_names(self) -> str:
        """Convert FASTA accession IDs to breed names using a CSV mapping file."""
        map_file = Path("data/breed_mapping.csv")
        mapping: Dict[str, str] = {}

        with open(map_file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapping[row["accession_id"]] = row["breed"]

        # Replace IDs in fasta file
        records = []
        for record in SeqIO.parse(str(self.fasta_file), "fasta"):
            if record.id in mapping:
                record.id = mapping[record.id]
                record.description = mapping[record.id]
            records.append(record)

        SeqIO.write(records, str(self.named_fasta), "fasta")
        return str(self.named_fasta)

    def identify(self) -> List[Tuple[str, float]]:
        """
        Compare the mystery sequence to the named reference set.
        Returns a list of (best_id, percent_identity).
        """
        if not self.named_fasta.exists():
            self.replace_ids_with_names()

        query_record = next(SeqIO.parse(self.mystery_file, "fasta"))
        query_seq = str(query_record.seq)

        ranked = compare_sequences(query_seq, str(self.named_fasta))

        if ranked:
            return [(ranked[0][0], ranked[0][1])]
        else:
            return [("Unknown", 0.0)]

    def build_tree(self) -> List[str]:
        """
        Build a phylogenetic tree from the named FASTA file.
        Returns list of output file paths [nwk, png].
        """
        if not self.named_fasta.exists():
            self.replace_ids_with_names()

        nwk_name = "phylogenetic_tree.nwk"
        png_name = "phylogenetic_tree.png"
        return generate_tree(self.named_fasta, self.out_dir, nwk_name, png_name)
