# Machine Learning for Translation Start-Site Prediction

This project investigates how genome structure affects the ability of machine learning models to predict gene translation start sites.

We compare performance across **human (eukaryotic)** and **bacterial (prokaryotic)** genomes using both traditional machine learning models and deep learning approaches.

---

## Project Overview

Correctly identifying gene start sites is important for genome annotation and understanding protein synthesis.

This project explores:

- Whether start-site prediction is a learnable sequence classification problem
- How genome complexity impacts prediction performance
- Differences between human and bacterial genomic signals

We trained multiple models on extracted DNA sequence windows centered around annotated start codons.

---

## Datasets

### Human Genome (RefSeq GRCh38)

- Source: NCBI RefSeq
- Files used:
  - `*_feature_table.txt` → used to obtain protein-coding gene start coordinates
  - `*_genomic.fna` → raw DNA sequence
- Window size: **300 bp**
- Balanced dataset created using positive gene starts and sampled negative regions

### Bacterial Genome (E. coli MG1655)

- Window size: **401 bp**
- Improved negative sampling:
  - Genome scanned for ATG / GTG / TTG codons
  - Annotated starts removed
  - Only valid upstream context retained
- Final dataset:
  - **4340 positive**
  - **4340 negative**

---

## Models Tested

Human Genome:

- Logistic Regression (one-hot encoding)
- Random Forest (k-mer frequency features)
- XGBoost
- Multilayer Perceptron
- 1D Convolutional Neural Network

Bacterial Genome:

- Logistic Regression
- Random Forest
- 1D Convolutional Neural Network

---

## Key Results

### Human Genome

| Model | Test Accuracy |
|------|---------------|
| Logistic Regression | 56.5% |
| Random Forest | 60.4% |
| XGBoost | 58.8% |
| MLP | 57.5% |
| CNN | 57.1% |

Prediction performance remained limited due to:

- weak local motifs
- alternative start sites
- annotation uncertainty
- complex gene structure

---

### Bacterial Genome

| Model | Test Accuracy |
|------|---------------|
| Logistic Regression | 88.9% |
| Random Forest | 88.0% |
| CNN | **95–96%** |

CNN models likely learned conserved signals such as the **Shine-Dalgarno motif** and fixed spacing upstream of start codons.

---

## Conclusion

Translation start-site prediction is significantly easier in bacterial genomes due to strong conserved sequence signals and compact gene structure.

Human gene start prediction is fundamentally constrained by biological complexity rather than model capacity.

---

