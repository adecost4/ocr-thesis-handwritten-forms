# Thesis Biweekly Progress Report

**Reporting Period:** October 7 – October 20, 2026  
**Student:** Aloyson De Costa

## Progress This Period

Over the past two weeks, my main focus was completing the **TrOCR baseline experiment on the IAM Handwriting Database (EXP002)** and performing a systematic analysis of its recognition errors.

### 1. Completed EXP002 — Pretrained TrOCR on IAM

I completed the formal evaluation of the pretrained `microsoft/trocr-base-handwritten` model using the established IAM dataset split.

As part of this work, I corrected and validated the IAM dataset preparation pipeline, generated the training, validation, and test manifests, and verified that there was no overlap between the generated splits.

After excluding IAM line annotations marked with segmentation errors (`status = err`), the usable splits contained:

- **Training:** 5,419 lines
- **Validation:** 1,539 lines
- **Test:** 1,480 lines

The pretrained TrOCR model was evaluated on all **1,480 usable test lines** without additional IAM-specific fine-tuning or image preprocessing.

The final baseline results were:

| Metric | Result |
|---|---:|
| CER | **3.33%** |
| WER | **8.63%** |
| Exact Match | **56.89%** |
| Exact Predictions | **842 / 1,480** |

This provides a fixed quantitative baseline for comparison with future experiments.

### 2. Systematic Error Analysis

Following the baseline evaluation, I analyzed the **638 non-exact predictions** to better understand the types of recognition errors produced by TrOCR.

I created a reproducible diagnostic sample of **125 predictions**, consisting of:

- 50 highest-CER failures
- 50 randomly selected failures
- 25 low-CER but non-exact failures

I manually reviewed the original handwriting images, ground-truth transcriptions, and TrOCR predictions and classified the observed errors.

The most common error categories in the reviewed sample were:

| Error Category | Count |
|---|---:|
| Word substitution | 72 |
| Character substitution | 62 |
| Punctuation | 24 |
| Spacing | 21 |
| Capitalization | 1 |

The analysis also showed that severe high-CER failures were frequently associated with difficult handwriting, while many low-CER failures involved relatively small character or spacing differences.

An important observation was that many recognition failures occurred even on images that appeared to have good image quality. This suggests that preprocessing should be evaluated experimentally rather than assuming that it will automatically improve recognition.

I documented the analysis and generated supporting tables and figures in the GitHub repository.

### 3. Literature Review — HTR-VT

I reviewed **“HTR-VT: Handwritten Text Recognition with Vision Transformer.”**

This paper provided another useful perspective on Transformer-based handwriting recognition. Unlike TrOCR's pretrained encoder-decoder architecture, HTR-VT combines:

`CNN feature extraction → Transformer encoder → CTC`

and focuses on data-efficient training without requiring large-scale external pretraining.

I also studied its use of **span feature masking** and **Sharpness-Aware Minimization (SAM)** and compared the HTR-VT architecture with both TrOCR and CRNN.

This provides a useful alternative architecture to consider later when comparing recognition approaches and their error behavior.

### 4. Started EXP003 — Controlled Image Preprocessing

I have started the next experiment, **EXP003**, which investigates whether controlled image preprocessing can improve TrOCR recognition performance.

The planned preprocessing techniques include grayscale conversion, thresholding, contrast enhancement, denoising, and later deskewing.

Rather than repeatedly optimizing against the test set, I plan to first evaluate preprocessing approaches using a reproducible subset of the **IAM validation split**, select promising approaches, and then evaluate the selected method on the held-out test set.

The EXP002 baseline will remain the reference for the final comparison.

---

## Next Steps

For the next two weeks, I plan to:

1. Complete **EXP003 — Controlled Image Preprocessing** and compare CER, WER, and Exact Match across preprocessing conditions.
2. Analyze whether preprocessing improves particular error types identified during the EXP002 error analysis.
3. Begin exploring **template/document alignment** for structured forms.
4. Continue the literature review, particularly around document alignment, layout-aware document understanding, and structured field extraction.
5. Begin developing the first simple **template-based field extraction pipeline**, where known field locations can be cropped and passed to the handwriting-recognition model.

These steps will begin moving the project from general handwritten line recognition toward the main thesis problem of **structured handwritten-form recognition**.

---

## Midterm Progress Review

I have also planned a **midterm thesis progress review for Tuesday, October 27 at 11:00 AM**.

For the review, I plan to summarize:

- literature reviewed so far,
- the TrOCR/IAM baseline,
- EXP002 methodology and results,
- systematic error-analysis findings,
- current EXP003 preprocessing work,
- and the proposed direction toward template alignment and structured field extraction.

The goal of the review is to assess the progress made so far and confirm that the next experimental direction is appropriate for the thesis.