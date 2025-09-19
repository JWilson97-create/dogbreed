import csv
from Bio import SeqIO

# File paths
input_fasta = "data/dog_sequences.fa"
output_fasta = "data/dog_sequences_named.fa"
mapping_file = "data/breed_mapping.csv"

# Step 1: Load mapping from CSV
id_to_breed = {}
with open(mapping_file, newline='') as csvfile:  # Open mapping CSV
    reader = csv.DictReader(csvfile)
    for row in reader:
        id_to_breed[row["accession_id"]] = row["breed"]  # Map accession_id to breed

# Step 2: Replace IDs in FASTA
updated_records = []
for record in SeqIO.parse(input_fasta, "fasta"):  # Parse input FASTA
    accession_id = record.id
    breed_name = id_to_breed.get(accession_id, f"Unknown_{accession_id}")  # Get breed or default
    record.id = breed_name.replace(" ", "_")  # Replace spaces with underscores
    record.description = ""
    updated_records.append(record)  # Clear description for cleaner output

# Step 3: Write output FASTA
with open(output_fasta, "w") as out_file:
    SeqIO.write(updated_records, out_file, "fasta")

print(f"✅ Output written to {output_fasta}")
