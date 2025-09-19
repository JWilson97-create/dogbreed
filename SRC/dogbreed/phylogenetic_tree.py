from pathlib import Path
from typing import List
from Bio import Phylo
import matplotlib.pyplot as plt

def generate_phylogenetic_tree(fasta_path: Path, output_dir: Path, newick_name: str, png_name: str) -> List[str]:
    """
    Generate a phylogenetic tree from a FASTA file.
    Returns list of output file paths [nwk, png].
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    nwk_path = output_dir / newick_name
    png_path = output_dir / png_name

    # Dummy tree for now
    with open(nwk_path, "w") as f:
        f.write("(A:0.1,B:0.2,C:0.3);")

    tree = Phylo.read(str(nwk_path), "newick")
    Phylo.draw(tree, do_show=False)
    plt.savefig(png_path)
    plt.close()

    return [str(nwk_path), str(png_path)]
