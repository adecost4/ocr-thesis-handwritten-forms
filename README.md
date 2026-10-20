# Handwritten Text Recognition for Structured Forms

**Master's Thesis Research | Computer Vision • Deep Learning • Document AI**

This repository contains my Master's thesis research on **Handwritten Text Recognition (HTR) for structured documents**, particularly fixed-template forms such as banking and government forms.

The research investigates whether structural information available in fixed-template forms—such as field location, field type, expected content, and document layout—can improve handwritten text recognition compared with general-purpose HTR approaches.

> 🚧 **Active Research — 2026–2027**  
> The research methodology, experiments, and hypotheses are evolving as the thesis progresses.

---

## Research Objective

The objective of this research is to develop and evaluate a **template-aware handwritten text recognition pipeline** for extracting handwritten information from predefined fields in structured forms.

Beyond developing a functional OCR/HTR system, the thesis aims to identify and experimentally evaluate a focused research hypothesis that provides a measurable improvement over baseline approaches.

---

## Current Research Questions

Current research questions include:

- How well does pretrained TrOCR perform on offline handwritten text?
- What types of errors dominate pretrained TrOCR recognition failures?
- How do Transformer-based HTR approaches differ from CNN/RNN/CTC approaches?
- Does controlled image preprocessing improve TrOCR recognition accuracy?
- Can fixed-template information improve field-level recognition?
- Can field-specific constraints reduce recognition errors?
- Can layout and field context improve Exact Match accuracy for structured handwritten fields?

These questions are being refined through literature review, baseline experiments, systematic error analysis, and controlled experiments.

---

## Proposed Thesis Pipeline

```text
Scanned / Photographed Form
            |
            v
     Template Alignment
            |
            v
       Field Extraction
            |
            v
 Handwritten Text Recognition
            |
            v
   Field-Aware Processing
            |
            v
      Structured Output
```

The current experiments focus on establishing and understanding the **handwriting-recognition component** before introducing template and field information.

---

# Current Research Status

The project has progressed from basic TrOCR inference to a reproducible IAM handwriting-recognition baseline and systematic error analysis.

Current progression:

```text
Basic TrOCR Inference
        ↓
IAM Dataset Preparation
        ↓
CER / WER / Exact Match
        ↓
EXP002 — TrOCR IAM Baseline
        ↓
Systematic Error Analysis
        ↓
EXP003 — Controlled Preprocessing   ← CURRENT
        ↓
Template Alignment
        ↓
Field Extraction
        ↓
Field-Aware Recognition
        ↓
Structured Output
```

---

# EXP002 — Pretrained TrOCR Baseline

The first formal baseline experiment evaluates:

```text
microsoft/trocr-base-handwritten
```

on the IAM Handwriting Database without additional IAM-specific fine-tuning or image preprocessing.

After filtering IAM line annotations marked with segmentation errors, the usable writer-independent splits contained:

| Split | Usable Lines |
|---|---:|
| Training | 5,419 |
| Validation | 1,539 |
| Test | 1,480 |

The complete usable test set was evaluated.

## EXP002 Results

| Metric | Result |
|---|---:|
| Test Samples | **1,480** |
| Average CER | **3.33%** |
| Average WER | **8.63%** |
| Exact Matches | **842 / 1,480** |
| Exact Match Rate | **56.89%** |
| Non-Exact Predictions | **638** |

This result is used as the fixed pretrained TrOCR baseline for future experiments.

---

# EXP002 — Systematic Error Analysis

The 638 non-exact predictions were used as the population for systematic error analysis.

A reproducible diagnostic sample of **125 predictions** was manually reviewed:

```text
50 highest-CER failures
+
50 random non-exact failures
+
25 low-CER non-exact failures
=
125 manually reviewed predictions
```

## Error Categories

| Error Category | Count | % of Reviewed Samples |
|---|---:|---:|
| Word substitution | 72 | 57.6% |
| Character substitution | 62 | 49.6% |
| Punctuation | 24 | 19.2% |
| Spacing | 21 | 16.8% |
| Capitalization | 1 | 0.8% |

Multiple categories could be assigned to one prediction, so percentages do not sum to 100%.

### Main Observations

- Word substitutions dominated the highest-CER failures.
- Character substitutions were common across all diagnostic groups.
- Low-CER but non-exact predictions frequently contained small character or spacing differences.
- 68% of the 50 highest-CER samples were manually classified as difficult handwriting.
- Many recognition failures occurred on images that appeared visually good.
- A low aggregate CER does not necessarily imply high Exact Match accuracy.

This distinction is particularly important for structured fields such as:

```text
Student ID
Account Number
Date
Phone Number
Name
```

where even a single incorrect character may make the extracted value incorrect.

> The 125 samples form a targeted diagnostic sample and are not a representative random sample of all 638 failures.

---

# EXP003 — Controlled Image Preprocessing

EXP003 is currently in progress.

## Research Question

> **Does controlled image preprocessing improve pretrained TrOCR recognition accuracy on IAM handwriting?**

Candidate preprocessing conditions include:

```text
Original
Grayscale
Otsu thresholding
CLAHE contrast enhancement
Denoising
Deskewing
```

Preprocessing approaches will first be developed and compared using the **IAM validation split**.

A reproducible development subset will be used for initial experiments before evaluating promising methods on the full validation set.

The selected method will then be evaluated once on the held-out IAM test set.

The final comparison will use the fixed EXP002 baseline:

```text
CER         3.33%
WER         8.63%
Exact Match 56.89%
```

---

# Literature Review

## Paper 01 — TrOCR

**TrOCR: Transformer-Based Optical Character Recognition with Pre-trained Models**

Key architecture:

```text
Image
 ↓
Transformer Image Encoder
 ↓
Autoregressive Transformer Decoder
 ↓
Text
```

Provides the pretrained recognition architecture used for EXP002.

---

## Paper 02 — CRNN

**An End-to-End Trainable Neural Network for Image-based Sequence Recognition and Its Application to Scene Text Recognition**

Key architecture:

```text
CNN
 ↓
BiLSTM
 ↓
CTC
 ↓
Text
```

Provides an important CNN/RNN/CTC baseline architecture for sequence recognition.

---

## Paper 03 — FUNSD

**FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents**

Introduces document-understanding concepts beyond OCR:

- spatial layout
- semantic entities
- question-answer relationships
- entity linking
- noisy scanned forms

FUNSD is relevant to the structured-form component of the thesis.

---

## Paper 04 — HTR-VT

**HTR-VT: Handwritten Text Recognition with Vision Transformer**

Key architecture:

```text
Handwritten Image
        ↓
CNN / ResNet-18
        ↓
Transformer Encoder
        ↓
CTC
        ↓
Text
```

Important concepts studied:

- data-efficient Transformer HTR
- CNN local feature extraction
- Transformer contextual modeling
- span feature masking
- Sharpness-Aware Minimization (SAM)
- CTC decoding
- encoder-only Transformer recognition

HTR-VT provides an important alternative to TrOCR because it demonstrates that Transformer-based HTR does not necessarily require an autoregressive Transformer decoder or large-scale external pretraining.

---

# Architecture Progression

The literature currently provides three useful recognition paradigms:

```text
CRNN
CNN → BiLSTM → CTC
        │
        ▼
HTR-VT
CNN → Transformer Encoder → CTC
        │
        ▼
TrOCR
Transformer Encoder → Transformer Decoder
```

FUNSD extends the research beyond recognition toward:

```text
OCR
 ↓
Layout
 ↓
Entities
 ↓
Relationships
 ↓
Form Understanding
```

Together, these papers support the progression toward structured handwritten-form recognition.

---

# Evaluation Metrics

Current experiments use:

### Character Error Rate

```text
CER
```

Measures character-level transcription errors.

### Word Error Rate

```text
WER
```

Measures word-level transcription errors.

### Exact Match / Field Accuracy

```text
1 = complete prediction matches ground truth
0 = mismatch
```

Exact Match is especially important for structured forms because a prediction can have low CER while still containing an incorrect field value.

---

# Technologies

## Currently Using

- Python
- PyTorch
- Hugging Face Transformers
- TrOCR
- OpenCV
- Pandas
- NumPy
- Matplotlib
- JiWER
- Pillow
- Jupyter Notebook
- VS Code
- Git / GitHub

## Research Components

- IAM Handwriting Database
- CER / WER / Exact Match
- systematic OCR error analysis
- image preprocessing
- Transformer-based HTR
- CTC-based HTR
- document understanding

## Planned

- Template alignment
- Field extraction
- Structured-form dataset experiments
- Field-aware recognition
- Layout-aware recognition
- Model adaptation / fine-tuning

---

# Research Progress

## Completed

- [x] Thesis research direction established
- [x] Research environment setup
- [x] GitHub research repository
- [x] Pretrained TrOCR inference pipeline
- [x] CSV-based handwriting loading
- [x] IAM dataset study
- [x] IAM data preparation
- [x] IAM manifest generation
- [x] Writer-independent IAM split generation
- [x] CER implementation
- [x] WER implementation
- [x] Exact Match implementation
- [x] Metric testing
- [x] EXP002 N=20 exploratory evaluation
- [x] EXP002 N=50 exploratory evaluation
- [x] EXP002 N=100 exploratory evaluation
- [x] EXP002 full IAM test-set evaluation
- [x] EXP002 systematic error analysis
- [x] 125-sample manual error review
- [x] Error-category tables and figures
- [x] TrOCR paper review
- [x] CRNN paper review
- [x] FUNSD paper review
- [x] HTR-VT paper review

## Currently Working On

- [ ] EXP003 controlled preprocessing
- [ ] OpenCV preprocessing experiments
- [ ] Validation-set preprocessing comparison
- [ ] Continued literature review

## Upcoming

- [ ] Complete EXP003
- [ ] Template/document alignment
- [ ] Field extraction pipeline
- [ ] Structured handwritten-form experiments
- [ ] Field-aware recognition
- [ ] Layout-aware recognition
- [ ] IAM-specific model adaptation / fine-tuning
- [ ] Candidate research hypothesis evaluation
- [ ] Final thesis contribution

---

# Repository Structure

```text
ocr-thesis-handwritten-forms/
│
├── papers/
│   ├── 01_trocr.md
│   ├── 02_crnn.md
│   ├── 03_funsd.md
│   └── 04_htr_vt.md
│
├── docs/
│
├── notebooks/
│
├── trocr_beginner_project/
│   ├── data/
│   ├── notebooks/
│   ├── experiments/
│   ├── outputs/
│   ├── results/
│   ├── src/
│   └── tests/
│
└── README.md
```

> Large research datasets and copyrighted papers are not stored directly in this repository.

---

# Experiment Tracking

Each experiment is documented with:

- Research question / hypothesis
- Dataset
- Model and configuration
- Data preparation
- Preprocessing
- Evaluation protocol
- CER / WER / Exact Match
- Results
- Error analysis
- Limitations
- Conclusion
- Next experiment

Current experiment progression:

```text
EXP002
Pretrained TrOCR on IAM
        ↓
Systematic Error Analysis
        ↓
EXP003
Controlled Image Preprocessing
        ↓
Future
Template Alignment / Field Extraction
```

---

# Research Hypothesis Development

The final thesis hypothesis has not yet been fixed.

Current candidate directions include:

1. **Field-aware recognition** — using field type, expected character set, expected format, or other field constraints to reduce recognition errors.

2. **Template-aware recognition** — exploiting known fixed-form structure during field extraction and recognition.

3. **Preprocessing and robustness** — measuring whether targeted preprocessing improves recognition under image degradation.

4. **Model adaptation** — adapting pretrained handwriting models to structured-form handwriting.

5. **Recognition architecture** — investigating differences between autoregressive recognition and encoder+CTC approaches.

The final hypothesis will be selected based on literature review and controlled experimental evidence.

---

# Current Focus

**October 2026**

> Complete EXP003 controlled preprocessing, preserve EXP002 as the fixed recognition baseline, and begin moving from general handwritten-line recognition toward template alignment and structured field extraction.

---

# Research Roadmap

| Period | Research Focus |
|---|---|
| Aug–Sep 2026 | HTR foundations, TrOCR, CRNN, IAM |
| Oct 2026 | IAM baseline, systematic error analysis, preprocessing |
| Oct–Nov 2026 | Template alignment and field extraction |
| Nov–Dec 2026 | Structured-form experiments and hypothesis development |
| Jan–Mar 2027 | Main experiments and evaluation |
| Mar–May 2027 | Thesis writing, publication, demo and defense |

---

# Dataset Reference

## IAM Handwriting Database

The IAM Handwriting Database is used for offline handwritten-text recognition experiments.

The dataset contains scanned English handwriting with form-, line-, and word-level annotations.

Official dataset:

https://fki.tic.heia-fr.ch/databases/iam-handwriting-database

The IAM dataset itself is **not distributed through this repository**.

Users must obtain IAM separately and comply with the dataset's license and usage requirements.

---

# Reproducibility

The repository tracks:

- source code
- experiment notebooks
- experiment definitions
- metric implementations
- small result files
- error-analysis annotations
- figures
- literature notes

Large research datasets such as IAM are intentionally excluded from Git.

Local IAM manifests can be regenerated using the provided preparation scripts.

---

# Disclaimer

This repository contains ongoing academic research as part of a Master's thesis.

Results, hypotheses, and conclusions should be considered preliminary until the research is completed.