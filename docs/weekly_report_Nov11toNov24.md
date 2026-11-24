# Thesis Progress Report

**Reporting Period:** November 11 – November 24, 2026  
**Student:** Aloyson De Costa

## Progress This Period

During this reporting period, my main focus was completing **EXP003 — Controlled Image Preprocessing**, validating the selected preprocessing method on the complete IAM validation and held-out test sets, documenting the final findings, and beginning the transition toward structured-form processing through **EXP004 — Template Alignment**.

---

### 1. EXP003 — Full IAM Validation Evaluation

The previous DEV100 experiment identified **Otsu thresholding** as the most promising preprocessing candidate.

To determine whether this result generalized beyond the 100-sample development subset, I evaluated the Original and Otsu conditions on the complete usable IAM validation split containing **1,539 samples**.

The results were:

| Condition | CER | WER | Exact Match |
|---|---:|---:|---:|
| Original | 3.22% | 8.24% | 58.48% |
| Otsu Threshold | **2.58%** | **6.96%** | **64.07%** |

Otsu therefore improved all three aggregate metrics on the complete validation split.

A paired sample-level analysis showed:

| Measure | Result |
|---|---:|
| Improved CER | 285 |
| Unchanged CER | 1,131 |
| Worsened CER | 123 |
| Recovered Exact | 139 |
| Lost Exact | 53 |
| Net Exact Gain | **+86** |

The full-validation results confirmed the direction initially observed on DEV100.

Based only on the validation evidence, I selected and froze Otsu thresholding as the EXP003 preprocessing configuration before evaluating the held-out test set.

---

### 2. EXP003 — Held-Out IAM Test Evaluation

After freezing the preprocessing decision, I evaluated the selected Otsu configuration on the complete usable IAM held-out test set containing **1,480 samples**.

The fixed EXP002 Original baseline was compared against the Otsu condition.

| Condition | CER | WER | Exact Match | Exact Predictions |
|---|---:|---:|---:|---:|
| Original | 3.33% | 8.63% | 56.89% | 842 / 1,480 |
| Otsu Threshold | **2.57%** | **7.39%** | **61.96%** | **917 / 1,480** |

Compared with the Original baseline, Otsu:

- reduced CER from **3.33% to 2.57%**,
- reduced WER from **8.63% to 7.39%**,
- increased Exact Match from **56.89% to 61.96%**,
- and produced **75 additional exact predictions**.

---

### 3. Held-Out Paired Analysis

The paired test analysis was also used to understand how individual predictions changed.

The results were:

| Measure | Result |
|---|---:|
| Improved CER | 251 |
| Unchanged CER | 1,117 |
| Worsened CER | 112 |
| Recovered Exact | 114 |
| Lost Exact | 39 |
| Net Exact Gain | **+75** |

The Exact Match transitions were:

```text
Original exact:       842
Original non-exact:   638

Stayed exact:         803
Recovered exact:      114
Lost exact:            39
Stayed non-exact:     524
```

The transition integrity check passed.

These results show that the improvement observed during development and validation also generalized to the held-out test set.

However, Otsu was still not beneficial for every sample. Some predictions worsened after thresholding, which reinforces the importance of paired sample-level analysis in addition to aggregate metrics.

---

### 4. EXP003 Final Conclusion

EXP003 is now **complete**.

Across all three stages, Otsu produced a consistent improvement:

| Dataset | Original Exact Match | Otsu Exact Match |
|---|---:|---:|
| DEV100 | 62.00% | **68.00%** |
| Full Validation | 58.48% | **64.07%** |
| Held-Out Test | 56.89% | **61.96%** |

The final conclusion is that **Otsu thresholding provides a reproducible overall improvement in pretrained TrOCR recognition on IAM under the evaluated experimental configuration, although its effect remains sample-dependent**.

I have completed the EXP003 experiment documentation, including the methodology, aggregate results, paired analyses, limitations, and final conclusion.

No further preprocessing selection or parameter tuning will be performed using the IAM held-out test set.

---

### 5. Literature Review — Document Alignment

I completed a literature review of:

**Character Keypoint-Based Homography Estimation in Scanned Documents for Efficient Information Extraction**

This paper is directly relevant to the next stage of the thesis because it addresses the problem of aligning a scanned or photographed structured document with a known reference template.

The main pipeline studied in the paper is:

```text
Reference Template
        +
Incoming Form
        ↓
Keypoint Detection / Matching
        ↓
RANSAC
        ↓
Homography Estimation
        ↓
Document Alignment
        ↓
Known Field Coordinates
        ↓
Field Extraction
```

An important takeaway is that alignment allows fixed coordinates defined on a reference template to be reused for extracting corresponding information fields from incoming forms.

This provides a bridge between my current work on already-segmented handwriting and the broader thesis problem involving complete structured forms.

---

### 6. EXP004 — Template Alignment

I have now started **EXP004 — Template Alignment**.

The initial research question is:

> Can a fixed-template document be geometrically aligned to a reference template accurately enough to support reliable field extraction?

The initial implementation will investigate:

- controlled rotation,
- translation,
- scaling,
- perspective distortion,
- feature/keypoint detection,
- feature matching,
- RANSAC,
- homography estimation,
- and perspective warping.

The initial alignment experiment will be evaluated independently of TrOCR so that alignment errors can be separated from handwriting-recognition errors.

This will allow later experiments to distinguish between:

```text
Alignment / Extraction Error
```

and:

```text
Handwriting Recognition Error
```

rather than treating all failures as OCR errors.

---

## Current Research Interpretation

The thesis has now progressed from evaluating general handwriting recognition toward the structured-form problem.

The experimental progression is:

```text
EXP002
Pretrained TrOCR Baseline
        ✓
        ↓
Systematic Error Analysis
        ✓
        ↓
EXP003
Controlled Image Preprocessing
        ✓
        ↓
Validated Otsu Improvement
        ✓
        ↓
EXP004
Template Alignment
        ← CURRENT
        ↓
Structured Field Extraction
        ↓
Field-Aware Recognition
        ↓
Structured Output
```

EXP002 and EXP003 establish and characterize the handwriting-recognition baseline.

The next experiments will increasingly focus on the structured-form pipeline and on identifying the thesis contribution beyond the application of an existing HTR model.

---

## Next Steps

For the next research period, I plan to:

1. Complete the initial controlled EXP004 template-alignment experiment.
2. Evaluate alignment under rotation, translation, scaling, and perspective variation.
3. Analyze alignment successes and failure cases.
4. Compare alignment quality using quantitative and visual measures.
5. Demonstrate fixed-coordinate field extraction before and after alignment.
6. Document EXP004 methodology and findings.
7. Move from synthetic/controlled transformations toward realistic scanned or photographed structured forms.
8. Begin the structured field-extraction stage.
9. Continue literature review on document understanding and layout-aware methods.
10. Investigate how template and field information can later support field-aware handwriting recognition.

The immediate goal is to establish a reliable template-alignment and field-localization pipeline before reconnecting the structured-form system with TrOCR.