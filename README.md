🧬 Machine Learning for Translation Start-Site Prediction
Project Overview

This project investigates how genome structure affects the ability of machine learning models to predict gene translation start sites.

We compare model performance across:

Human genome (eukaryotic — complex structure)

Bacterial genome (prokaryotic — strong sequence signals)

The goal is to understand:

Whether start-site prediction is a learnable sequence classification task

How biological complexity impacts achievable prediction accuracy

How traditional ML models compare to deep learning approaches

📊 Datasets
Human Genome (RefSeq GRCh38)

Source: NCBI RefSeq

Files used:

feature_table.txt → gene start coordinates
genomic.fna → raw DNA sequence

Processing steps:

Extracted 300 bp DNA windows centered on annotated start sites (positive samples)

Sampled genomic regions away from annotated starts to create negative samples

Constructed a balanced dataset (~46k windows)

Bacterial Genome (E. coli MG1655)

Processing steps:

Extracted 401 bp windows centered on ATG / GTG / TTG start codons

Removed annotated starts for negative sampling

Retained only windows with valid upstream context

Final dataset:

4340 positive samples
4340 negative samples
🤖 Models Tested

We evaluated multiple machine learning approaches:

Baseline Models

Logistic Regression (one-hot encoding)

Logistic Regression (k-mer features)

Tree-Based Models

Random Forest

XGBoost

Neural Models

Multilayer Perceptron (MLP)

1D Convolutional Neural Network (CNN)

📈 Key Results
Human Genome
Model	Test Accuracy
Logistic Regression	~56.5%
Random Forest	~60.4%
XGBoost	~58.8%
CNN	~57.1%

Results indicate:

Weak sequence signals near start sites

Model complexity provides limited performance gains

Bacterial Genome
Model	Test Accuracy
Logistic Regression	~88.9%
Random Forest	~88.0%
CNN	95–96%

CNN achieved:

High precision and recall

Minimal overfitting

Learned Shine-Dalgarno motif spacing patterns

🧪 How to Run the Pipeline
1. Extract gene start coordinates
python extract_protein_coding_starts.py feature_table.txt protein_coding_starts.txt
2. Generate positive DNA windows
python extract_windows.py genome.fna protein_coding_starts.txt 300 positive_windows.fna
3. Generate negative DNA windows
python extract_negative_windows.py genome.fna protein_coding_starts.txt 300 negative_windows.fna
4. Build training dataset
python make_training_dataset.py positive_windows.fna negative_windows.fna training_dataset.csv
5. Train baseline model
python train_logreg_baseline.py training_dataset.csv
📁 Project Structure
project/

data/
    genome_raw/
    windows/
    training_dataset.csv

scripts/
    extract_windows.py
    extract_negative_windows.py
    make_training_dataset.py
    train_logreg_baseline.py

models/
    cnn_start_predictor.h5

notebooks/
    model_testing.ipynb

results/
    human_results.txt
    bacterial_results.txt
🧠 Conclusion

Start-site prediction is strongly influenced by genome structure.

Bacterial genomes contain strong conserved motifs → highly learnable

Human genomes contain weak local signals and annotation uncertainty → lower achievable accuracy

This suggests biological variability, not model capacity, is the main limiting factor.
