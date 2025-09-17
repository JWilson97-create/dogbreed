# SRC/dogbreed/dog_breed_identifier.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Tuple
import csv

from Bio import SeqIO
from dogbreed.compare_sequences import compare_sequences, closest_match



class DogBreedIdentifier:
    """
    Keeps paths only in __init__. No I/O or heavy work at import/construct time.
    Methods do the work and return useful paths/values for tests.
    """

    def __init__(self, fasta_file: Path, mystery_file: Path, mapping_file: Path, output_dir: Path):
        """
        Initialize the DogBreedIdentifier with file paths.
        """
        self.fasta_file = Path(fasta_file)
        self.mystery_file = Path(mystery_file)
        self.mapping_file = Path(mapping_file)
        self.output_dir = Path(output_dir)

        # Precomputed destinations (don’t create/write here)
        self.named_fasta = self.output_dir / "dog_sequences_named.fa"
        self.alignment_file = self.output_dir / "dog_sequences.aln"  # optional if you never use it
        self.dnd_file = self.output_dir / "dog_sequences.dnd"        # optional if you never use it
        self.tree_png = self.output_dir / "phylogenetic_tree.png"
        self.tree_nwk = self.output_dir / "phylogenetic_tree.nwk"

    # --------------------- helpers ---------------------

    def _load_map(self) -> Dict[str, str]:
        """
        Load the mapping from accession IDs to breed names.
        """
        mapping: Dict[str, str] = {} # accession_id -> breed
        with self.mapping_file.open(newline="") as f: # type: ignore
            for row in csv.DictReader(f): # type: ignore
                mapping[row["accession_id"]] = row["breed"] # map accession_id to breed
        return mapping

    # --------------------- public API ---------------------

    def replace_ids_with_names(self) -> str:
        """
        Read self.fasta_file, replace record IDs using mapping CSV,
        write to self.named_fasta. Spaces become underscores.
        Returns the path written (string for easy assertions).
        """
        self.output_dir.mkdir(parents=True, exist_ok=True) # ensure output dir exists
        mapping = self._load_map() # load mapping

        with self.named_fasta.open("w") as out_handle: # open output file
            for rec in SeqIO.parse(self.fasta_file, "fasta"): # parse input FASTA
                breed = mapping.get(rec.id, "Unknown").replace(" ", "_") # get breed or Unknown
                rec.id = breed # set record ID to breed
                rec.description = ""  # clean header
                SeqIO.write(rec, out_handle, "fasta") # write record

        return str(self.named_fasta)

    def identify_mystery(self) -> Tuple[str, float]:
        """
        Compare the first sequence in self.mystery_file to the named reference set
        (creates it if missing). Returns (best_id, percent_identity).
        """
        if not self.named_fasta.exists():
            self.replace_ids_with_names()

        # Load the query sequence (first record)
        query_record = next(SeqIO.parse(self.mystery_file, "fasta")) # type: ignore
        query_seq = str(query_record.seq) # get sequence string

        # Compare against named set. compare_sequences returns ranked (id, %id)
        ranked = compare_sequences(query_seq, self.named_fasta)
        best_id = ranked[0][0] if ranked else "Unknown"
        best_pid = ranked[0][1] if ranked else 0.0
        return best_id, best_pid # return best match

    def build_tree(self) -> List[str]:
        """
        Generate a phylogenetic tree from the named FASTA.
        Returns list of written file paths.
        """
        from .generate_phylogenetic_tree import generate_tree # avoid circular import
        if not self.named_fasta.exists(): # ensure named FASTA exists
            self.replace_ids_with_names() # create if missing
        return generate_tree(
            fasta_path=self.named_fasta,
            output_dir=self.output_dir,
            newick_name=self.tree_nwk.name,
            png_name=self.tree_png.name,
        ) # return list of written paths

    def run(self) -> List[str]:
        """
        Convenience: do the whole pipeline (rename IDs -> build tree).
        Returns list of written file paths.
        """
        self.replace_ids_with_names()
        return self.build_tree() # return list of written paths
