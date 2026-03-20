#!/usr/bin/env python3
"""
extract_protein_coding_starts.py

Simple helper script for the final project.

Given a RefSeq feature_table.txt file, this script:
  - filters for rows where column 2 == "protein_coding"
  - extracts the gene start coordinate (column 7)
  - optionally writes all start positions to a text file
  - prints how many protein-coding starts were found

Usage:
    python3 extract_protein_coding_starts.py \
        GCF_000001405.40_GRCh38.p14_feature_table.txt \
        protein_coding_starts.txt

If you don't want to save to a file, you can omit the second argument:
    python3 extract_protein_coding_starts.py GCF_000001405.40_GRCh38.p14_feature_table.txt
"""

import sys

def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 extract_protein_coding_starts.py feature_table.txt [output_starts.txt]")
        sys.exit(1)

    feature_table_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) == 3 else None

    starts = []

    # Open the feature table and scan line by line
    with open(feature_table_path) as f:
        for line in f:
            # Skip empty lines
            if not line.strip():
                continue

            parts = line.rstrip("\n").split("\t")

            # Make sure the line has enough columns
            if len(parts) < 8:
                continue

            # Column 2: feature type (e.g., "gene", "CDS", "protein_coding")
            feature_type = parts[1]

            # We only care about protein_coding rows
            if feature_type == "protein_coding":
                # Column 8 (0-based index 7) is the start coordinate
                try:
                    start = int(parts[7])
                    starts.append(start)
                except ValueError:
                    # If the coordinate is malformed, just skip that line
                    continue

    print("Found protein coding gene starts:", len(starts))

    # If user provided an output file, write one start per line
    if out_path is not None:
        with open(out_path, "w") as out_f:
            for pos in starts:
                out_f.write(f"{pos}\n")
        print(f"Wrote start positions to: {out_path}")


if __name__ == "__main__":
    main()
