# SRC/dogbreed/cli.py

import argparse
from pathlib import Path
from dogbreed.dog_breed_identifier import DogBreedIdentifier


def identify():
    """CLI: Identify the breed of a mystery sequence."""
    parser = argparse.ArgumentParser("dogbreed-identify")
    parser.add_argument("--fasta", required=True, help="Reference FASTA (all dog breeds)")
    parser.add_argument("--mystery", required=True, help="Mystery FASTA file (unknown breed)")
    parser.add_argument("--map", required=True, help="CSV mapping accession_id → breed")
    parser.add_argument("--out", default="Results", help="Output directory")
    args = parser.parse_args()

    # Run identification
    identifier = DogBreedIdentifier(args.fasta, args.mystery, args.map, args.out)
    best_id, pid = identifier.identify_mystery()
    breed = identifier.lookup_breed(best_id)

    print(f"✅ Best match: {breed} ({best_id}), {pid:.2f}% identity")


def tree():
    """CLI: Build a phylogenetic tree from reference FASTA."""
    parser = argparse.ArgumentParser("dogbreed-tree")
    parser.add_argument("--fasta", required=True, help="Reference FASTA file")
    parser.add_argument("--map", required=True, help="CSV mapping accession_id → breed")
    parser.add_argument("--out", default="Results", help="Output directory")
    args = parser.parse_args()

    identifier = DogBreedIdentifier(args.fasta, args.fasta, args.map, args.out)
    written = identifier.build_tree()

    print("🌳 Tree generated:")
    for w in written:
        print(f"   - {w}")
