import sys, os
# Ensure the utils module can be imported from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Main.utils import load_fasta, load_breed_mapping, find_best_match, update_breed_mapping


def test_utils_functions():
    # Test 1: Load FASTA
    sequences = load_fasta("data/test_sequence.fa")
    print(f"Loaded {len(sequences)} sequences from FASTA.")
    
    # Test 2: Load_breed_mapping
    breed_mapping = load_breed_mapping("data/breed_mapping.csv")
    print(f"Loaded {len(breed_mapping)} breed(s) from CSV.")

    # Test 3: find_best_match
    if len(sequences) > 0:
        matches = find_best_match(sequences[0], sequences)
        print(f"Found {len(matches)} matches for the query sequence.")

    # Test 4: Update breed mapping
    update_breed_mapping("data/breed_mapping.csv", "test_id", "Test Breed")
    print("Breed mapping updated successfully.")

if __name__ == "__main__":
    test_utils_functions()