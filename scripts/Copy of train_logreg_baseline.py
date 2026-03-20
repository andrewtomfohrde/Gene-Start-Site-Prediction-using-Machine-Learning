#!/usr/bin/env python3
"""
train_logreg_baseline.py

Train a simple logistic regression classifier to distinguish
true start windows (label=1) from negative windows (label=0).

Usage:
    python3 train_logreg_baseline.py training_dataset.csv
"""

import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


def one_hot_encode_sequence(seq: str) -> np.ndarray:
    """
    One-hot encode a DNA sequence.

    For each position we use 4 channels: A, C, G, T.
    Any other base (N, etc.) becomes all zeros.
    Output shape: (len(seq) * 4,)
    """
    mapping = {
        "A": np.array([1, 0, 0, 0], dtype=np.float32),
        "C": np.array([0, 1, 0, 0], dtype=np.float32),
        "G": np.array([0, 0, 1, 0], dtype=np.float32),
        "T": np.array([0, 0, 0, 1], dtype=np.float32),
    }
    seq = seq.upper()
    vec = np.zeros((len(seq), 4), dtype=np.float32)
    for i, base in enumerate(seq):
        if base in mapping:
            vec[i] = mapping[base]
        # else leave that row as all zeros
    return vec.reshape(-1)  # flatten to 1D


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 train_logreg_baseline.py training_dataset.csv")
        sys.exit(1)

    csv_path = sys.argv[1]

    print(f"Loading dataset from {csv_path} ...")
    df = pd.read_csv(csv_path)

    sequences = df["sequence"].tolist()
    labels = df["label"].to_numpy(dtype=np.int64)

    # All windows should be same length (e.g., 100)
    window_len = len(sequences[0])
    print(f"Number of examples: {len(sequences)}")
    print(f"Window length: {window_len}")

    # --- One-hot encode all sequences ---
    print("One-hot encoding sequences (this may take a moment)...")
    X = np.vstack([one_hot_encode_sequence(s) for s in sequences])
    y = labels

    print(f"Feature matrix shape: {X.shape}")  # (n_samples, 4 * window_len)

    # --- Train/test split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # --- Train logistic regression ---
    print("Training logistic regression model...")
    clf = LogisticRegression(
        max_iter=1000,
        n_jobs=-1,
        solver="lbfgs"
    )
    clf.fit(X_train, y_train)

    # --- Evaluate ---
    y_train_pred = clf.predict(X_train)
    y_test_pred = clf.predict(X_test)

    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)

    print(f"\nTrain accuracy: {train_acc:.3f}")
    print(f"Test accuracy : {test_acc:.3f}\n")

    print("Classification report on test set:")
    print(classification_report(y_test, y_test_pred, digits=3))


if __name__ == "__main__":
    main()
