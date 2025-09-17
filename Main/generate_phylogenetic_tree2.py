import os
import matplotlib.pyplot as plt
from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor


def main():
    """
    Main function to generate a phylogenetic tree from input sequences.
    """
    # Optional: Make sure Results folder exists
    os.makedirs("Results", exist_ok=True)

    # Define the path to your input FASTA file
    fasta_file = "input_sequences.fasta"  # TODO: Replace with your actual FASTA file path

    # Step 1: Run ClustalW alignment (requires clustalw2 installed)
    clustalw_cline = ClustalwCommandline("C:/Program Files (x86)/ClustalW2/clustalw2.exe", infile=fasta_file)
    stdout, stderr = clustalw_cline()

    # Define the alignment file name (ClustalW outputs .aln by default)
    aln_file = os.path.splitext(fasta_file)[0] + ".aln"

    # Step 2: Load the alignment
    alignment = AlignIO.read(aln_file, "clustal")

    # Step 3: Calculate distances
    calculator = DistanceCalculator("identity")
    distance_matrix = calculator.get_distance(alignment)

    # Step 4: Build tree using UPGMA
    constructor = DistanceTreeConstructor()
    tree = constructor.upgma(distance_matrix)

    import matplotlib.pyplot as plt
    from Bio import Phylo

    # Step 5: Save the tree as an image
    fig = plt.figure(figsize=(10, 8)) # Adjust figure size as needed
    axes = fig.add_subplot(1, 1, 1) # Create a subplot

    for clade in tree.find_clades(): # Replace underscores in names
        if clade.name:
            clade.name = clade.name.replace("_", " ").title() # Replace underscores with spaces

    # Highlight unknown clades
    for clade in tree.find_clades():
        if clade.name and "Unknown" in clade.name:
            clade.color = "red"
            clade.name =  "Mystery Breed"

    Phylo.draw(tree, do_show=False, axes=axes) # Draw the tree
    tree_file = "Results/phylogenetic_tree.png" # Define output image file path
    plt.savefig(tree_file) # Save the figure
    Phylo.write(tree, "Results/phylogenetic_tree.nwk", "newick") # Save the tree in Newick format
    print(f"✅ Phylogenetic tree saved to: {tree_file}") # Print confirmation


if __name__ == "__main__":
    main()
