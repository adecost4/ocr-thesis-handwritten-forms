# Thesis Progress Report

**Reporting Period:** October 21 – November 10, 2026  
**Student:** Aloyson De Costa

## Progress This Period

Over the past three weeks, my main focus was completing the thesis midterm progress review and advancing **EXP003 — Controlled Image Preprocessing**. I also refined the direction of the thesis based on feedback received during the midterm review.

### 1. Midterm Thesis Progress Review

I completed my thesis midterm progress review on **October 27**.

During the review, I presented:

- the overall structured handwritten-form recognition problem,
- literature reviewed so far,
- the IAM dataset and evaluation methodology,
- the EXP002 pretrained TrOCR baseline,
- systematic error-analysis results,
- and the proposed progression toward preprocessing, template alignment, and structured field extraction.

An important point from the review was that, while the current experiments use existing recognition algorithms such as TrOCR, the final thesis should clearly demonstrate and document **my own research work and contribution**.

This contribution may include the experimental methodology, systematic analysis of model behavior, documented findings, and eventually the design and evaluation of a structured-form recognition approach.

Based on this feedback, I am treating EXP002 and EXP003 as experiments that establish and characterize the existing HTR baseline before moving toward the main structured-form contribution.

---

### 2. EXP003 — Visual Preprocessing Analysis

I continued **EXP003 — Controlled Image Preprocessing**, which investigates whether conventional image preprocessing improves pretrained TrOCR recognition.

A reproducible development subset of **100 samples** was selected from the IAM validation split using a fixed random seed.

I visually inspected multiple samples under the following conditions:

- Original
- Grayscale
- Otsu thresholding
- CLAHE contrast enhancement
- Denoising

The visual analysis showed that grayscale and denoising produced relatively small changes because many IAM images were already clean.

Otsu thresholding produced the strongest foreground/background separation, while CLAHE sometimes improved faint handwriting but also amplified background variations.

No method was selected based only on visual appearance. All methods were evaluated quantitatively using the same DEV100 samples.

---

### 3. EXP003 — DEV100 Original Baseline

The Original DEV100 images were first evaluated without additional preprocessing to establish the control condition.

The results were:

| Metric | Result |
|---|---:|
| Samples | 100 |
| CER | **2.61%** |
| WER | **7.27%** |
| Exact Match | **62.00%** |
| Exact Predictions | **62 / 100** |

This baseline is used only for comparison with preprocessing conditions on the same DEV100 samples.

---

### 4. Controlled Preprocessing Comparison

The same 100 samples were then evaluated using each preprocessing condition while keeping the TrOCR model, processor, decoding procedure, and metrics unchanged.

The results were:

| Condition | CER | WER | Exact Match |
|---|---:|---:|---:|
| Original | **2.61%** | **7.27%** | **62%** |
| Grayscale | 2.61% | 7.27% | 62% |
| Otsu Threshold | **2.49%** | **6.94%** | **68%** |
| CLAHE | 3.08% | 8.62% | 59% |
| Denoising | 2.79% | 7.55% | 62% |

Among the evaluated conditions, **Otsu thresholding produced the most promising preliminary result**, improving all three metrics.

Grayscale produced no measurable change, while CLAHE and denoising did not improve the aggregate recognition results.

---

### 5. Paired Sample-Level Analysis

Because aggregate metrics do not explain how individual predictions change, I performed a paired analysis between each preprocessing condition and the Original control.

The results were:

| Condition | Improved CER | Unchanged | Worsened | Recovered Exact | Lost Exact | Net Exact Gain |
|---|---:|---:|---:|---:|---:|---:|
| Grayscale | 0 | 100 | 0 | 0 | 0 | 0 |
| Otsu Threshold | **13** | 77 | 10 | **8** | 2 | **+6** |
| CLAHE | 5 | 85 | 10 | 2 | 5 | -3 |
| Denoising | 5 | 92 | 3 | 1 | 1 | 0 |

For Otsu thresholding:

- 8 previously incorrect predictions became exactly correct,
- 2 previously correct predictions became incorrect,
- producing a net gain of **6 Exact Matches**.

This explains the Exact Match improvement from:

```text
62% → 68%
```

However, Otsu was not universally beneficial. It improved CER for 13 samples but worsened CER for 10 samples.

Therefore, the current conclusion is not that thresholding always improves TrOCR, but that **Otsu is the most promising preprocessing candidate from the DEV100 experiment and requires larger-scale validation**.

---

## Current Research Interpretation

EXP003 has reinforced an important observation from the earlier EXP002 error analysis:

> Image preprocessing can improve some handwriting samples while negatively affecting others.

This suggests that applying the same preprocessing transformation universally may not always be optimal.

The paired analysis is therefore useful not only for selecting a preprocessing method but also for understanding which types of handwriting or image conditions benefit from particular transformations.

This may later become relevant when investigating structured forms, where preprocessing could potentially depend on field type, image condition, or other structural information.

---

## Thesis Direction Following Midterm Feedback

The work completed so far primarily establishes and analyzes the behavior of an existing HTR model.

The next phase will begin moving the project toward the main thesis problem:

```text
Structured Form
        ↓
Template Alignment
        ↓
Field Extraction
        ↓
Handwriting Recognition
        ↓
Field / Structural Information
        ↓
Validated Structured Output
```

The goal is to investigate whether information available in structured forms—such as field position, expected content type, valid character set, expected format, or other field constraints—can improve recognition beyond a general-purpose HTR baseline.

This will help distinguish the final thesis contribution from simply applying or tuning an existing OCR model.

---

## Next Steps

For the next research period, I plan to:

1. Inspect representative Otsu improvements and regressions from DEV100.
2. Evaluate **Original vs Otsu** on the complete **1,539-sample IAM validation split**.
3. Perform aggregate and paired analysis on the full validation results.
4. Freeze the EXP003 preprocessing decision before evaluating the selected method on the held-out test set.
5. Complete the final EXP003 documentation and conclusion.
6. Begin **template/document alignment** experiments for structured forms.
7. Begin developing a simple template-based field extraction pipeline.
8. Continue refining the thesis contribution around structured/form-aware recognition rather than only general HTR performance.

The immediate goal is to complete EXP003 and then transition from general handwritten-line recognition toward the structured-form component of the thesis.