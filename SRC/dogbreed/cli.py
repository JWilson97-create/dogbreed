from __future__ import annotations
from pathlib import Path
import argparse

from .dog_breed_identifier import DogBreedIdentifier
from .generate_phylogenetic_tree import generate_tree

def identify():
    p = argparse.ArgumentParser("dogbreed-identify")
    p.add_argument("--fasta", required=True, help="Reference FASTA")
    p.add_argument("--mystery", required=True, help="Unknown sample FASTA")
    p.add_argument("--map", required=True, help="CSV mapping accession_id,breed")
    p.add_argument("--out", default="Results", help="Output directory")
    args = p.parse_args()

    idr = DogBreedIdentifier(args.fasta, args.mystery, args.map, args.out)
    best_id, pid = idr.identify_mystery()
    print(f"{best_id}\t{pid:.2f}")

def make_tree():
    p = argparse.ArgumentParser("dogbreed-tree")
    p.add_argument("--fasta", required=True, help="Named FASTA (or any FASTA alignment)")
    p.add_argument("--out", default="Results", help="Output directory")
    p.add_argument("--nwk", default="phylogenetic_tree.nwk")
    p.add_argument("--png", default="phylogenetic_tree.png")
    args = p.parse_args()
    written = generate_tree(Path(args.fasta), Path(args.out), args.nwk, args.png)
    for w in written:
        print(w)

# Example usage:
# dogbreed-identify --fasta data/dog_sequences.fa --mystery data/mystery_breed.fasta --map data/breed_mapping.csv --out Results
# dogbreed-tree --fasta Results/dog_sequences_named.fa --out Results
