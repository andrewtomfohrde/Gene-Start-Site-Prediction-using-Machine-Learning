#!/usr/bin/env python3

import sys
import csv

def read_fasta(path):
    """Returns a list of sequences from a FASTA file."""
    seqs = []
    cur = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if cur:
                    seqs.append("".join(cur))
                    cur = []
            else:
                cur.append(line)
        if cur:
            seqs.append("".join(cur))
    return seqs

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 make_training_dataset.py positive_windows.fna negative_windows.fna output.csv")
        sys.exit(1)

    pos_path = sys.argv[1]
    neg_path = sys.argv[2]
    out_csv = sys.argv[3]

    pos_seqs = read_fasta(pos_path)
    neg_seqs = read_fasta(neg_path)

    print(f"Loaded {len(pos_seqs)} positives and {len(neg_seqs)} negatives")

    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sequence", "label"])

        for s in pos_seqs:
            w.writerow([s, 1])

        for s in neg_seqs:
            w.writerow([s, 0])

    print(f"Wrote dataset to: {out_csv}")

if __name__ == "__main__":
    main()
