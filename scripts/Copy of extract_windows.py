#!/usr/bin/env python3

import sys

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
    starts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            starts.append(int(line))
    return starts


def main():
    if len(sys.argv) != 5:
        print("Usage:")
        print("  python3 extract_windows.py genome.fna protein_coding_starts.txt window_size output.fna")
        sys.exit(1)

    genome_path = sys.argv[1]
    starts_path = sys.argv[2]
    window_size = int(sys.argv[3])
    out_path = sys.argv[4]

    genome = read_genome_fasta(genome_path)
    starts = read_starts(starts_path)

    half = window_size // 2
    windows = []

    for idx, pos in enumerate(starts):
        start_i = pos - half
        end_i   = pos + half

        # skip windows that run outside the genome
        if start_i < 0 or end_i > len(genome):
            continue

        seq = genome[start_i:end_i]
        windows.append((f"start_{pos}", seq))

    # Write results as FASTA
    with open(out_path, "w") as out:
        for header, seq in windows:
            out.write(f">{header}\n{seq}\n")

    print(f"Extracted {len(windows)} windows of size {window_size}")
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
