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

EXP003 investigates whether conventional image preprocessing improves recognition performance from pretrained TrOCR.

## Research Question

> **Does controlled image preprocessing improve pretrained TrOCR recognition accuracy on IAM handwriting?**

The experiment follows a validation-first protocol so that preprocessing decisions are not repeatedly optimized against the held-out IAM test set.

```text
IAM Validation Split
        ↓
Reproducible DEV100
        ↓
Visual Preprocessing Analysis
        ↓
Original Control
        ↓
Controlled Preprocessing Comparison
        ↓
Paired Sample-Level Analysis
        ↓
Full Validation Evaluation
        ↓
Freeze Preprocessing Decision
        ↓
Held-Out Test Evaluation
```

---

## DEV100 Experimental Setup

A reproducible development subset was selected from the IAM validation split:

```text
N = 100
random_state = 42
```

The following conditions were evaluated on exactly the same samples:

```text
Original
Grayscale
Otsu Thresholding
CLAHE Contrast Enhancement
Denoising
```

The TrOCR model, processor, decoding procedure, metrics, and sample IDs remained unchanged across conditions.

---

## Visual Preprocessing Analysis

Ten DEV100 samples were visually inspected before OCR evaluation.

General observations:

- Original IAM images were generally clean and readable.
- Grayscale produced almost no visible change.
- Otsu produced the strongest foreground/background separation.
- CLAHE sometimes strengthened faint handwriting but also amplified background variations.
- Denoising produced relatively subtle changes.

No preprocessing method was selected based only on visual appearance.

---

## DEV100 Results

| Condition | CER | WER | Exact Match |
|---|---:|---:|---:|
| Original | **2.61%** | **7.27%** | **62%** |
| Grayscale | 2.61% | 7.27% | 62% |
| **Otsu Threshold** | **2.49%** | **6.94%** | **68%** |
| CLAHE | 3.08% | 8.62% | 59% |
| Denoising | 2.79% | 7.55% | 62% |

Otsu thresholding was the only tested condition to improve CER, WER, and Exact Match simultaneously.

---

## Paired Sample-Level Analysis

Aggregate metrics were followed by a paired comparison against the Original prediction for every DEV100 sample.

| Condition | Improved CER | Unchanged | Worsened | Recovered Exact | Lost Exact | Net Exact |
|---|---:|---:|---:|---:|---:|---:|
| Grayscale | 0 | 100 | 0 | 0 | 0 | 0 |
| **Otsu Threshold** | **13** | 77 | 10 | **8** | 2 | **+6** |
| CLAHE | 5 | 85 | 10 | 2 | 5 | -3 |
| Denoising | 5 | 92 | 3 | 1 | 1 | 0 |

For Otsu:

```text
Original Exact:       62
Recovered Exact:       8
Lost Exact:            2
Final Otsu Exact:      68

Net Exact Gain:        +6
```

The paired analysis shows that Otsu's improvement was not only an aggregate metric effect.

Eight previously incorrect predictions became exactly correct, while two previously correct predictions became incorrect.

However, Otsu also worsened CER for 10 samples.

Therefore, the current conclusion is:

> **Otsu thresholding is a promising preprocessing candidate, but it is not universally beneficial and requires evaluation on the complete IAM validation split.**

---

## Current EXP003 Decision

| Method | Current Decision |
|---|---|
| Grayscale | Do not advance |
| **Otsu Threshold** | **Advance to full validation** |
| CLAHE | Do not advance under current configuration |
| Denoising | Do not advance under current configuration |

The next stage will compare:

```text
Complete IAM Validation Split
N = 1,539

Original
   vs.
Otsu Thresholding
```

The held-out IAM test set remains untouched during preprocessing selection.

The fixed EXP002 test baseline remains:

```text
CER         3.33%
WER         8.63%
Exact Match 56.89%
```

EXP003 is therefore still **in progress**.

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
- [x] IAM dataset study and preparation
- [x] IAM writer-independent split generation
- [x] CER / WER / Exact Match implementation
- [x] EXP002 exploratory N=20 / N=50 / N=100 evaluations
- [x] EXP002 full IAM test-set evaluation
- [x] EXP002 systematic error analysis
- [x] 125-sample manual error review
- [x] Error-category tables and figures
- [x] TrOCR paper review
- [x] CRNN paper review
- [x] FUNSD paper review
- [x] HTR-VT paper review
- [x] EXP003 DEV100 dataset preparation
- [x] EXP003 visual preprocessing study
- [x] EXP003 Original DEV100 baseline
- [x] Grayscale DEV100 evaluation
- [x] Otsu DEV100 evaluation
- [x] CLAHE DEV100 evaluation
- [x] Denoising DEV100 evaluation
- [x] EXP003 aggregate preprocessing comparison
- [x] EXP003 paired sample-level analysis
- [x] Otsu Exact Match transition analysis

## Currently Working On

- [ ] Inspect representative Otsu recoveries and regressions
- [ ] Original vs Otsu full IAM validation evaluation
- [ ] EXP003 full-validation paired analysis
- [ ] Finalize EXP003 preprocessing decision
- [ ] Continue EXP003 documentation

## Upcoming

- [ ] Evaluate frozen EXP003 configuration on held-out IAM test set
- [ ] Complete EXP003
- [ ] Template/document alignment
- [ ] Structured field extraction pipeline
- [ ] Structured handwritten-form experiments
- [ ] Field-aware recognition
- [ ] Field-specific validation and constraints
- [ ] Layout-aware recognition
- [ ] Candidate thesis hypothesis evaluation
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

**November 2026**

> Complete EXP003 by validating the promising Otsu preprocessing result on the complete IAM validation split, then transition from general handwritten-line recognition toward template alignment, structured field extraction, and field-aware recognition.

The current research progression is:

```text
EXP002
General HTR Baseline
        ✓
        ↓
Systematic Error Analysis
        ✓
        ↓
EXP003
Controlled Preprocessing
        ← CURRENT
        ↓
Template Alignment
        ↓
Field Extraction
        ↓
Field-Aware Recognition
        ↓
Structured Output
```

Following feedback from the thesis midterm review, the remaining work will increasingly focus on clearly identifying and evaluating the thesis contribution beyond the use of an existing HTR model.

The baseline and preprocessing experiments provide the experimental foundation for that contribution.

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