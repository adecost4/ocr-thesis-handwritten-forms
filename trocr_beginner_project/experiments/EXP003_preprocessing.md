# EXP003 — Controlled Image Preprocessing for TrOCR

## Status

**IN PROGRESS**

Current progress:

```text
Visual preprocessing study                 ✓
DEV100 Original baseline                   ✓
DEV100 preprocessing comparison            ✓
DEV100 paired sample-level analysis        ✓
Representative recovery/regression review  NEXT
Full IAM validation evaluation             NEXT
Final preprocessing decision               PENDING
Held-out IAM test evaluation               PENDING
Final EXP003 conclusion                     PENDING
```

---

# Objective

Evaluate whether controlled image preprocessing improves the recognition performance of pretrained TrOCR on IAM handwritten text.

EXP003 builds directly on EXP002.

EXP002 established the pretrained TrOCR recognition baseline and identified the major recognition-error patterns.

EXP003 investigates whether conventional image preprocessing can reduce some of these errors.

The experiment does **not** assume that visually cleaner images necessarily produce better OCR results.

Instead, preprocessing methods are evaluated quantitatively under controlled conditions.

---

# Research Question

> **Does controlled image preprocessing improve pretrained TrOCR handwriting-recognition performance compared with the unmodified Original image condition?**

---

# Motivation

EXP002 established a baseline using:

```text
microsoft/trocr-base-handwritten
```

on the usable IAM writer-independent test split.

The final EXP002 results were:

| Metric | Result |
|---|---:|
| Samples | 1,480 |
| CER | 3.33% |
| WER | 8.63% |
| Exact Match | 56.89% |
| Exact Predictions | 842 / 1,480 |
| Non-Exact Predictions | 638 |

A systematic error analysis was then performed on a targeted diagnostic sample of 125 non-exact predictions.

The analysis identified several recurring error types:

- word substitutions,
- character substitutions,
- punctuation errors,
- spacing errors,
- handwriting difficulty,
- and some image-condition problems.

However, many recognition failures occurred on images that appeared visually clean.

Therefore:

> Poor image quality alone does not explain TrOCR recognition failures.

This motivated EXP003 as a controlled experiment rather than assuming that preprocessing would automatically improve recognition.

---

# Hypotheses

## Null Hypothesis — H0

Additional image preprocessing does not improve pretrained TrOCR recognition performance compared with the Original image condition.

## Alternative Hypothesis — H1

At least one controlled preprocessing method improves pretrained TrOCR recognition performance compared with the Original image condition.

---

# Model

The same pretrained model is used throughout EXP003:

```text
microsoft/trocr-base-handwritten
```

No IAM-specific fine-tuning is performed.

The model and decoding configuration remain unchanged across preprocessing conditions.

---

# Dataset

## IAM Handwriting Database

EXP003 uses the IAM writer-independent validation split generated during EXP002 dataset preparation.

Usable validation samples:

```text
1,539
```

The IAM held-out test split contains:

```text
1,480
```

usable lines.

The test set is intentionally not used for preprocessing selection.

---

# Experimental Protocol

EXP003 follows a validation-first experimental protocol.

```text
IAM Validation Split
        ↓
Reproducible DEV100 subset
        ↓
Visual preprocessing inspection
        ↓
Original DEV100 control
        ↓
Controlled preprocessing comparison
        ↓
Paired sample-level analysis
        ↓
Select promising preprocessing candidate
        ↓
Complete IAM Validation Split
        ↓
Freeze preprocessing decision
        ↓
Held-Out IAM Test Set
        ↓
Final EXP003 conclusion
```

This design reduces the risk of repeatedly optimizing preprocessing choices against the held-out test set.

---

# DEV100 Development Subset

A reproducible development subset was selected from the IAM validation split.

Configuration:

```text
N = 100
random_state = 42
```

The selected subset is saved as:

```text
outputs/exp003/validation_dev100.csv
```

The same 100 sample IDs are used for every DEV100 preprocessing condition.

This enables paired sample-level comparisons.

---

# Preprocessing Conditions

Five conditions were evaluated.

## 1. Original

No additional OpenCV preprocessing.

This is the control condition.

---

## 2. Grayscale

The image is explicitly converted to grayscale.

Purpose:

> Determine whether explicit removal of color information affects recognition.

---

## 3. Otsu Thresholding

The image is converted to grayscale and automatic global thresholding is applied using Otsu's method.

Conceptually:

```text
Grayscale Image
        ↓
Estimate Threshold
        ↓
Binary Foreground / Background
```

Purpose:

> Increase separation between handwriting strokes and the background.

---

## 4. CLAHE Contrast Enhancement

Contrast Limited Adaptive Histogram Equalization is applied to increase local contrast.

Purpose:

> Determine whether enhancing faint handwriting improves recognition.

---

## 5. Denoising

OpenCV Non-Local Means denoising is applied.

Purpose:

> Reduce small image artifacts while preserving handwriting strokes.

---

# Controlled Variables

The following variables remain unchanged across all DEV100 conditions:

- DEV100 sample IDs,
- IAM ground truth,
- pretrained TrOCR checkpoint,
- TrOCR processor,
- model inference procedure,
- decoding procedure,
- CER implementation,
- WER implementation,
- Exact Match implementation,
- and compute environment.

Therefore, the additional image preprocessing operation is the primary experimental variable.

---

# Evaluation Metrics

EXP003 uses the same metrics as EXP002.

## Character Error Rate — CER

CER measures character-level recognition differences.

```text
CER =
Substitutions + Insertions + Deletions
-------------------------------------
Number of Ground-Truth Characters
```

Lower is better.

---

## Word Error Rate — WER

WER measures recognition differences at the word level.

```text
WER =
Word Substitutions + Insertions + Deletions
-------------------------------------------
Number of Ground-Truth Words
```

Lower is better.

---

## Exact Match

Exact Match measures whether the complete predicted transcription exactly matches the ground truth.

```text
1 = complete match
0 = at least one difference
```

Higher is better.

Exact Match is particularly important for the broader structured-form thesis because even a single incorrect character may invalidate fields such as:

- IDs,
- dates,
- account numbers,
- phone numbers,
- ZIP codes,
- and names.

---

# Stage 1 — Visual Preprocessing Analysis

Before performing quantitative OCR evaluation, 10 samples from DEV100 were manually inspected under all preprocessing conditions.

The inspected samples included different handwriting characteristics such as:

- thin handwriting,
- faint handwriting,
- dark handwriting,
- separated characters,
- connected cursive writing,
- and different writer styles.

The purpose of this stage was **not** to select the best preprocessing method.

The goal was to verify that each transformation behaved as expected before running TrOCR.

---

# Original — Visual Observations

The Original IAM line images were generally clean and readable.

Most samples contained:

- mostly white backgrounds,
- limited visible noise,
- clear separation between handwriting and background,
- and sufficient contrast.

However, handwriting characteristics varied substantially.

Some samples contained dark and clearly separated characters, while others contained thin, faint, or highly cursive strokes.

The observed variation appeared to be related more to handwriting style and stroke intensity than to severe image degradation.

---

# Grayscale — Visual Observations

Grayscale conversion produced almost no visible change compared with the Original images.

Across the inspected samples:

- handwriting structure was preserved,
- stroke thickness remained similar,
- background appearance remained nearly unchanged,
- and no obvious new information was introduced.

This was expected because IAM line images already contain little meaningful color information.

Visual inspection therefore suggested that explicit grayscale conversion might provide limited additional benefit.

---

# Otsu Thresholding — Visual Observations

Otsu thresholding produced the strongest visible transformation among the evaluated methods.

The transformation generally:

- darkened handwriting strokes,
- produced an almost completely white background,
- removed faint background intensity variations,
- and increased foreground/background separation.

For some faint handwriting samples, the text became visually more prominent.

However, thresholding also modifies the original stroke-intensity information.

Potential risks include:

- altering thin strokes,
- removing lightly written details,
- increasing apparent stroke thickness,
- and removing grayscale information potentially useful to TrOCR.

Therefore, a cleaner visual appearance was not assumed to imply better recognition.

---

# CLAHE — Visual Observations

CLAHE increased local contrast while preserving grayscale structure.

In some samples, faint handwriting became more visible.

However, CLAHE also amplified local background variations.

Several images showed more noticeable gray or patch-like background regions after contrast enhancement.

Therefore, CLAHE appeared capable of strengthening faint strokes but could also amplify undesirable image artifacts.

---

# Denoising — Visual Observations

Denoising produced relatively subtle visual changes.

The handwriting structure was generally preserved.

Small intensity variations appeared smoother, but because most IAM images were already relatively clean, the transformation produced limited obvious visual improvement.

Excessive smoothing could potentially reduce useful thin-stroke information.

---

# Stage 1 Conclusion

The visual comparison can be summarized as:

| Method | Visual Observation |
|---|---|
| Original | Generally clean and readable |
| Grayscale | Almost identical to Original |
| Otsu | Strong foreground/background separation |
| CLAHE | Stronger local contrast but may amplify background artifacts |
| Denoising | Subtle smoothing with limited visible benefit |

No preprocessing method was consistently visually superior across all inspected samples.

Therefore:

> Visual appearance alone was considered insufficient for selecting a preprocessing method.

All methods were advanced to quantitative DEV100 evaluation.

---

# Stage 2 — Original DEV100 Control

The Original DEV100 images were evaluated using pretrained TrOCR without additional OpenCV preprocessing.

## Results

| Metric | Result |
|---|---:|
| Samples | 100 |
| Average CER | **2.61%** |
| Average WER | **7.27%** |
| Exact Match | **62.00%** |
| Exact Predictions | **62 / 100** |

This establishes the EXP003 DEV100 control condition.

---

## Important Interpretation

The DEV100 Original result should **not** be directly compared with the EXP002 test-set result as evidence of improvement.

EXP002 uses a different set of samples:

```text
EXP002 Test:
N = 1,480
CER = 3.33%
WER = 8.63%
Exact Match = 56.89%
```

EXP003 DEV100 uses:

```text
Validation DEV100:
N = 100
CER = 2.61%
WER = 7.27%
Exact Match = 62%
```

The DEV100 Original result exists specifically as the control condition for the preprocessing experiments performed on those same 100 samples.

---

# Stage 3 — Controlled DEV100 Preprocessing Comparison

Each preprocessing condition was evaluated on exactly the same DEV100 samples.

## Aggregate Results

| Condition | Samples | CER | WER | Exact Match | Exact Predictions |
|---|---:|---:|---:|---:|---:|
| Original | 100 | **2.61%** | **7.27%** | **62%** | 62 |
| Grayscale | 100 | 2.61% | 7.27% | 62% | 62 |
| Otsu Threshold | 100 | **2.49%** | **6.94%** | **68%** | **68** |
| CLAHE | 100 | 3.08% | 8.62% | 59% | 59 |
| Denoising | 100 | 2.79% | 7.55% | 62% | 62 |

---

# Preliminary DEV100 Findings

Otsu thresholding was the only tested preprocessing condition to improve all three aggregate metrics simultaneously.

Compared with Original:

```text
CER
2.61% → 2.49%

WER
7.27% → 6.94%

Exact Match
62% → 68%
```

This corresponds to an increase of:

```text
+6 percentage points
```

in Exact Match.

---

## Grayscale

Grayscale produced no measurable change.

```text
Original:
CER = 2.61%
WER = 7.27%
Exact = 62%

Grayscale:
CER = 2.61%
WER = 7.27%
Exact = 62%
```

This agrees with the visual observation that IAM line images already contain little meaningful color information.

---

## CLAHE

CLAHE worsened all three aggregate metrics.

```text
CER:
2.61% → 3.08%

WER:
7.27% → 8.62%

Exact:
62% → 59%
```

The result is consistent with the visual observation that CLAHE sometimes amplified local background variations.

---

## Denoising

Denoising slightly worsened CER and WER.

```text
CER:
2.61% → 2.79%

WER:
7.27% → 7.55%
```

Exact Match remained:

```text
62%
```

Therefore, denoising did not provide evidence of an aggregate recognition improvement under the current configuration.

---

# Why Aggregate Results Were Not Enough

Although Otsu produced the best aggregate result, average metrics do not explain how individual predictions changed.

For example, an average improvement could result from:

```text
few large improvements
+
many regressions
```

or:

```text
many small improvements
+
few regressions
```

These situations have different implications.

A paired sample-level analysis was therefore performed.

---

# Stage 4 — Paired Sample-Level Analysis

Each processed prediction was paired with its corresponding Original prediction using the IAM sample ID.

For CER:

```text
Processed CER < Original CER
→ Improved

Processed CER = Original CER
→ Unchanged

Processed CER > Original CER
→ Worsened
```

Exact Match transitions were also analyzed.

```text
Original non-exact
        ↓
Processed exact

= Recovered Exact
```

and:

```text
Original exact
        ↓
Processed non-exact

= Lost Exact
```

---

# Paired Results

| Condition | Improved CER | Unchanged CER | Worsened CER | Recovered Exact | Lost Exact | Net Exact Gain |
|---|---:|---:|---:|---:|---:|---:|
| Grayscale | 0 | 100 | 0 | 0 | 0 | 0 |
| **Otsu Threshold** | **13** | 77 | 10 | **8** | 2 | **+6** |
| CLAHE | 5 | 85 | 10 | 2 | 5 | -3 |
| Denoising | 5 | 92 | 3 | 1 | 1 | 0 |

---

# Grayscale Paired Analysis

Grayscale produced no prediction-level change.

```text
Improved CER:    0
Unchanged CER: 100
Worsened CER:    0

Recovered Exact: 0
Lost Exact:      0
Net Exact Gain:  0
```

This provides strong evidence that explicit grayscale conversion is redundant for the current IAM/TrOCR setup.

---

# Otsu Paired Analysis

Otsu produced the strongest paired result.

```text
Improved CER:   13
Unchanged CER:  77
Worsened CER:   10
```

At the Exact Match level:

```text
Recovered Exact: 8
Lost Exact:      2
Net Exact Gain: +6
```

This explains the aggregate Exact Match increase:

```text
Original: 62%
Otsu:     68%
```

---

# Otsu Exact-Match Transition Analysis

The Original condition contained:

```text
Exact:     62
Non-exact: 38
```

After Otsu thresholding:

```text
Stayed exact:       60
Recovered exact:     8
Lost exact:          2
Stayed non-exact:   30
```

These transitions sum to:

```text
100 samples
```

and produce:

```text
60 + 8 = 68 Otsu Exact Matches
```

The transition integrity check passed.

---

# Interpretation of Otsu Result

The Otsu improvement is not caused only by a change in aggregate CER.

Eight previously incorrect predictions became completely correct.

At the same time, two previously correct predictions became incorrect.

Therefore:

```text
8 recovered
-
2 lost
=
+6 net Exact Matches
```

This provides stronger evidence of potential benefit than aggregate metrics alone.

However, Otsu is **not universally beneficial**.

At the CER level:

```text
13 improved
77 unchanged
10 worsened
```

Therefore, thresholding can help some samples while negatively affecting others.

This observation is important for the broader thesis because it suggests that a single preprocessing transformation may not be optimal for every handwriting/image condition.

---

# CLAHE Paired Analysis

CLAHE produced:

```text
Improved CER:   5
Unchanged CER: 85
Worsened CER:  10
```

Exact Match transitions were:

```text
Recovered Exact: 2
Lost Exact:      5
Net Exact Gain: -3
```

This supports the aggregate conclusion that CLAHE is unfavorable under the current configuration.

---

# Denoising Paired Analysis

Denoising produced:

```text
Improved CER:   5
Unchanged CER: 92
Worsened CER:   3
```

Exact Match transitions were:

```text
Recovered Exact: 1
Lost Exact:      1
Net Exact Gain:  0
```

Denoising therefore changed relatively few predictions and did not improve overall Exact Match.

---

# Stage 4 Overall Interpretation

Among the four evaluated preprocessing conditions, Otsu thresholding provides the strongest preliminary evidence of benefit.

It was the only method that:

- reduced average CER,
- reduced average WER,
- increased Exact Match,
- recovered substantially more Exact Matches than it lost,
- and produced a positive net Exact Match gain.

However:

> The DEV100 result does not establish that Otsu universally improves TrOCR.

The experiment contains only 100 validation samples, and Otsu worsened CER for 10 of them.

Therefore, the appropriate conclusion is:

> **Otsu thresholding is a promising preprocessing candidate that should be evaluated on the complete IAM validation split.**

---

# Current Preprocessing Decision

Based on DEV100:

| Method | Decision |
|---|---|
| Grayscale | Do not advance |
| Otsu Threshold | **Advance to full validation** |
| CLAHE | Do not advance under current configuration |
| Denoising | Do not advance under current configuration |

This decision applies only to the current configurations.

It does not establish that other CLAHE, denoising, or preprocessing parameterizations could not perform differently.

---

# Stage 5 — Full IAM Validation Evaluation

## Status

**NEXT**

The next stage will evaluate:

```text
Complete IAM Validation Split
N = 1,539
```

under two conditions:

```text
Original
   vs.
Otsu Thresholding
```

The same:

- TrOCR model,
- processor,
- decoding procedure,
- CER implementation,
- WER implementation,
- and Exact Match implementation

will be used.

---

# Stage 5 Research Question

> Does the promising Otsu improvement observed on DEV100 generalize to the complete IAM validation split?

---

# Stage 5 Metrics

The following will be compared:

```text
CER
WER
Exact Match
Improved CER samples
Unchanged CER samples
Worsened CER samples
Recovered Exact Matches
Lost Exact Matches
```

---

# Stage 5 Results

**TBD**

| Condition | Samples | CER | WER | Exact Match |
|---|---:|---:|---:|---:|
| Original | 1,539 | TBD | TBD | TBD |
| Otsu Threshold | 1,539 | TBD | TBD | TBD |

---

# Stage 5 Paired Analysis

**TBD**

| Measure | Result |
|---|---:|
| Improved CER | TBD |
| Unchanged CER | TBD |
| Worsened CER | TBD |
| Recovered Exact | TBD |
| Lost Exact | TBD |
| Net Exact Gain | TBD |

---

# Held-Out Test Evaluation

## Status

**PENDING**

The IAM test set remains untouched during preprocessing development.

The final EXP003 preprocessing configuration will be selected using validation data.

Only after the decision is frozen will the selected configuration be evaluated on:

```text
IAM Test
N = 1,480
```

The result will then be compared with the fixed EXP002 baseline:

```text
EXP002

CER:         3.33%
WER:         8.63%
Exact Match: 56.89%
```

---

# Why the Test Set Is Kept Separate

Repeatedly evaluating preprocessing methods on the test set could indirectly optimize experimental decisions toward the test data.

Therefore:

```text
Validation
    ↓
Develop + select preprocessing

Test
    ↓
Final evaluation only
```

This provides a more defensible experimental protocol.

---

# Limitations So Far

## 1. DEV100 Sample Size

The current preprocessing conclusion is based on only 100 validation samples.

The result may not generalize to the complete validation distribution.

---

## 2. Limited Preprocessing Methods

Only four additional preprocessing conditions were evaluated:

```text
Grayscale
Otsu
CLAHE
Denoising
```

Other methods such as:

- deskewing,
- adaptive thresholding,
- resizing strategies,
- morphological operations,
- and preprocessing combinations

have not yet been evaluated.

---

## 3. Fixed Parameters

The current CLAHE and denoising experiments use one parameter configuration each.

Their results should therefore not be interpreted as proving that those techniques can never improve TrOCR.

---

## 4. Otsu Is Not Universally Beneficial

Otsu improved CER for 13 DEV100 samples but worsened CER for 10.

This indicates sample-dependent behavior.

---

## 5. General HTR Rather Than Structured Forms

EXP003 still evaluates cropped IAM handwriting lines.

It does not yet evaluate:

- template alignment,
- field detection,
- field type,
- expected field format,
- field-specific constraints,
- or structured output.

These are part of later thesis stages.

---

# Relevance to the Thesis

EXP003 contributes to the thesis by experimentally evaluating a common assumption:

> Does making handwriting images visually cleaner actually improve a pretrained Transformer HTR model?

The preliminary result demonstrates that preprocessing effects are method-dependent.

```text
Grayscale
→ no measurable effect

CLAHE
→ worse under current configuration

Denoising
→ no aggregate benefit

Otsu
→ promising improvement
```

More importantly, paired analysis shows that even a preprocessing method with better aggregate performance can:

```text
help some samples
+
harm other samples
```

This observation may become relevant to later structured-form research.

Instead of universally applying one preprocessing transformation, future work could potentially investigate preprocessing based on:

- image condition,
- field type,
- handwriting characteristics,
- or structural information.

That possibility remains a future research direction rather than a conclusion from EXP003.

---

# Connection to the Thesis Contribution

TrOCR and Otsu thresholding are existing techniques.

Therefore, EXP003 itself is not presented as a new OCR algorithm.

The contribution of this stage is the controlled experimental methodology and analysis used to understand:

- whether preprocessing helps,
- which preprocessing method helps,
- which samples improve,
- which samples regress,
- and whether the effect generalizes.

This evidence will inform the later structured-form pipeline.

The broader thesis aims to move from:

```text
Existing HTR Model
        ↓
General Recognition
```

toward:

```text
Structured Form
        ↓
Template Alignment
        ↓
Field Extraction
        ↓
HTR
        ↓
Field / Structural Information
        ↓
Validated Structured Output
```

Later experiments will investigate whether structured information can provide recognition benefits beyond the general HTR baseline.

---

# Current Conclusion

The current DEV100 experiment provides preliminary evidence that preprocessing can affect pretrained TrOCR recognition performance, but the effect depends strongly on the preprocessing method.

Otsu thresholding produced the strongest result:

```text
Original

CER:         2.61%
WER:         7.27%
Exact Match: 62%

        ↓ Otsu

CER:         2.49%
WER:         6.94%
Exact Match: 68%
```

Paired analysis showed:

```text
Recovered Exact: 8
Lost Exact:      2
Net Exact Gain: +6
```

However:

```text
CER Improved:  13
CER Worsened:  10
```

Therefore, the evidence does not support the claim that Otsu universally improves TrOCR.

The current conclusion is:

> **Otsu thresholding is the most promising preprocessing candidate identified in DEV100 and should be evaluated on the complete IAM validation split before any final preprocessing decision is made.**

---

# Next Steps

1. Inspect representative Otsu recoveries and regressions.
2. Run Original on all 1,539 IAM validation samples.
3. Run Otsu on the same 1,539 samples.
4. Compare CER, WER, and Exact Match.
5. Perform paired full-validation analysis.
6. Freeze the EXP003 preprocessing decision.
7. Evaluate the selected configuration once on the held-out IAM test set.
8. Write the final EXP003 conclusion.
9. Move toward template alignment.
10. Build structured field extraction.
11. Investigate field-aware recognition and constraints.

---

# Current EXP003 Status

```text
Research question defined                    ✓
Experimental protocol defined                ✓
DEV100 reproducibly selected                 ✓
Visual preprocessing analysis                ✓
Original DEV100 control                      ✓
Grayscale DEV100                             ✓
Otsu DEV100                                  ✓
CLAHE DEV100                                 ✓
Denoising DEV100                             ✓
Aggregate comparison                         ✓
Paired sample-level analysis                 ✓
Otsu Exact Match transition analysis         ✓

Current candidate:
Otsu Thresholding                            ✓

Representative recovery/regression review    NEXT
Full validation Original                     NEXT
Full validation Otsu                         NEXT
Full validation paired analysis              PLANNED
Preprocessing decision freeze                PLANNED
Held-out test evaluation                     PLANNED
Final EXP003 conclusion                      PLANNED

EXP003                                       IN PROGRESS
```