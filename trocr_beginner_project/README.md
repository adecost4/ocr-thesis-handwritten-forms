# TrOCR Beginner Project

A beginner-friendly research project for learning and evaluating **Handwritten Text Recognition (HTR)** using Microsoft's **TrOCR** model.

This project is part of my Master's thesis research on **Transformer-based OCR for structured handwritten forms**.

---

## Project Goals

This project explores the progression from basic OCR inference toward reproducible handwritten-text recognition experiments and, eventually, structured handwritten-form understanding.

The project currently demonstrates:

- Running inference with a pretrained TrOCR model
- Loading handwriting images using CSV manifests
- Preparing the IAM Handwriting Database
- Evaluating OCR using CER, WER, and Exact Match
- Running reproducible OCR experiments
- Performing error analysis on model predictions
- Preparing for IAM-specific TrOCR fine-tuning
- Studying OCR and document-understanding literature

---

## Project Structure

```text
trocr_beginner_project/
│
├── data/
│   ├── sample/
│   │   ├── images/
│   │   └── sample.csv
│   │
│   └── iam/
│       ├── ascii/
│       ├── lines/
│       ├── xml/
│       ├── splits/
│       ├── iam_sample.csv
│       ├── train.csv
│       ├── validation.csv
│       └── test.csv
│
├── notebooks/
│   ├── 01_trocr_beginner.ipynb
│   └── 02_iam_evaluation.ipynb
│
├── experiments/
│   └── EXP002_iam_trocr_baseline.md
│
├── outputs/
│   └── exp002/
│       ├── n20/
│       ├── n50/
│       ├── n100/
│       └── iam_test/
│
├── src/
│   ├── __init__.py
│   ├── create_iam_sample.py
│   ├── create_iam_splits.py
│   ├── data_utils.py
│   ├── dataset.py
│   ├── evaluate.py
│   ├── metrics.py
│   └── train.py
│
├── tests/
│   ├── __init__.py
│   └── test_metrics.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

> The IAM dataset is stored locally and is excluded from Git using `.gitignore`.

---

## Prerequisites

- Python 3.9 or newer
- Python 3.11 recommended
- pip
- Git
- VS Code, Jupyter Notebook, or JupyterLab

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>/trocr_beginner_project
```

### Create a Virtual Environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Notebook 01 — TrOCR Beginner

Open:

```text
notebooks/01_trocr_beginner.ipynb
```

This notebook introduces the basic TrOCR inference pipeline:

```text
Handwritten Image
        ↓
TrOCR Processor
        ↓
Pretrained TrOCR
        ↓
Recognized Text
```

It demonstrates:

- loading sample images
- loading pretrained TrOCR
- running inference
- generating text predictions
- working with CSV manifests

---

## IAM Handwriting Database

The IAM Handwriting Database is used as the primary handwriting-recognition dataset.

The full IAM dataset is **not included in this Git repository**.

After downloading IAM locally, the expected structure is:

```text
data/iam/
├── ascii/
├── lines/
├── xml/
└── splits/
```

The dataset is converted into CSV manifests for experimentation.

### Generate IAM Manifest

Run:

```bash
python3 -m src.create_iam_sample
```

This generates:

```text
data/iam/iam_sample.csv
```

The manifest contains:

```text
id
image
text
```

where:

- `id` identifies the IAM text line
- `image` points to the corresponding line image
- `text` contains the ground-truth transcription

---

## IAM Dataset Splits

For reproducible evaluation and future fine-tuning, IAM is separated into writer-independent training, validation, and test sets.

The target files are:

```text
data/iam/train.csv
data/iam/validation.csv
data/iam/test.csv
```

Generate them using:

```bash
python3 -m src.create_iam_splits
```

These files are generated locally and are not committed to GitHub with the IAM dataset.

---

## Notebook 02 — IAM Evaluation

Open:

```text
notebooks/02_iam_evaluation.ipynb
```

This notebook evaluates:

```text
microsoft/trocr-base-handwritten
```

on IAM handwritten text-line images.

The evaluation pipeline is:

```text
IAM Line Image
        ↓
TrOCR Processor
        ↓
Pretrained TrOCR
        ↓
Text Prediction
        ↓
Ground Truth Comparison
        ↓
CER / WER / Exact Match
```

No additional IAM-specific fine-tuning is performed in the baseline experiment.

---

## Evaluation Metrics

### Character Error Rate (CER)

Measures character-level transcription errors.

Lower is better.

```text
CER = 0
```

indicates a perfect character-level prediction.

### Word Error Rate (WER)

Measures word-level transcription errors.

Lower is better.

```text
WER = 0
```

indicates a perfect word-level prediction.

### Exact Match

Measures whether the complete prediction exactly matches the ground truth.

```text
1 = exact match
0 = mismatch
```

Exact Match is particularly relevant for structured forms where fields such as IDs, dates, names, and numerical values may require completely correct transcription.

---

## Running the Metric Tests

Run:

```bash
python3 -m tests.test_metrics
```

Example:

```text
Reference : hello world
Prediction: hallo world

CER : 0.0909
WER : 0.5
Exact Match : 0
```

---

# Experiments

## EXP002 — Pretrained TrOCR on IAM

EXP002 evaluates:

```text
microsoft/trocr-base-handwritten
```

on IAM handwritten text lines without additional fine-tuning.

The experiment began with progressively larger exploratory subsets:

```text
N=20
  ↓
N=50
  ↓
N=100
```

### Exploratory Results

| Samples | Average CER | Average WER | Exact Match |
|---:|---:|---:|---:|
| 20 | 2.39% | 5.99% | 75% |
| 50 | 1.08% | 2.81% | 86% |
| 100 | 1.15% | 3.68% | 81% |

The N=50 and N=100 CER values were relatively similar, while the smaller N=20 evaluation was more sensitive to individual recognition errors.

These results are **exploratory pipeline-validation results**.

They use the first N usable entries in the generated IAM manifest and should **not be interpreted as official IAM benchmark results**.

---

## EXP002 — Next Stage

The exploratory evaluation is complete:

```text
N=20   ✓
N=50   ✓
N=100  ✓
```

The next stage evaluates pretrained TrOCR on an established writer-independent IAM test split.

```text
IAM
│
├── train.csv
├── validation.csv
└── test.csv
        │
        ▼
Pretrained TrOCR
        │
        ▼
All Valid Test Lines
        │
        ├── CER
        ├── WER
        └── Exact Match
```

The resulting test-set metrics will become the final pretrained baseline for EXP002.

Detailed experimental documentation is available in:

```text
experiments/EXP002_iam_trocr_baseline.md
```

---

## Experiment Outputs

Experiment results are stored separately to preserve each run.

```text
outputs/
└── exp002/
    ├── n20/
    │   ├── predictions.csv
    │   ├── best_predictions.csv
    │   ├── worst_predictions.csv
    │   └── summary.json
    │
    ├── n50/
    │   └── ...
    │
    ├── n100/
    │   └── ...
    │
    └── iam_test/
        └── ...
```

This prevents later experiments from overwriting earlier results.

---

## Current Progress

### Completed

- Pretrained TrOCR inference
- CSV-based image loading
- CER implementation
- WER implementation
- Exact Match implementation
- OCR metrics testing
- IAM dataset study
- IAM data preparation
- IAM CSV manifest generation
- TrOCR IAM evaluation pipeline
- EXP002 N=20 evaluation
- EXP002 N=50 evaluation
- EXP002 N=100 evaluation
- Initial OCR error analysis
- TrOCR literature review
- CRNN literature review
- FUNSD literature review

### In Progress

- IAM writer-independent split preparation
- Full IAM test-set evaluation for EXP002

### Next Steps

- Complete the EXP002 IAM test-set baseline
- Fine-tune TrOCR using IAM training data
- Compare pretrained and IAM-fine-tuned TrOCR
- Investigate structured handwritten forms
- Explore layout-aware recognition
- Explore field-aware recognition
- Investigate template information

---

## Research Progression

The project currently follows this progression:

```text
Basic TrOCR Inference
        │
        ▼
OCR Evaluation Metrics
        │
        ▼
IAM Dataset Preparation
        │
        ▼
Pretrained TrOCR Baseline
        │
        ▼
Writer-Independent IAM Evaluation
        │
        ▼
IAM Fine-Tuning
        │
        ▼
Structured Handwritten Forms
        │
        ▼
Layout + Field Context
        │
        ▼
Structured Output
```

---

## Thesis Motivation

Standard handwritten text recognition asks:

> What text is written in this image?

The final thesis problem goes further and considers structured handwritten forms.

A future system may need to perform:

```text
Structured Form
       ↓
Text / Field Detection
       ↓
Handwriting Recognition
       ↓
Spatial Layout Understanding
       ↓
Field Classification
       ↓
Relationship Understanding
       ↓
Structured Output
```

This project therefore combines concepts from:

- Handwritten Text Recognition
- Transformer-based OCR
- Document Understanding
- Form Understanding
- Layout Analysis
- Structured Information Extraction

---

## Literature Review

### Paper 01 — TrOCR

**TrOCR: Transformer-Based Optical Character Recognition with Pre-trained Models**

Introduces an end-to-end Transformer-based OCR architecture using a pretrained image Transformer encoder and text Transformer decoder.

---

### Paper 02 — CRNN

**An End-to-End Trainable Neural Network for Image-based Sequence Recognition and Its Application to Scene Text Recognition**

Introduces the classic:

```text
CNN → BiLSTM → CTC
```

architecture for image-based sequence recognition.

---

### Paper 03 — FUNSD

**FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents**

Introduces form understanding beyond OCR, including:

- spatial layout
- semantic entities
- question-answer relationships
- entity linking
- noisy scanned documents

Together, these papers provide the progression:

```text
CRNN
CNN + RNN + CTC
        ↓
TrOCR
Transformer OCR
        ↓
FUNSD
Form Understanding
        ↓
Structured Handwritten Forms
```

---

## Datasets

### IAM Handwriting Database

Used for:

- offline handwritten text recognition
- line-level OCR evaluation
- future TrOCR fine-tuning

### FUNSD

Studied for:

- form understanding
- spatial layout
- semantic entities
- entity relationships

IAM and FUNSD address complementary parts of the thesis problem:

```text
IAM
 │
 └── Handwriting Recognition
             │
             ▼
        Thesis Problem
             ▲
             │
FUNSD
 │
 └── Form Understanding
```

---

## Reproducibility

The repository tracks:

- source code
- notebooks
- experiment definitions
- evaluation metrics
- small experiment result files

Large datasets such as IAM are intentionally excluded from Git.

The dataset can be downloaded separately and the local manifests regenerated using the provided preparation scripts.

---

## License

This repository is intended for educational and research purposes.

External datasets and pretrained models remain subject to their respective licenses and terms of use.

## Dataset Reference

### IAM Handwriting Database

The IAM Handwriting Database is used for offline handwritten text recognition experiments in this project.

The dataset contains scanned handwritten English documents with form-, line-, and word-level annotations.

Official dataset:

https://fki.tic.heia-fr.ch/databases/iam-handwriting-database

If you use the IAM dataset, please refer to the citation and usage requirements provided by the dataset authors on the official IAM website.

> The IAM dataset itself is not distributed through this repository.  
> Users must obtain the dataset separately and comply with its license and usage terms.