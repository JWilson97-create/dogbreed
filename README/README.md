🐾 Dog Breed Identifier

A Python-based bioinformatics tool that identifies dog breeds from DNA sequences and generates phylogenetic trees. This project was developed as part of my coursework and demonstrates skills in:

- Data Visualisation
- Python Software Development (modular code, CLI tools, testing)
- Sequence Alignment and Phylogenetics

---

## 🚀 Features
- 🔍 **Breed Identification**: Finds the closest matching dog breed from input DNA sequences.
- 🧬 **Sequence Comparison**: Uses pairwise alignment to calculate percent identity between sequences.
- 🌳 **Phylogenetic Tree**: Automatically generates a tree visualisation to show relationships between breeds.
- 📂 **Breed Mapping**: CSV-based breed mapping for flexibility. Automatically updates or creates a mapping file for known and unknown breeds.
- ✅ Fully **tested** with `pytest`for reliability.
- Command line interface (CLI) for easy use

---

## 🛠️ Tech Stack
- Python 3.12
- [Biopython](https://biopython.org/)
- `pytest`
- `matplotlib`

---

## 📦 Installation  

Clone the repository and install dependencies:  

```bash
git clone https://github.com/JWilson97-create/dogbreed.git
cd dogbreed
pip install -r requirements.txt



📂 Project Structure

Dog Breed/
│
├── data/                      # FASTA sequences
├── SRC/dogbreed/              # Source code
│   ├── cli.py                 # CLI entry point
│   ├── compare_sequences.py   # DNA comparison logic
│   ├── generate_phylogenetic_tree.py # Tree generation
│   └── dog_breed_identifier.py # Main module
├── tests/                     # Unit tests
├── requirements.txt           # Dependencies
├── pyproject.toml             # Project metadata
└── README.md

🙋 Author

Developed by Josh Wilson-Addo
MSc Bioinformatics Student