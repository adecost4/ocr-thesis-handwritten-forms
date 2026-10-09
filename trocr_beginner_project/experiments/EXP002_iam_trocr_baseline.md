# EXP002 — Pretrained TrOCR on IAM

## Objective

Evaluate the performance of Microsoft's pretrained TrOCR handwriting model on subsets of the IAM Handwriting Database without additional fine-tuning.

This experiment establishes an initial handwriting-recognition baseline before official test-set evaluation and task-specific fine-tuning.

---

## Research Question

How well does a pretrained TrOCR model recognize handwritten text from the IAM dataset before task-specific fine-tuning?

---

## Hypothesis

This is a baseline experiment.

No improvement hypothesis is being tested. The purpose is to measure the out-of-the-box performance of pretrained TrOCR, validate the evaluation pipeline, and identify recognition errors before conducting a formal evaluation using an established IAM test split.

---

## Model

`microsoft/trocr-base-handwritten`

The pretrained checkpoint was used directly without additional IAM fine-tuning.

---

## Dataset

**IAM Handwriting Database**

### Evaluation Level

- Offline handwritten text
- Cropped line images
- Ground-truth line transcriptions

The IAM data was converted into a CSV manifest containing:

```text
id
image
text
```

where:

- `id` identifies the IAM text line
- `image` contains the path to the line image
- `text` contains the ground-truth transcription

---

## Sample Size

The baseline was evaluated incrementally using three sample sizes:

```text
N = 20
N = 50
N = 100
```

The samples correspond to the first N usable entries in the generated IAM manifest.

The purpose of increasing the sample size was to verify the evaluation pipeline and observe whether aggregate metrics remained reasonably stable as additional samples were included.

The progression was:

```text
20 → 50 → 100
```

These runs are exploratory and should not be interpreted as official IAM benchmark results because they do not use an established IAM test split.

The next stage of EXP002 will evaluate the model using an established IAM test split.

---

## Preprocessing

For each IAM line:

1. Load the image using Pillow.
2. Convert the image to RGB.
3. Process the image using the TrOCR processor.
4. Convert the processed image into the pixel values expected by TrOCR.
5. Generate text using the pretrained TrOCR model.
6. Compare the generated text against the IAM ground truth.

No additional:

- image enhancement
- thresholding
- deskewing
- denoising
- data augmentation

was applied.

---

## Inference Pipeline

```text
IAM Line Image
      ↓
TrOCR Processor
      ↓
Pixel Values
      ↓
Pretrained TrOCR
      ↓
Generated Text
      ↓
Ground Truth Comparison
      ↓
CER / WER / Exact Match
```

---

## Metrics

### Character Error Rate (CER)

CER measures character-level differences between the ground-truth transcription and model prediction.

Lower is better.

```text
CER = 0
```

indicates a perfect character-level transcription.

---

### Word Error Rate (WER)

WER measures word-level differences between the ground truth and prediction.

Lower is better.

```text
WER = 0
```

indicates a perfect word-level transcription.

---

### Exact Match

Exact Match determines whether the complete prediction matches the ground truth.

```text
1 = prediction exactly matches ground truth
0 = prediction differs from ground truth
```

Exact Match is particularly relevant to the future structured-form task because some fields, such as IDs, dates, names, or numerical values, may require completely correct transcription.

---

# Results

## Exploratory Sample Size Comparison

Before running the established IAM test evaluation, the pipeline was validated using progressively larger subsets of the generated IAM manifest.

| Run | Samples | Average CER | Average WER | Exact Matches | Exact Match Rate |
|---|---:|---:|---:|---:|---:|
| Pilot | 20 | 2.39% | 5.99% | 15 / 20 | 75.00% |
| Expanded | 50 | 1.08% | 2.81% | 43 / 50 | 86.00% |
| Expanded | 100 | 1.15% | 3.68% | 81 / 100 | 81.00% |

These experiments used the first N usable entries in the generated IAM manifest.

Their primary purpose was to validate:

- IAM data loading,
- TrOCR inference,
- CER/WER computation,
- Exact Match computation,
- result storage,
- and error-analysis workflow.

Because these samples were not selected using the established writer-independent test split, these values are treated as exploratory results rather than the final EXP002 baseline.

---

## Established IAM Split Preparation

After validating the pipeline, the IAM manifest-generation process was corrected and the established writer-independent split definitions were applied.

The IAM `lines.txt` annotation file contained:

```text
Total line annotations: 13,353
Status = ok:            11,344
Status = err:            2,009
Missing images:              0
```

Only line images marked:

```text
status = ok
```

were retained.

Lines marked:

```text
status = err
```

were excluded from the experimental manifests.

After applying the split definitions, the usable datasets contained:

| Split | Defined Lines | Usable `ok` Lines | Excluded `err` Lines |
|---|---:|---:|---:|
| Train | 6,161 | 5,419 | 742 |
| Validation | 1,840 | 1,539 | 301 |
| Test | 1,861 | 1,480 | 381 |

All missing split IDs were systematically checked.

The diagnostic results showed:

```text
Missing despite status=ok: 0
Missing/unknown annotation: 0
```

for training, validation, and test sets.

Therefore, all excluded split samples were explained by IAM annotations marked `err`.

Additional overlap checks were also performed between the generated splits.

```text
Train vs Validation: PASS
Train vs Test:       PASS
Validation vs Test:  PASS
```

This provided the final dataset used for the formal EXP002 evaluation.

---

# Final EXP002 Baseline

The pretrained:

```text
microsoft/trocr-base-handwritten
```

model was evaluated on all:

```text
1,480
```

usable line images from the writer-independent IAM test manifest.

No IAM-specific fine-tuning was performed.

No additional preprocessing such as:

- thresholding,
- denoising,
- contrast enhancement,
- deskewing,
- or data augmentation

was applied.

## Final Results

| Metric | Result |
|---|---:|
| Samples Evaluated | **1,480** |
| Average CER | **3.33%** |
| Average WER | **8.63%** |
| Exact Matches | **842 / 1,480** |
| Exact Match Rate | **56.89%** |

These results represent the primary pretrained TrOCR baseline for EXP002.

---

# Exploratory vs Test-Set Results

The complete progression was:

| Evaluation | Samples | CER | WER | Exact Match Rate |
|---|---:|---:|---:|---:|
| Exploratory | 20 | 2.39% | 5.99% | 75.00% |
| Exploratory | 50 | 1.08% | 2.81% | 86.00% |
| Exploratory | 100 | 1.15% | 3.68% | 81.00% |
| **Writer-independent test** | **1,480** | **3.33%** | **8.63%** | **56.89%** |

The test-set evaluation produced higher CER and WER and a substantially lower Exact Match Rate than the exploratory subsets.

For example:

```text
N=100 exploratory CER = 1.15%

IAM test CER          = 3.33%
```

and:

```text
N=100 Exact Match     = 81.00%

IAM test Exact Match  = 56.89%
```

This demonstrates why the exploratory subsets should not be interpreted as representative estimates of overall IAM performance.

The first 100 usable manifest samples appear to have been easier for the pretrained model than the broader writer-independent test set.

The larger evaluation also contains greater variation in handwriting styles and recognition difficulty.

---

# Good Predictions

A substantial number of test lines were recognized perfectly.

The final test evaluation produced:

```text
842 exact matches
```

out of:

```text
1,480 test samples
```

giving:

```text
56.89% Exact Match
```

For these samples:

```text
CER = 0
WER = 0
Exact Match = 1
```

This demonstrates that pretrained TrOCR can recognize many IAM handwritten lines correctly without additional IAM-specific fine-tuning.

---

# Poor Predictions

The complete test evaluation also revealed difficult samples with substantially higher recognition errors than those observed during the small exploratory experiments.

Examples among the highest-error predictions included samples such as:

```text
p03-033-04
m04-038-04
p06-047-07
```

with character error rates substantially above the overall test-set average.

These difficult samples are useful for subsequent qualitative error analysis because they can help determine whether failures are associated with:

- handwriting style,
- ambiguous characters,
- image quality,
- long or complex lines,
- punctuation,
- word segmentation,
- or language-model behavior.

---

# Error Categories

The predictions observed throughout EXP002 suggest several recurring error categories.

## 1. Character Substitution

Example:

```text
defended
→
defenched
```

A visually ambiguous character causes an otherwise mostly correct word to be recognized incorrectly.

---

## 2. Character Insertion / Deletion

Individual characters may be added or omitted.

These errors can produce relatively low CER while still causing Exact Match failure.

---

## 3. Word-Level Substitution

Example:

```text
met
→
need
```

The predicted word differs from the ground truth while still being linguistically plausible.

---

## 4. Language-Like Generation Errors

Example:

```text
institution
→
institutionalism
```

Rather than generating unrelated characters, the decoder generated a valid and related English word.

Another observed example was:

```text
Robertson later disclosed he had sent a letter

→

Robertson later disclosed the fact sent a letter
```

These observations are consistent with the behavior expected from an autoregressive decoder that uses previously generated tokens as context.

However, this experiment does not establish that decoder language modeling is the direct cause of these errors.

---

## 5. Spacing / Tokenization Errors

Example:

```text
M Ps
→
MPs
```

The model output may be linguistically reasonable while differing from the IAM ground-truth transcription convention.

---

## 6. Punctuation Errors

Examples include:

```text
talks .
→
talks ,
```

and:

```text
Federation .
→
Federation
```

These differences affect strict CER, WER, and Exact Match even when the primary textual content is correct.

---

## 7. Capitalization Errors

Example:

```text
Though
→
though
```

The semantic content remains unchanged, but strict case-sensitive evaluation records the difference.

---

# Observations

## 1. Pretrained TrOCR Provides a Strong Starting Baseline

Without additional IAM-specific fine-tuning or image preprocessing, pretrained TrOCR achieved:

```text
CER:         3.33%
WER:         8.63%
Exact Match: 56.89%
```

on the 1,480 usable test lines.

This confirms that the pretrained model already provides a useful handwriting-recognition baseline for subsequent experiments.

---

## 2. Small Exploratory Subsets Overestimated Performance

The exploratory N=50 and N=100 evaluations produced substantially lower error rates than the complete test evaluation.

For example:

```text
N=100 CER:   1.15%
Test CER:    3.33%
```

This demonstrates the importance of using a defined evaluation protocol rather than drawing conclusions from small convenience subsets.

The exploratory runs were useful for validating the implementation, but the 1,480-line test evaluation provides a more defensible reference point.

---

## 3. Exact Match Reveals Errors Hidden by Low CER

The test-set CER was only 3.33%, yet Exact Match was 56.89%.

Therefore:

```text
43.11%
```

of evaluated lines contained at least one difference from the ground truth.

Many of these differences may involve only:

- one character,
- punctuation,
- spacing,
- capitalization,
- or a small word-level error.

This distinction is particularly important for structured-form applications.

For fields such as:

```text
Student ID
Date
Account Number
Phone Number
Name
```

even one incorrect character may make the extracted value unusable.

For this reason, Exact Match / Field Accuracy will remain an important metric as the research transitions from general handwriting recognition toward structured forms.

---

## 4. Error Distribution Is Not Uniform

Many test lines were recognized perfectly, while a smaller subset produced much larger errors.

This suggests that overall CER and WER are influenced disproportionately by difficult handwriting samples.

Future analysis should therefore examine not only aggregate metrics but also the distribution and characteristics of high-error samples.

---

## 5. Strict Evaluation Captures Formatting Differences

Punctuation, spacing, and capitalization differences contribute to the reported CER, WER, and Exact Match results.

Future experiments may consider both:

1. strict evaluation using the original IAM ground truth,
2. explicitly defined normalized evaluation for additional analysis.

However, the strict metrics from EXP002 should remain the primary baseline to ensure reproducibility.

---

# Limitations

## Exclusion of `err` Segmentation Samples

The evaluation uses only IAM line annotations marked:

```text
status = ok
```

Lines marked `err` were excluded.

As a result, the final test manifest contains:

```text
1,480
```

usable samples rather than all 1,861 IDs contained in the original test split definition.

This filtering decision should be considered when comparing EXP002 against results reported using different IAM preprocessing or segmentation protocols.

---

## No IAM-Specific Fine-Tuning

The model was evaluated directly from:

```text
microsoft/trocr-base-handwritten
```

without additional training on the generated IAM training set.

Therefore, EXP002 measures pretrained model performance rather than the performance of an IAM-adapted model.

---

## No Additional Preprocessing

No additional:

- thresholding,
- denoising,
- contrast enhancement,
- deskewing,
- or handwriting-specific preprocessing

was performed.

This provides a clean baseline for future controlled preprocessing experiments.

---

## Recognition Only

EXP002 evaluates cropped handwritten line recognition.

It does not evaluate:

- text detection,
- form-field detection,
- document alignment,
- layout understanding,
- semantic entity classification,
- field relationships,
- template information,
- or structured information extraction.

These problems are outside the scope of EXP002 but are directly relevant to the broader thesis.

---

# Relevance to Thesis

EXP002 establishes the quantitative handwritten-text-recognition baseline:

```text
Handwritten Line
       ↓
Pretrained TrOCR
       ↓
Text Prediction
       ↓
CER / WER / Exact Match
```

The final baseline is:

```text
IAM usable test lines: 1,480

CER:         3.33%
WER:         8.63%
Exact Match: 56.89%
```

Future approaches can now be compared against this baseline using the same evaluation protocol.

Potential comparisons include:

- controlled preprocessing,
- IAM-specific fine-tuning,
- alternative HTR architectures,
- field-aware recognition,
- spatial/contextual information,
- template-aware recognition.

The broader thesis eventually extends the pipeline toward:

```text
Structured Form
       ↓
Template / Document Alignment
       ↓
Field Detection
       ↓
Handwriting Recognition
       ↓
Field / Layout Context
       ↓
Structured Output
```

EXP002 therefore establishes the recognition component before introducing additional structured-form information.

---

# Conclusion

EXP002 successfully established a reproducible baseline for evaluating pretrained TrOCR on IAM handwritten text lines.

The experiment progressed from small exploratory evaluations:

```text
N=20
N=50
N=100
```

to an established writer-independent IAM test evaluation containing:

```text
1,480 usable line images
```

after excluding annotations marked `err`.

The final pretrained TrOCR baseline achieved:

```text
Average CER:       3.33%
Average WER:       8.63%
Exact Match Rate: 56.89%
```

These results demonstrate that pretrained TrOCR can recognize a substantial portion of IAM handwritten text accurately without IAM-specific fine-tuning.

At the same time, the difference between the exploratory subset results and the complete test-set results demonstrates the importance of evaluating models on a defined and sufficiently diverse test set.

The Exact Match result also highlights an important consideration for the thesis: low average character error does not necessarily imply that complete fields or text lines are correct. This distinction is especially important for structured forms, where a single incorrect character in an identifier, date, name, or numerical value may be significant.

EXP002 therefore provides both:

1. a quantitative reference baseline for future handwriting-recognition experiments, and
2. an initial set of recognition failures for systematic error analysis.

The experiment establishes the foundation needed to determine whether future techniques provide measurable improvements rather than relying on qualitative examples alone.

---

# Next Research Steps

EXP002 baseline evaluation is complete.

The immediate next stage is **systematic error analysis**.

## Step 1 — Error Analysis

Analyze the complete test predictions and categorize errors according to:

- character substitutions,
- insertions,
- deletions,
- word substitutions,
- spacing,
- punctuation,
- capitalization,
- handwriting difficulty,
- image quality,
- and possible language-model effects.

Particular attention should be given to the highest-CER samples.

---

## Step 2 — Controlled Preprocessing Experiments

After identifying common failure modes, evaluate preprocessing techniques such as:

- grayscale conversion,
- thresholding,
- denoising,
- contrast enhancement,
- resizing,
- and deskewing.

Each preprocessing experiment should use the same IAM test protocol and be compared directly against the EXP002 baseline:

```text
Baseline CER = 3.33%
Baseline WER = 8.63%
```

This will determine whether preprocessing produces measurable improvement.

---

## Step 3 — IAM-Specific Fine-Tuning

A later experiment can fine-tune TrOCR using:

```text
Train:      5,419 usable lines
Validation: 1,539 usable lines
```

and evaluate the resulting model on the same:

```text
Test:       1,480 usable lines
```

This enables a controlled comparison:

```text
EXP002
Pretrained TrOCR
        ↓
IAM Test Set
        ↓
CER / WER / Exact Match


          VS.


Future Experiment
IAM Fine-Tuned TrOCR
        ↓
Same IAM Test Set
        ↓
CER / WER / Exact Match
```

---

## Step 4 — Structured Handwritten Forms

After establishing handwriting-recognition baselines, the research can move toward:

- document/template alignment,
- field detection,
- field extraction,
- layout-aware recognition,
- field-specific context,
- and structured output generation.

These experiments will connect the handwriting-recognition findings from IAM with the structured-document concepts studied through FUNSD and related literature.

---

# Final Status

```text
IAM dataset preparation                  ✓
IAM manifest parser                      ✓
IAM status=ok filtering                  ✓
Writer-independent split generation      ✓
Split overlap validation                 ✓
CER / WER / Exact Match metrics          ✓

EXP002 N=20 pilot                        ✓
EXP002 N=50 evaluation                   ✓
EXP002 N=100 evaluation                  ✓
EXP002 IAM test evaluation               ✓

Final baseline:
    Samples                              1,480
    CER                                  3.33%
    WER                                  8.63%
    Exact Match                          56.89%

EXP002                                   COMPLETE

Systematic error analysis                NEXT
Controlled preprocessing                 PLANNED
IAM-specific fine-tuning                 PLANNED
Structured-form evaluation               FUTURE
```