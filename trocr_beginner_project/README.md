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

EXP003 evaluates whether conventional image preprocessing improves pretrained TrOCR recognition performance.

## Research Question

> Does controlled image preprocessing improve pretrained TrOCR recognition accuracy on IAM handwriting?

---

## Experimental Protocol

Preprocessing development uses the IAM validation split.

A reproducible DEV100 subset was created using:

```text
N = 100
random_state = 42
```

The workflow is:

```text
IAM Validation
        ↓
DEV100
        ↓
Visual Analysis
        ↓
Original Baseline
        ↓
Grayscale / Otsu / CLAHE / Denoising
        ↓
Aggregate Comparison
        ↓
Paired Sample-Level Analysis
        ↓
Select Candidate
        ↓
Full Validation
        ↓
Freeze Decision
        ↓
Held-Out Test
```

The test set is not used for preprocessing selection.

---

## DEV100 Control

Original images:

```text
Samples:       100
CER:           2.61%
WER:           7.27%
Exact Match:   62%
Exact:         62 / 100
```

---

## DEV100 Controlled Comparison

| Condition | CER | WER | Exact Match |
|---|---:|---:|---:|
| Original | 2.61% | 7.27% | 62% |
| Grayscale | 2.61% | 7.27% | 62% |
| **Otsu Threshold** | **2.49%** | **6.94%** | **68%** |
| CLAHE | 3.08% | 8.62% | 59% |
| Denoising | 2.79% | 7.55% | 62% |

---

## Paired DEV100 Analysis

| Condition | Improved | Unchanged | Worsened | Recovered Exact | Lost Exact | Net Exact |
|---|---:|---:|---:|---:|---:|---:|
| Grayscale | 0 | 100 | 0 | 0 | 0 | 0 |
| Otsu Threshold | 13 | 77 | 10 | 8 | 2 | **+6** |
| CLAHE | 5 | 85 | 10 | 2 | 5 | -3 |
| Denoising | 5 | 92 | 3 | 1 | 1 | 0 |

Otsu Exact Match transitions:

```text
Original exact:       62
Original non-exact:   38

Stayed exact:         60
Recovered exact:       8
Lost exact:            2
Stayed non-exact:     30

Otsu exact:            68
Net Exact Gain:        +6
```

---

## Current EXP003 Decision

Otsu thresholding is the only tested method that:

- reduced CER,
- reduced WER,
- increased Exact Match,
- and produced a positive paired Exact Match gain.

However:

```text
CER improved: 13
CER worsened: 10
```

so Otsu is not universally beneficial.

Current decision:

```text
Grayscale       → stop
Otsu            → advance
CLAHE           → stop under current configuration
Denoising       → stop under current configuration
```

---

## Next Stage

Evaluate:

```text
Original
vs.
Otsu Thresholding
```

on the complete:

```text
IAM Validation
N = 1,539
```

Then perform:

```text
aggregate comparison
+
paired sample-level analysis
```

before freezing the preprocessing decision.

Only the frozen preprocessing configuration will be evaluated on the held-out:

```text
IAM Test
N = 1,480
```

---

## EXP003 Files

```text
notebooks/
└── 04_exp003_preprocessing.ipynb

src/
└── preprocessing.py

experiments/
└── EXP003_preprocessing.md

outputs/
└── exp003/
    ├── validation_dev100.csv
    └── dev100/
        ├── original.csv
        ├── grayscale.csv
        ├── otsu.csv
        ├── clahe.csv
        ├── denoise.csv
        ├── comparison.csv
        └── paired_analysis/
            ├── grayscale_paired.csv
            ├── otsu_threshold_paired.csv
            ├── clahe_paired.csv
            ├── denoising_paired.csv
            └── paired_summary.csv
```

Detailed methodology and interpretation:

```text
experiments/EXP003_preprocessing.md
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

### EXP003 Completed So Far

- [x] OpenCV preprocessing implementation
- [x] Reproducible DEV100 selection
- [x] Visual preprocessing comparison
- [x] Original DEV100 TrOCR baseline
- [x] Grayscale DEV100 evaluation
- [x] Otsu DEV100 evaluation
- [x] CLAHE DEV100 evaluation
- [x] Denoising DEV100 evaluation
- [x] Aggregate CER / WER / Exact Match comparison
- [x] Paired sample-level comparison
- [x] Exact Match transition analysis
- [x] Otsu selected as full-validation candidate

### In Progress

- [ ] Inspect representative Otsu recoveries and regressions
- [ ] Full-validation Original evaluation
- [ ] Full-validation Otsu evaluation
- [ ] Full-validation paired analysis

### Next Steps

- [ ] Freeze EXP003 preprocessing decision
- [ ] Evaluate frozen configuration on held-out IAM test set
- [ ] Complete EXP003 documentation
- [ ] Begin template/document alignment
- [ ] Build structured field extraction pipeline
- [ ] Investigate field-aware recognition
- [ ] Evaluate field-specific constraints
- [ ] Develop final thesis hypothesis/contribution

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