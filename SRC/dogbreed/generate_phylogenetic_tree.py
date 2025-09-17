from __future__ import annotations
from pathlib import Path
from typing import List, Union, Optional
import os

from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

PathLike = Union[str, Path]

def _pick_fasta(data_dir: Path, results_dir: Path) -> Path:
    """
    Pick a FASTA file for alignment.
    """
    # Test writes this file into the results dir
    cand = results_dir / "alignment_input.fasta"
    if cand.exists():
        return cand
    # Fallbacks for your project structure
    for p in (
        data_dir / "dog_sequences_named.fa",
        data_dir / "dog_sequences.fa",
        Path("data") / "dog_sequences_named.fa",
        Path("data") / "dog_sequences.fa",
    ):
        if p.exists():
            return p
    raise FileNotFoundError("No input FASTA found (looked for alignment_input.fasta or dog_sequences*.fa)")

def generate_tree(
            fasta_path: PathLike,
    output_dir: PathLike,
    newick_name: str = "phylogenetic_tree.nwk",
    png_name: str = "phylogenetic_tree.png",
) -> List[str]:
    """Build an NJ tree from FASTA, write Newick (+PNG if possible), return written paths."""
    fasta_path = Path(fasta_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    alignment = AlignIO.read(fasta_path, "fasta") # assume already aligned
    calc = DistanceCalculator("identity") # Calculate distance matrix
    dm = calc.get_distance(alignment) # Get distance matrix
    tree = DistanceTreeConstructor().nj(dm) # Build neighbor-joining tree

    written: List[str] = [] # Initialize list of written file paths
    newick_path = out_dir / newick_name # Define output Newick file path
    Phylo.write(tree, newick_path, "newick") # Write tree to Newick file
    written.append(str(newick_path)) # Append Newick file path to written list

    try:
        import matplotlib.pyplot as plt  # optional
        plt.figure()
        Phylo.draw(tree, do_show=False)
        png_path = out_dir / png_name
        plt.savefig(png_path, bbox_inches="tight")
        plt.close()
        written.append(str(png_path))
    except Exception:
        pass

    return written

# >>> ENTRY expected by the test <<<
def ENTRY(data_dir: Optional[PathLike] = None, results_dir: Optional[PathLike] = None) -> List[str]:
    """
    Test harness entry point.
    - If called with args, use them.
    - If called with no args, read DOG_DATA_DIR and DOG_RESULTS_DIR from env.
    Returns list of written file paths.
    """
    if data_dir is None:
        data_dir = os.getenv("DOG_DATA_DIR", "data")
    if results_dir is None:
        results_dir = os.getenv("DOG_RESULTS_DIR", "Results")

    data_dir = Path(data_dir)
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    fasta = _pick_fasta(data_dir, results_dir)
    return generate_tree(fasta, results_dir)

# Optional manual run
def main() -> None:
    for p in ENTRY():
        print(p)

if __name__ == "__main__":
    main()