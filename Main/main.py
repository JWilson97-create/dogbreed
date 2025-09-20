import os
import csv
from Bio import SeqIO
from Bio.Align import PairwiseAligner
import matplotlib.pyplot as plt
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Align.Applications import MuscleCommandline


MIN_SCORE_THRESHOLD = 15000 # Minimum score threshold for alignment

# Load FASTA files
def load_fasta(file_path): # Load a FASTA file and return a list of SeqIO records
    """
    Load a FASTA file and return a list of SeqIO records.
    """
    return list(SeqIO.parse(file_path, "fasta")) # Load the FASTA file


# Load breed mapping
def load_breed_mapping(file_path): # Load the breed mapping CSV file
    """
    Load a breed mapping CSV file and return a dictionary mapping accession IDs to breed names.
    """
    mapping = {} # Initialize an empty dictionary to hold the mapping
    with open(file_path, newline='') as csvfile: # Open the CSV file
        reader = csv.reader(csvfile) # Create a CSV reader
        next(reader)  # Skip header
        for row in reader:
            accession_id = row[0] # Get the accession ID
            breed_name = row[1] # Get the breed name
            mapping[accession_id] = breed_name # Map accession ID to breed name
    return mapping # Return the completed mapping

# Update breed mapping

def update_breed_mapping(file_path, accession_id, breed_name="Unknown Breed"): # Update the breed mapping
    """
Update the breed mapping CSV file with a new accession ID and breed name.
"""
    lookup_path = os.path.join(os.path.dirname(__file__), "local_breed_lookup.csv")

    # Try to update from local_breed_lookup.csv
    try:
        with open(lookup_path, "r") as lookup_file: # Open the local breed lookup file
            reader = csv.reader(lookup_file) # Create a CSV reader
            next(reader, None)  # Skip header
            for row in reader: # Iterate over each row in the CSV
                if not row or len(row) < 2: # Skip empty or malformed rows
                    continue
                if row[0] == accession_id: # If the accession ID matches
                    breed_name = row[1] # Get the breed name
                    break
    except FileNotFoundError:  # Handle file not found error
        print("❌ local_breed_lookup.csv not found — using 'Unknown Breed'")

    # Update breed_mapping.csv
    with open(file_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([accession_id, breed_name])
    print(f"✅ breed_mapping.csv updated: {accession_id} → {breed_name}")



def find_best_match(test_seq, database): # Find the best match for a given sequence in the database
    """
    Find the best match for a given sequence in the database.
    """
    aligner = PairwiseAligner() # Create a pairwise aligner
    database = database[0:100]  # Limit to first 100 records for testing
    aligner.mode = 'local'  # Use 'local' to avoid memory errors
    results = [] # Initialize an empty list to hold the results

    for record in database: # Iterate over each record in the database
        score = aligner.score(test_seq, record.seq) # Compute the alignment score
        results.append((record, score)) # Append the result tuple to the results list

    for i, record in enumerate(database):
        score = aligner.score(test_seq, record.seq)
        results.append((record, score))

        if i % 100 == 0:  # Print progress every 100 records
            print(f"Compared {i + 1}/{len(database)} sequences...")

    results.sort(key=lambda x: x[1], reverse=True) # Sort results by score
    return results[:3] # Return the top 3 results

# Main function

def main(): # Main function
    """
    Main function to run the breed matching pipeline.
    """
    # Load files
    query = list(SeqIO.parse("data/mystery_breed.fasta", "fasta")) # Load the query FASTA file
    database = load_fasta(os.path.join("data", "dog_breeds.fasta")) # Load the database FASTA file
    # Load breed mapping
    breed_mapping_path = os.path.join("data", "breed_mapping.csv") # Path to the breed mapping CSV file
    breed_mapping = load_breed_mapping(breed_mapping_path) # Load the breed mapping

    top_matches = find_best_match(query[0].seq, database) # Find the best matches
    print("\nTop 3 Closest Dog Breed Matches:") # Print header for matches
    for i, (match, score) in enumerate(top_matches, 1): # Iterate over the top matches
        accession_id = match.id if hasattr(match, "id") else match[0]
        breed_name = breed_mapping.get(accession_id, "Unknown Breed") # Get the breed name
        print(f"{i}. {breed_name} (ID: {accession_id}) - Score: {score:.1f}") # Print the match information

# Save the best matches to a text file
    with open("closest_match.txt", "w") as f: # Open the output file
        for i, (match, score) in enumerate(top_matches,1): # Iterate over the top matches
           breed_name = breed_mapping.get(match.id, "Unknown Breed")
           print (f"{i}. {breed_name} (ID: {accession_id})- Score: {score:.1f}") # Print the match information
           f.write(f"{i}. {breed_name} (ID: {accession_id}) - Score: {score:.1f}\n") # Write the match information

            # Update breed_mapping.csv if unknown
        if breed_name == "Unknown Breed": # If the breed is unknown
           update_breed_mapping(breed_mapping_path, accession_id, "Unknown Breed") # Update the breed mapping
            # Save the best match to closest_match.txt


# Prepare labels and scores
           mystery_id = query[0].id 

           labels = []
           scores = []
           colors = []

           for match, score in top_matches: # Iterate over the top matches
               acc_id = match.id # Get the accession ID
               breed_name = breed_mapping.get(acc_id, "Unknown Breed") # Get the breed name
               labels.append(f"{breed_name} (ID: {acc_id})") # Append label
               scores.append(score) # Append score

               if acc_id == mystery_id: # Check if this is the mystery breed
                   colors.append("crimson") # Append color for mystery breed
               else: # If not the mystery breed
                   colors.append("steelblue") # Append color for non-mystery breeds

           plt.figure(figsize=(10, 6))
           plt.barh(labels, scores, color=colors, edgecolor='black')
           plt.xlabel("Alignment Score")
           plt.title("Top 3 Closest Dog Breed Matches")
           plt.tight_layout()
           plt.savefig("Results/top_matches_chart.png")
           plt.show()


def generate_phylogenetic_tree(fasta_path, aligned_path="aligned_dogs.fa"):
    """
    Generate a phylogenetic tree from a FASTA file using MUSCLE alignment.
    Saves and displays the tree.
    """
    try:
        # Run MUSCLE to align sequences
        muscle_cline = MuscleCommandline(input=fasta_path, out=aligned_path)
        stdout, stderr = muscle_cline()

        # Read aligned sequences
        alignment = AlignIO.read(aligned_path, "fasta")

        # Calculate distance matrix
        calculator = DistanceCalculator("identity")
        dm = calculator.get_distance(alignment)

        # Build tree using Neighbor Joining
        constructor = DistanceTreeConstructor()
        tree = constructor.nj(dm)

        # Draw tree
        Phylo.draw(tree)

        # Save tree to file
        Phylo.write(tree, "Results/dog_breed_tree.xml", "phyloxml")
        print("✅ Phylogenetic tree generated and saved to 'Results/dog_breed_tree.xml'")

    except Exception as e:
        print(f"❌ Error generating phylogenetic tree: {e}")



if __name__ == "__main__":
    main()
