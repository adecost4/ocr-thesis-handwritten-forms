# Week 05–06 Notes — OCR Thesis Research

## Week Overview

The past two weeks marked a transition from theoretical learning toward practical and quantitative experimentation.

The primary focus was on:

- understanding the IAM Handwriting Database,
- implementing evaluation metrics for handwritten text recognition,
- establishing a pretrained TrOCR baseline evaluation workflow,
- running initial quantitative experiments on IAM,
- performing early recognition-error analysis,
- and studying the FUNSD dataset to better understand structured document analysis beyond OCR.

---

# Activities Completed

## IAM Handwriting Dataset

Studied the IAM Handwriting Database as the primary benchmark dataset for offline handwritten text recognition.

Topics explored:

- dataset organization,
- writer information,
- form-level, line-level, and word-level samples,
- ground-truth transcriptions,
- dataset splits,
- and benchmark usage in handwritten text recognition research.

### Key Observation

IAM is highly suitable for evaluating handwritten text recognition models.

However, IAM is being used in this research primarily as a handwriting-recognition benchmark. It does not directly represent the complete structured-form problem central to the thesis, where document layout, predefined fields, field relationships, and template information may also need to be considered.

---

# Evaluation Metrics

Implemented standard evaluation metrics for handwritten text recognition.

The current evaluation pipeline uses:

- Character Error Rate (CER)
- Word Error Rate (WER)
- Exact Match / Field Accuracy

A dedicated `metrics.py` module was created to compare OCR predictions against ground-truth transcriptions.

## Character Error Rate (CER)

CER measures character-level recognition errors.

It provides a fine-grained indication of transcription quality.

```text
CER = 0
```

represents a perfect character-level prediction.

---

## Word Error Rate (WER)

WER measures recognition errors at the word level.

It provides a higher-level measure of OCR performance.

```text
WER = 0
```

represents a perfect word-level prediction.

---

## Exact Match / Field Accuracy

Exact Match determines whether the complete predicted string matches the ground truth.

```text
1 = exact match
0 = mismatch
```

This metric may become particularly important for structured forms, where fields such as:

- names,
- dates,
- IDs,
- phone numbers,
- and numerical values

may require completely correct transcription.

---

# TrOCR + IAM Baseline Experiment

## Experiment 002 — Pretrained TrOCR on IAM

Started the first quantitative baseline experiment using:

```text
microsoft/trocr-base-handwritten
```

### Research Question

> How well does a pretrained TrOCR model recognize handwritten IAM text-line samples without additional fine-tuning?

No IAM-specific fine-tuning or additional image preprocessing was applied during these initial evaluations.

---

## Evaluation Workflow

The evaluation pipeline is:

```text
IAM Line Image
        ↓
TrOCR Processor
        ↓
Pretrained TrOCR
        ↓
Predicted Text
        ↓
Ground Truth Comparison
        ↓
CER / WER / Exact Match
```

The workflow currently supports:

- loading IAM line images,
- running pretrained TrOCR inference,
- comparing predictions with ground truth,
- computing CER,
- computing WER,
- computing Exact Match,
- saving predictions,
- identifying best and worst predictions,
- and recording aggregate experiment results.

---

# EXP002 Exploratory Results

The evaluation was progressively expanded using:

```text
N = 20
N = 50
N = 100
```

## Results

| Samples | Average CER | Average WER | Exact Matches | Exact Match Rate |
|---:|---:|---:|---:|---:|
| 20 | 2.39% | 5.99% | 15 / 20 | 75% |
| 50 | 1.08% | 2.81% | 43 / 50 | 86% |
| 100 | 1.15% | 3.68% | 81 / 100 | 81% |

The N=50 and N=100 CER values were relatively similar:

```text
N=50  → CER = 1.08%
N=100 → CER = 1.15%
```

The smaller N=20 experiment produced a higher CER of 2.39%, indicating that very small evaluation subsets can be strongly affected by individual difficult predictions.

These results are currently treated as **exploratory pipeline-validation results** because the experiments use the first N usable samples from the generated IAM manifest rather than an established writer-independent test split.

---

# Initial Error Analysis

Reviewing the TrOCR predictions revealed several recurring types of recognition errors.

## Character-Level Errors

Example:

```text
defended
→
defenched
```

Most of the word is recognized correctly, but one or more characters are incorrectly predicted.

---

## Punctuation Errors

Example:

```text
talks .
→
talks ,
```

or:

```text
Federation .
→
Federation
```

The textual content may be correct while punctuation differs from the ground truth.

---

## Spacing / Tokenization Errors

Example:

```text
M Ps
→
MPs
```

The model prediction is linguistically reasonable but differs from the IAM ground-truth transcription format.

---

## Language-Like Substitutions

One particularly interesting example was:

```text
Ground Truth:
institution .

Prediction:
institutionalism .
```

Rather than producing random characters, the model generated a valid and linguistically related English word.

Another observed example was:

```text
Ground Truth:
Robertson later disclosed he had sent a letter

Prediction:
Robertson later disclosed the fact sent a letter
```

These errors suggest that the autoregressive decoder may sometimes produce linguistically plausible text when visual evidence is ambiguous.

This is currently an observation rather than a conclusion and requires further investigation.

---

# Key Experimental Observation

The exploratory results demonstrate why multiple evaluation metrics are useful.

At N=100:

```text
Average CER:       1.15%
Average WER:       3.68%
Exact Match Rate: 81%
```

A prediction may have a very low CER while still failing Exact Match because of a single character, punctuation mark, capitalization difference, or spacing error.

This distinction may become especially important for structured forms, where even one incorrect character in an ID, date, or numerical field could make the extracted value unusable.

---

# Literature Review

## Paper #3 — FUNSD

**FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents**

**Authors:** Jaume et al.

The paper was studied to understand the challenges introduced when moving from handwritten text recognition toward structured document understanding.

### Key Topics Studied

- form understanding,
- document layout,
- semantic entities,
- word grouping,
- question-answer relationships,
- entity linking,
- noisy scanned documents,
- and structured information extraction.

### Key Understanding

IAM is being used primarily to study:

```text
Handwriting Recognition
```

while FUNSD introduces:

```text
Form Understanding
```

Form understanding requires more than recognizing the text.

A system may also need to determine:

```text
What text is present?
        ↓
Where is it located?
        ↓
What role does it have?
        ↓
Which field does it belong to?
        ↓
What other entity is it related to?
```

This is directly relevant to the transition from standard handwriting recognition toward structured handwritten forms.

---

# IAM and FUNSD — Complementary Roles

The two datasets address different aspects of the thesis problem.

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

IAM provides a benchmark for recognizing handwritten text.

FUNSD provides concepts for understanding:

- layout,
- semantic fields,
- entities,
- and relationships.

The eventual thesis problem may require ideas from both areas.

---

# Current Research Direction

The current working thesis pipeline is:

```text
Structured Form
        ↓
Template / Document Alignment
        ↓
Field Detection & Extraction
        ↓
Handwritten Text Recognition
        ↓
Field-Aware Processing
        ↓
Structured Output
```

The immediate objective is to establish reliable and reproducible baseline experiments before developing or evaluating more advanced template-aware or field-aware approaches.

---

# Key Takeaways

- IAM provides a strong benchmark for offline handwritten text recognition.
- CER and WER provide quantitative measures of OCR recognition performance.
- Exact Match may be especially important for structured-form fields.
- Pretrained TrOCR already performs strongly on the selected exploratory IAM samples.
- Small evaluation subsets can produce unstable aggregate results.
- N=50 and N=100 produced relatively similar character-level error rates.
- Error analysis revealed character, punctuation, spacing, and language-like substitution errors.
- FUNSD demonstrates that structured form understanding requires more than OCR alone.
- A defensible baseline should use an established writer-independent IAM test split before moving to model improvements.

---

# Challenges Encountered

The main challenges during this period included:

- understanding the IAM dataset organization and annotations,
- preparing IAM line-level data for evaluation,
- creating a reproducible CSV-based evaluation workflow,
- implementing CER, WER, and Exact Match,
- managing Python environments and TrOCR dependencies,
- designing experiment outputs so results from different runs are preserved,
- distinguishing exploratory evaluation from benchmark-level evaluation,
- and connecting handwriting recognition with the broader structured-form problem.

These implementation challenges also helped improve the reproducibility and organization of the research codebase.

---

# Next Two-Week Goals

## 1. Complete the EXP002 Baseline

The highest priority is to move from exploratory subsets to a reproducible IAM evaluation.

Planned workflow:

```text
IAM
 │
 ├── train.csv
 ├── validation.csv
 └── test.csv
          ↓
   Pretrained TrOCR
          ↓
   Complete Test Evaluation
          ↓
   CER / WER / Exact Match
```

Tasks:

- prepare an established writer-independent IAM split,
- generate train, validation, and test manifests,
- verify that the splits do not overlap,
- evaluate pretrained TrOCR on all valid test samples,
- record the final EXP002 baseline metrics,
- and compare the test-set results with the exploratory N=20, N=50, and N=100 runs.

---

## 2. Systematic Error Analysis

After establishing the test-set baseline:

- identify the highest-error predictions,
- categorize common error types,
- study handwriting styles associated with recognition failures,
- investigate punctuation and spacing errors,
- investigate language-like substitutions,
- and determine which errors are most relevant to structured-form fields.

---

## 3. Controlled Preprocessing Experiments

Begin controlled OpenCV preprocessing experiments.

Potential preprocessing operations include:

- grayscale conversion,
- thresholding,
- denoising,
- contrast enhancement,
- resizing,
- and deskewing.

Each preprocessing method should be compared against the same baseline using CER and WER rather than relying only on visual inspection.

---

## 4. Structured Form Research

Study techniques related to:

- document alignment,
- template alignment,
- field detection,
- field extraction,
- layout understanding,
- and field relationships.

The goal is to understand how structural information could eventually complement handwriting recognition.

---

## 5. Literature Review

Continue the literature review with:

- HTR-VT,
- Transformer-based handwritten text recognition,
- layout-aware document understanding,
- and template-based form processing.

The objective is to identify limitations in existing approaches that could lead to a focused and testable thesis hypothesis.

---

# Midterm Progress Presentation / Demo

After Fall Break, prepare a short thesis progress presentation/demo covering:

1. Research motivation
2. Literature review
   - CRNN
   - TrOCR
   - FUNSD
3. IAM Handwriting Database
4. TrOCR evaluation pipeline
5. CER / WER / Exact Match
6. EXP002 exploratory results
7. Recognition error analysis
8. Established IAM baseline
9. Structured-form research direction
10. Planned next experiments

A short live demonstration can include:

```text
IAM Image
    ↓
TrOCR
    ↓
Prediction
    ↓
Ground Truth
    ↓
CER / WER
```

---

# Research Progression

The research currently follows this progression:

```text
Literature Review
       ↓
Basic TrOCR Inference
       ↓
Evaluation Metrics
       ↓
IAM Dataset Preparation
       ↓
Exploratory TrOCR Baseline
       ↓
Established IAM Test Baseline
       ↓
Error Analysis
       ↓
Controlled Preprocessing
       ↓
Structured Form Understanding
       ↓
Potential Research Hypothesis
```

---

# Weekly Reflection

The past two weeks represented an important transition from literature review and conceptual learning toward quantitative experimentation.

By studying IAM, implementing standard HTR evaluation metrics, and running pretrained TrOCR across progressively larger subsets, I established a working experimental pipeline and began collecting measurable baseline results.

The N=20, N=50, and N=100 evaluations also demonstrated the importance of sample size and careful experimental design. In particular, the smaller pilot was more sensitive to individual recognition failures, while the larger exploratory runs produced more stable character-level results.

Reviewing FUNSD broadened the research perspective beyond OCR by introducing spatial layout, semantic entities, and relationships between form fields.

The next major milestone is to replace exploratory subset evaluation with an established writer-independent IAM test-set baseline. This will provide a more defensible reference point for subsequent preprocessing, fine-tuning, and structured-form experiments.