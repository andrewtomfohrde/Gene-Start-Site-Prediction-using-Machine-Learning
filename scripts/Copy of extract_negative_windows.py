#!/usr/bin/env python3

import sys
import random

def read_genome_fasta(path):
    """Reads a FASTA genome file and returns one long string of bases."""
    seq_chunks = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                continue
            seq_chunks.append(line.upper())
    return "".join(seq_chunks)


def read_starts(path):
    """Reads genomic start positions (one per line)."""
    starts = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            starts.add(int(line))
    return starts


def main():
    if len(sys.argv) != 6:
        print("Usage:")
        print("  python3 extract_negative_windows.py "
              "genome.fna protein_coding_starts.txt window_size "
              "n_negatives output.fna")
        sys.exit(1)

    genome_path = sys.argv[1]
    starts_path = sys.argv[2]
    window_size = int(sys.argv[3])
    n_neg = int(sys.argv[4])
    out_path = sys.argv[5]

    genome = read_genome_fasta(genome_path)
    start_positions = read_starts(starts_path)

    half = window_size // 2
    L = len(genome)

    negatives = []
    tried = 0

    while len(negatives) < n_neg:
        tried += 1
        # pick a random central position that has room on both sides
        pos = random.randint(half, L - half - 1)

        # skip if this is exactly a known start
        if pos in start_positions:
            continue

        start_i = pos - half
        end_i = pos + half
        seq = genome[start_i:end_i]
        negatives.append((f"neg_{pos}", seq))

        # safety: avoid infinite loop if something weird happens
        if tried > n_neg * 50:
            break

    with open(out_path, "w") as out:
        for header, seq in negatives:
            out.write(f">{header}\n{seq}\n")

    print(f"Requested {n_neg} negatives, wrote {len(negatives)} windows of size {window_size}")
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
