# Experiments

## EXP002 — Pretrained TrOCR on IAM

EXP002 evaluates:

```text
microsoft/trocr-base-handwritten
```

on IAM handwritten text lines without additional IAM-specific fine-tuning or image preprocessing.

The experiment progressed through:

```text
N=20
  ↓
N=50
  ↓
N=100
  ↓
Writer-independent IAM test evaluation
```

---

### Exploratory Results

| Samples | Average CER | Average WER | Exact Match |
|---:|---:|---:|---:|
| 20 | 2.39% | 5.99% | 75% |
| 50 | 1.08% | 2.81% | 86% |
| 100 | 1.15% | 3.68% | 81% |

These runs were used to validate the evaluation pipeline.

They should not be interpreted as the final IAM baseline because they use convenience subsets of the IAM manifest.

---

## EXP002 — Formal IAM Test Evaluation

After validating the pipeline, the corrected IAM manifest and writer-independent split definitions were used.

The IAM line annotations contained:

```text
Total annotations: 13,353
status=ok:          11,344
status=err:          2,009
Missing images:          0
```

Only samples marked:

```text
status=ok
```

were retained.

The generated usable splits contained:

| Split | Defined | Usable |
|---|---:|---:|
| Train | 6,161 | 5,419 |
| Validation | 1,840 | 1,539 |
| Test | 1,861 | 1,480 |

All excluded split IDs were verified to correspond to `status=err`.

No unexpected `status=ok` IDs were missing.

Form-level overlap checks also passed between the generated training, validation, and test sets.

---

### Final EXP002 Baseline

The complete usable test set was evaluated:

```text
Samples:      1,480
CER:          3.33%
WER:          8.63%
Exact Match:  56.89%
Exact:        842 / 1,480
Non-exact:    638
```

This is the fixed pretrained TrOCR baseline for subsequent experiments.

Detailed documentation:

```text
experiments/EXP002_iam_trocr_baseline.md
```

---

# EXP002 — Systematic Error Analysis

The 638 non-exact predictions were used for systematic error analysis.

A reproducible diagnostic sample was created:

```text
50 highest-CER errors
+
50 random non-exact errors
+
25 low-CER non-exact errors
=
125 manually reviewed samples
```

The manually reviewed fields include:

```text
id
ground_truth
prediction
cer
wer
selection_group
error_category
image_quality
handwriting_difficulty
notes
```

### Error Categories

| Error Category | Count | % of Reviewed Samples |
|---|---:|---:|
| Word substitution | 72 | 57.6% |
| Character substitution | 62 | 49.6% |
| Punctuation | 24 | 19.2% |
| Spacing | 21 | 16.8% |
| Capitalization | 1 | 0.8% |

Multiple categories may occur in one prediction.

The diagnostic sample deliberately oversamples high- and low-CER cases, so these percentages should not be interpreted as prevalence estimates across all 638 failures.

### Main Findings

- Word substitutions dominated severe high-CER failures.
- Character substitutions were common across the diagnostic sample.
- Low-CER failures frequently involved small character or spacing differences.
- 68% of the 50 highest-CER samples were manually classified as difficult handwriting.
- Many recognition failures occurred on images that appeared visually good.
- CER alone does not fully describe whether an entire field or line is correct.

Detailed documentation:

```text
experiments/EXP002_error_analysis.md
```

Notebook:

```text
notebooks/03_exp002_error_analysis.ipynb
```

Results:

```text
results/exp002/
├── exp002_error_analysis.csv
├── error_category_summary.csv
└── figures/
    ├── exp002_error_categories.png
    ├── exp002_categories_by_group.png
    └── exp002_handwriting_difficulty.png
```

---

# EXP003 — Controlled Image Preprocessing

EXP003 is currently in progress.

## Research Question

> Does controlled image preprocessing improve pretrained TrOCR recognition accuracy on IAM handwriting?

Candidate preprocessing conditions include:

```text
Original
Grayscale
Otsu thresholding
CLAHE contrast enhancement
Denoising
Deskewing
```

The experiment uses the IAM validation split for development and preprocessing selection.

Initial development will use a reproducible:

```text
N = 100
random_state = 42
```

validation subset.

The same images will be evaluated under each preprocessing condition.

Metrics:

```text
CER
WER
Exact Match
```

The workflow is:

```text
IAM Validation Set
        ↓
Reproducible DEV100
        ↓
Original Baseline
        ↓
Controlled Preprocessing Conditions
        ↓
CER / WER / Exact Match Comparison
        ↓
Select Promising Method
        ↓
Full Validation Evaluation
        ↓
Freeze Method
        ↓
Held-Out IAM Test Evaluation
        ↓
Compare with EXP002
```

The EXP002 held-out test result remains fixed:

```text
CER:         3.33%
WER:         8.63%
Exact Match: 56.89%
```

The test set should not be repeatedly used to select preprocessing parameters.

Planned implementation:

```text
notebooks/04_exp003_preprocessing.ipynb
src/preprocessing.py
experiments/EXP003_preprocessing.md
outputs/exp003/
```

---

# Experiment Outputs

Experiment outputs are stored separately to preserve reproducibility.

```text
outputs/
├── exp002/
│   ├── n20/
│   ├── n50/
│   ├── n100/
│   └── iam_test/
│
└── exp003/
    └── dev100/
```

EXP002 output files include:

```text
predictions.csv
best_predictions.csv
worst_predictions.csv
summary.json
```

Analyzed research results are stored separately:

```text
results/
└── exp002/
    ├── exp002_error_analysis.csv
    ├── error_category_summary.csv
    └── figures/
```

This distinction is intentional:

```text
outputs = raw experiment outputs

results = analyzed research findings
```

---

## Current Progress

### Completed

- [x] Pretrained TrOCR inference
- [x] CSV-based image loading
- [x] CER implementation
- [x] WER implementation
- [x] Exact Match implementation
- [x] OCR metric testing
- [x] IAM dataset study
- [x] IAM data preparation
- [x] IAM CSV manifest generation
- [x] IAM writer-independent split generation
- [x] Split coverage diagnostics
- [x] Split overlap checks
- [x] EXP002 N=20 evaluation
- [x] EXP002 N=50 evaluation
- [x] EXP002 N=100 evaluation
- [x] EXP002 full IAM test evaluation
- [x] EXP002 systematic error analysis
- [x] 125-sample manual review
- [x] Error-category summary
- [x] Error-analysis figures
- [x] TrOCR literature review
- [x] CRNN literature review
- [x] FUNSD literature review
- [x] HTR-VT literature review

### In Progress

- [ ] EXP003 controlled image preprocessing
- [ ] OpenCV preprocessing implementation
- [ ] DEV100 validation baseline
- [ ] Validation preprocessing comparison

### Next Steps

- [ ] Complete EXP003 development experiments
- [ ] Select promising preprocessing method
- [ ] Evaluate selected method on full validation set
- [ ] Evaluate frozen preprocessing method on held-out test set
- [ ] Compare EXP003 against EXP002
- [ ] Investigate template/document alignment
- [ ] Build field extraction pipeline
- [ ] Investigate structured handwritten forms
- [ ] Explore field-aware recognition
- [ ] Explore layout-aware recognition
- [ ] Investigate IAM-specific model adaptation / fine-tuning

---

## Research Progression

The project now follows:

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
EXP002 TrOCR Baseline
        │
        ▼
Systematic Error Analysis
        │
        ▼
EXP003 Controlled Preprocessing
        │
        ▼
Template Alignment
        │
        ▼
Field Extraction
        │
        ▼
Field / Layout Context
        │
        ▼
Structured Output
```

The purpose of EXP003 is not to assume preprocessing improves OCR.

Instead, it tests whether controlled transformations produce measurable improvement relative to an unchanged baseline.