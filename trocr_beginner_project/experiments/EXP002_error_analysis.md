# EXP002 — Systematic Error Analysis

## Objective

Perform a systematic qualitative and quantitative analysis of recognition errors produced by pretrained TrOCR during the EXP002 IAM test-set evaluation.

The purpose of this analysis is to move beyond aggregate CER and WER values and understand **what types of errors TrOCR makes, when severe failures occur, and which error patterns may motivate future experiments**.

---

## Baseline

The analysis is based on the completed EXP002 baseline.

### Model

```text
microsoft/trocr-base-handwritten
```

### Dataset

IAM Handwriting Database

### Evaluation Set

Writer-independent IAM test manifest containing only usable line annotations with:

```text
status = ok
```

### Baseline Results

| Metric | Result |
|---|---:|
| Test Samples | 1,480 |
| Average CER | 3.33% |
| Average WER | 8.63% |
| Exact Matches | 842 / 1,480 |
| Exact Match Rate | 56.89% |
| Non-Exact Predictions | 638 / 1,480 |

Although the average CER was relatively low, 638 predictions contained at least one difference from the ground truth.

This distinction is important for the broader thesis because structured-form fields such as IDs, dates, names, account numbers, and numerical values may require completely correct transcription.

---

# Research Question

> **RQ1: What types of recognition errors contribute most to pretrained TrOCR's incorrect predictions on the IAM test set?**

Additional exploratory questions include:

- What types of errors occur among the most severe recognition failures?
- How do high-CER errors differ from low-CER but non-exact errors?
- Are severe errors associated with difficult handwriting?
- Are recognition failures frequently associated with obvious image-quality problems?
- Which observed errors might potentially be addressed by preprocessing, model adaptation, or field-specific constraints?

---

# Methodology

## Error Population

The completed EXP002 evaluation contained:

```text
Total predictions:     1,480
Exact predictions:       842
Non-exact predictions:   638
```

The 638 non-exact predictions formed the population considered for error analysis.

---

## Diagnostic Sample Selection

Manually reviewing all 638 failures was not necessary for the initial analysis.

Instead, a targeted diagnostic sample of 125 unique non-exact predictions was created.

| Selection Group | Samples | Purpose |
|---|---:|---|
| High CER | 50 | Investigate severe recognition failures |
| Random | 50 | Investigate more typical recognition failures |
| Low CER | 25 | Investigate minor errors that still fail Exact Match |
| **Total** | **125** | |

The high-CER samples were selected by sorting incorrect predictions by CER in descending order.

The low-CER samples were selected from the remaining non-exact predictions by sorting CER in ascending order.

The random samples were selected from the remaining predictions using:

```python
random_state=42
```

to make the selection reproducible.

No sample appears in more than one group.

---

## Important Sampling Limitation

The 125 samples form a **targeted diagnostic sample**, not a random representative sample of all 638 incorrect predictions.

The sample deliberately oversamples:

- the 50 highest-CER failures,
- and the 25 lowest-CER non-exact failures.

Therefore, category percentages from this analysis **must not be interpreted as estimates of the natural prevalence of error categories across all 638 EXP002 failures**.

The results describe patterns within the manually reviewed diagnostic sample.

---

# Manual Review Procedure

For each selected prediction, the following were compared:

```text
Original IAM Line Image
        ↓
Ground Truth
        ↓
TrOCR Prediction
        ↓
CER / WER
        ↓
Manual Error Classification
```

The original handwriting image was inspected before assigning handwriting-difficulty or image-condition judgments.

---

# Annotation Fields

Each manually reviewed sample contains:

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

Multiple error categories were allowed for a single prediction.

Multiple categories were separated using:

```text
;
```

---

# Error Categories

The following error categories were used during manual review:

```text
Character substitution
Insertion
Deletion
Word substitution
Spacing
Punctuation
Capitalization
Possible handwriting ambiguity
Possible image-quality issue
Possible language-generation error
Other
```

The final manually assigned categories observed in the reviewed sample were primarily:

- Word substitution
- Character substitution
- Punctuation
- Spacing
- Capitalization

---

# Handwriting Difficulty

Handwriting difficulty was manually classified as:

```text
Easy
Moderate
Difficult
```

This judgment describes how difficult the handwriting appeared to interpret visually.

It should not be interpreted as an objective measure of handwriting complexity.

---

# Image Conditions

Image condition was also inspected manually.

Observed descriptions included:

- Good
- Blur
- Cropping problems
- combinations of these conditions

These labels are qualitative observations rather than objective image-quality measurements.

---

# Results

## Error Category Distribution

Across the 125 manually reviewed samples:

| Error Category | Count | % of Reviewed Samples |
|---|---:|---:|
| **Word substitution** | **72** | **57.6%** |
| **Character substitution** | **62** | **49.6%** |
| Punctuation | 24 | 19.2% |
| Spacing | 21 | 16.8% |
| Capitalization | 1 | 0.8% |

Multiple categories could be assigned to a single prediction.

Therefore:

```text
category counts > number of reviewed samples
```

and percentages do not sum to 100%.

---

## Figure 1 — Error Category Distribution

The overall distribution of manually assigned error categories is stored in:

```text
results/exp002/figures/exp002_error_categories.png
```

The figure shows that word substitutions and character substitutions were the dominant error types within the diagnostic sample.

---

# Error Categories by Diagnostic Group

Breaking the categories down by sample-selection group reveals substantial differences between severe and minor recognition failures.

| Error Category | High CER | Random | Low CER |
|---|---:|---:|---:|
| Word substitution | 49 | 22 | 1 |
| Character substitution | 25 | 22 | 15 |
| Punctuation | 11 | 12 | 1 |
| Spacing | 7 | 6 | 8 |
| Capitalization | 0 | 0 | 1 |

---

## Figure 2 — Error Categories by Diagnostic Group

The comparison is stored in:

```text
results/exp002/figures/exp002_categories_by_group.png
```

This comparison reveals that the nature of recognition errors changes substantially with error severity.

---

# High-CER Failures

Among the 50 highest-CER predictions:

```text
Word substitution        49 / 50
Character substitution   25 / 50
Punctuation              11 / 50
Spacing                   7 / 50
```

Word substitution occurred in:

```text
98%
```

of the high-CER diagnostic group.

This indicates that the most severe TrOCR failures were generally not limited to isolated character differences.

Instead, they frequently involved incorrect words or larger transcription differences.

Character substitutions also appeared frequently, but word-level errors were the dominant pattern in this group.

---

# Random Non-Exact Predictions

Among the 50 randomly selected remaining non-exact predictions:

```text
Word substitution        22 / 50
Character substitution   22 / 50
Punctuation              12 / 50
Spacing                   6 / 50
```

Word and character substitutions occurred at similar frequencies in this group.

This suggests that more typical incorrect predictions contain a mixture of:

- word-level recognition errors,
- character-level errors,
- punctuation differences,
- and spacing differences.

---

# Low-CER but Non-Exact Predictions

Among the 25 lowest-CER non-exact predictions:

```text
Character substitution   15 / 25
Spacing                   8 / 25
Word substitution         1 / 25
Punctuation               1 / 25
Capitalization            1 / 25
```

Unlike the high-CER group, word substitution was uncommon.

Instead, minor failures were dominated by:

- character substitutions,
- spacing differences,
- and occasional formatting differences.

This provides an explanation for the difference between the EXP002 CER and Exact Match results.

A prediction may differ from the ground truth by only one character or word boundary and therefore achieve a very low CER while still failing Exact Match.

---

# Handwriting Difficulty Analysis

Across all 125 manually reviewed samples:

| Handwriting Difficulty | Count | Percentage |
|---|---:|---:|
| Difficult | 66 | 52.8% |
| Moderate | 40 | 32.0% |
| Easy | 19 | 15.2% |

Therefore:

```text
84.8%
```

of the manually reviewed errors were judged to contain either moderate or difficult handwriting.

---

## High-CER Handwriting Difficulty

Among the 50 highest-CER failures:

| Difficulty | Count | Percentage |
|---|---:|---:|
| Difficult | 34 | 68% |
| Moderate | 13 | 26% |
| Easy | 3 | 6% |

The majority of severe failures were therefore associated with handwriting manually classified as difficult.

This suggests an association between handwriting difficulty and severe recognition errors within the diagnostic sample.

However, this analysis does **not establish causality**.

It cannot be concluded from this experiment alone that difficult handwriting caused the recognition failures.

---

## Figure 3 — Handwriting Difficulty

The handwriting-difficulty distribution is stored in:

```text
results/exp002/figures/exp002_handwriting_difficulty.png
```

---

# Image Condition Analysis

The manually reviewed samples contained the following image-condition annotations:

```text
Good                       80
Cropping problems          32
Blur                       10
Good + cropping problems    2
Blur + cropping problems    1
```

A majority of reviewed failures therefore occurred on images that were manually considered visually good.

Approximately:

```text
80 / 125 = 64%
```

of the reviewed errors were assigned the simple `Good` image-condition label.

This is an important observation.

Recognition failures cannot be attributed solely to visibly poor image quality.

---

# Key Findings

## 1. Word Substitutions Dominate Severe Failures

Word substitution appeared in 49 of the 50 highest-CER samples.

This indicates that severe recognition failures frequently involve larger word-level mistakes rather than only isolated character errors.

---

## 2. Character Errors Dominate Many Minor Failures

Character substitution appeared in 15 of the 25 low-CER non-exact predictions.

These errors may involve only a small textual difference while still causing the complete prediction to fail Exact Match.

This is particularly relevant to structured-form recognition.

For example:

```text
Student ID:
12345678
```

predicted as:

```text
12345673
```

may have a very low character error rate but still represent an incorrect field value.

---

## 3. Exact Match Provides Information Not Captured by CER Alone

EXP002 produced:

```text
CER:         3.33%
WER:         8.63%
Exact Match: 56.89%
```

The error analysis helps explain this difference.

Many non-exact predictions contain relatively small errors involving:

- individual characters,
- spacing,
- punctuation,
- or capitalization.

Therefore, low aggregate CER does not imply that complete text lines or structured fields are always correct.

---

## 4. Severe Failures Are Frequently Associated with Difficult Handwriting

Among the 50 highest-CER samples:

```text
68%
```

were manually classified as difficult handwriting.

Across the entire diagnostic sample:

```text
52.8%
```

were classified as difficult.

This suggests that handwriting variability and ambiguity should remain an important consideration in subsequent experiments.

---

## 5. Poor Image Quality Does Not Explain Most Errors

Most manually reviewed samples were not classified as obviously degraded.

A majority were labeled as having good image quality.

Therefore, applying generic preprocessing to every image should not automatically be expected to improve recognition.

Some transformations could potentially remove useful stroke information from already good-quality handwriting.

---

## 6. Error Type Changes with Error Severity

The diagnostic groups reveal different failure patterns.

```text
High CER
    ↓
Word substitutions dominate

Random failures
    ↓
Mixture of word and character substitutions

Low CER
    ↓
Character substitutions and spacing become more prominent
```

This suggests that treating all OCR errors as a single category would hide meaningful differences in model behavior.

---

# Implications for Structured Handwritten Forms

The results are particularly relevant to the thesis goal of recognizing structured handwritten form fields.

For general text recognition, a prediction containing a single incorrect character may still appear highly accurate according to CER.

For structured fields such as:

```text
Name
Date
Student ID
Phone Number
Account Number
Postal Code
```

a single-character error may make the extracted value incorrect.

Therefore, future structured-form experiments should continue reporting:

```text
CER
WER
Exact Match / Field Accuracy
```

rather than relying on CER alone.

Field type may also provide useful contextual constraints.

For example:

```text
Field type: DATE
Expected structure: MM/DD/YYYY
```

or:

```text
Field type: STUDENT ID
Expected characters: digits
Expected length: fixed
```

Such constraints may eventually provide a way to reduce errors that a general unconstrained OCR model cannot detect.

---

# Implications for EXP003

The original plan for EXP003 is controlled image preprocessing.

The error analysis provides a more evidence-based motivation for that experiment.

Some reviewed samples exhibited:

- blur,
- cropping problems,
- or other image-condition issues.

These cases may potentially benefit from preprocessing.

However, because many failures occurred on images judged to have good quality, preprocessing should **not** be assumed to improve recognition globally.

EXP003 should therefore test preprocessing as a controlled experimental variable.

Potential transformations include:

```text
Grayscale
Thresholding
Contrast enhancement
Denoising
Deskewing
```

Each transformation should be evaluated independently before combining transformations.

---

# EXP003 Experimental Principle

The EXP002 test set should remain the held-out evaluation set.

Preprocessing approaches should first be developed and compared using the IAM validation split.

The workflow should be:

```text
IAM Validation Set
        ↓
Baseline
        vs.
Preprocessing A
        vs.
Preprocessing B
        vs.
Preprocessing C
        ↓
Select promising approach
        ↓
IAM Test Set
        ↓
Final comparison against EXP002
```

This reduces the risk of repeatedly optimizing preprocessing decisions against the held-out test set.

The fixed EXP002 reference remains:

```text
CER:         3.33%
WER:         8.63%
Exact Match: 56.89%
```

---

# Possible Future Research Directions

The error analysis suggests several possible intervention directions.

## Image-Based Intervention

Errors associated with blur, cropping, contrast, or skew may potentially benefit from image preprocessing.

This motivates EXP003.

---

## Model Adaptation

Errors associated with difficult handwriting or character ambiguity may potentially benefit from:

- IAM-specific fine-tuning,
- additional handwriting training data,
- or alternative HTR architectures.

---

## Decoder / Context Investigation

Some word substitutions may produce linguistically plausible but visually incorrect predictions.

These cases may warrant further investigation of the relationship between:

```text
visual evidence
+
autoregressive decoding
+
language context
```

However, the current analysis does not establish decoder language modeling as the cause of these errors.

---

## Field-Aware Recognition

Structured forms provide information that generic handwriting recognition does not.

Examples include:

```text
field type
expected data type
expected length
valid character set
known template position
```

A future research direction could investigate whether such constraints improve Exact Match accuracy for structured handwritten fields.

---

# Limitations

## Targeted Diagnostic Sampling

The 125 manually reviewed predictions are not a representative random sample of all 638 errors.

The selection deliberately includes:

```text
50 highest CER
50 random
25 lowest CER
```

Therefore, overall category percentages should only be interpreted as descriptive statistics for this diagnostic sample.

---

## Manual Annotation Subjectivity

Handwriting difficulty and image condition were manually judged.

Different reviewers could potentially assign different labels.

Future work could improve reliability by:

- defining more formal annotation criteria,
- using multiple annotators,
- or measuring inter-rater agreement.

---

## Multiple Error Categories

A single prediction may contain several error types.

Therefore, category counts overlap and percentages may sum to more than 100%.

---

## No Causal Claims

The analysis identifies associations and recurring patterns.

It does not establish that:

- difficult handwriting causes recognition failure,
- poor image quality causes OCR errors,
- or decoder language modeling causes word substitutions.

Controlled experiments would be required to test those hypotheses.

---

# Conclusion

The systematic error analysis extends EXP002 beyond aggregate OCR metrics by examining how pretrained TrOCR fails on IAM handwriting.

A targeted diagnostic sample of 125 non-exact predictions was manually reviewed, including severe, typical, and minor recognition failures.

The dominant observed error categories were:

```text
Word substitution        72 / 125
Character substitution   62 / 125
Punctuation              24 / 125
Spacing                  21 / 125
Capitalization            1 / 125
```

The analysis revealed an important distinction between severe and minor failures.

Severe high-CER errors were dominated by word substitutions, with 49 of 50 high-CER samples containing a word-level substitution.

In contrast, low-CER but non-exact predictions were dominated by character substitutions and spacing differences.

The manual handwriting analysis also showed that 68% of the highest-CER samples were classified as difficult handwriting.

At the same time, most reviewed errors did not occur on obviously poor-quality images, indicating that image degradation alone does not explain TrOCR's failures.

These findings help explain why the EXP002 baseline achieved a relatively low CER of 3.33% while only 56.89% of test lines were exact matches.

For structured handwritten forms, this distinction is important because even small transcription errors may invalidate fields such as IDs, dates, names, or numerical values.

The analysis therefore provides an evidence-based foundation for subsequent experiments rather than applying model changes or preprocessing techniques arbitrarily.

---

# Next Experiment

## EXP003 — Controlled Image Preprocessing

### Research Question

> **Does controlled image preprocessing improve TrOCR handwriting-recognition accuracy compared with the unmodified EXP002 baseline?**

Candidate preprocessing methods include:

```text
Grayscale
Thresholding
Contrast enhancement
Denoising
Deskewing
```

Preprocessing methods will first be investigated using the IAM validation split.

A selected approach can then be evaluated on the held-out IAM test set and compared against:

```text
EXP002 Baseline

CER:         3.33%
WER:         8.63%
Exact Match: 56.89%
```

---

# Status

```text
EXP002 baseline evaluation               ✓
1,480-line IAM test evaluation           ✓
638 non-exact predictions identified     ✓
125-sample diagnostic set generated      ✓
125 samples manually reviewed            ✓
Error categories generated               ✓
Handwriting difficulty analyzed          ✓
Image conditions analyzed                ✓
Error-category figures generated         ✓
Systematic error analysis documented     ✓

EXP002 ERROR ANALYSIS                     COMPLETE

Paper #4 — HTR-VT                        NEXT
EXP003 — Controlled preprocessing         NEXT
Template alignment                       PLANNED
Field extraction                         PLANNED
Structured-form hypothesis               FUTURE
```