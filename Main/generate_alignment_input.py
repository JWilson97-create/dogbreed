from Bio import SeqIO

# Paths
dog_sequences_file = "data/dog_sequences.fa"
mystery_file = "data/mystery_breed.fasta"
output_file = "data/alignment_input.fasta"

# Top matching sequence IDs from main.py results
top_ids = [
    "AY566744.1",  # English Springer Spaniel
    "CM023446.1",  # Golden Retriever
    "MW916023.1"   # Labrador Retriever
]

# Load all dog sequences
all_dogs = SeqIO.to_dict(SeqIO.parse(dog_sequences_file, "fasta"))

# Load the mystery breed
mystery_seq = list(SeqIO.parse(mystery_file, "fasta"))[0]

# Build final list: mystery + top 3 matches
sequences_to_write = [mystery_seq]

for id in top_ids:
    if id in all_dogs:
        sequences_to_write.append(all_dogs[id])
    else:
        print(f"❌ Missing: {id}")

# Write combined FASTA
with open(output_file, "w") as out_f:
    SeqIO.write(sequences_to_write, out_f, "fasta")

print("✅ Created alignment_input.fasta with mystery and top 3 matches.")
