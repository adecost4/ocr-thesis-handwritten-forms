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

## Sample Size Comparison

| Run | Samples | Average CER | Average WER | Exact Matches | Exact Match Rate |
|---|---:|---:|---:|---:|---:|
| Pilot | 20 | 2.39% | 5.99% | 15 / 20 | 75% |
| Expanded | 50 | 1.08% | 2.81% | 43 / 50 | 86% |
| Expanded | 100 | 1.15% | 3.68% | 81 / 100 | 81% |

---

## Initial Interpretation

Performance improved substantially when moving from the 20-sample pilot to the 50-sample evaluation.

The N=20 run produced:

```text
CER:         2.39%
WER:         5.99%
Exact Match: 75%
```

while N=50 produced:

```text
CER:         1.08%
WER:         2.81%
Exact Match: 86%
```

The N=100 evaluation produced:

```text
CER:         1.15%
WER:         3.68%
Exact Match: 81%
```

The N=50 and N=100 CER values are relatively close:

```text
N=50  → 1.08%
N=100 → 1.15%
```

This suggests that the very small N=20 pilot was more sensitive to individual difficult samples.

WER increased from 2.81% at N=50 to 3.68% at N=100, while Exact Match decreased from 86% to 81%.

This indicates that the additional 50 samples introduced more recognition errors, although overall character-level performance remained similar.

These results suggest that pretrained TrOCR performs strongly on this selected subset of IAM.

However, because the samples are the first N entries of the generated manifest rather than an established IAM test split, these values should not be interpreted as benchmark-level IAM performance.

---

# Good Predictions

Many samples were recognized perfectly.

Examples from the pilot evaluation include:

| Sample | Ground Truth | Prediction | CER | WER |
|---|---|---|---:|---:|
| a01-003-02 | turn down the Foot-Griffiths resolution . Mr. | turn down the Foot-Griffiths resolution . Mr. | 0.0000 | 0.0000 |
| a01-003-07 | that the House of Lords should be abolished | that the House of Lords should be abolished | 0.0000 | 0.0000 |
| a01-007-05 | members . THE two rival African Nationalist | members . THE two rival African Nationalist | 0.0000 | 0.0000 |
| a01-007-08 | Roy Welensky , the Federal Premier . | Roy Welensky , the Federal Premier . | 0.0000 | 0.0000 |

The model successfully preserved:

- complete words
- capitalization
- punctuation
- spacing

for many of the evaluated lines.

This indicates that the pretrained model already transfers well to at least this selected subset of IAM handwriting.

---

# Poor Predictions

One of the most significant errors observed was:

| Sample | Ground Truth | Prediction | CER | WER |
|---|---|---|---:|---:|
| a01-003-10 | institution . | institutionalism . | 0.3846 | 0.5000 |

The model transformed:

```text
institution
```

into:

```text
institutionalism
```

The prediction is interesting because it is not random. It is a valid and linguistically related English word.

This may indicate that the decoder's language modeling can influence the final prediction when handwriting is visually ambiguous.

However, additional experiments are required before concluding that language modeling is the direct cause.

---

## Additional Errors Observed

Increasing the evaluation size revealed additional error patterns that were not as visible in the smaller pilot.

### Punctuation Error

```text
Ground Truth:
talks .

Prediction:
talks ,
```

The textual content is correct, but the punctuation differs.

---

### Word-Level Substitution

```text
Ground Truth:
of Virginia - met today in closed session

Prediction:
of Virginia - need today in closed sessions
```

This example contains word-level substitutions and an additional character in `sessions`.

---

### Language-Level Substitution

```text
Ground Truth:
Robertson later disclosed he had sent a letter

Prediction:
Robertson later disclosed the fact sent a letter
```

Several words differ while the resulting prediction remains linguistically plausible.

---

### Character-Level Error

```text
Ground Truth:
defended the appointment of a Negro as

Prediction:
defenched the appointment of a Negro as
```

The majority of the line is correct, but one word contains a character-level recognition error.

---

### Missing Punctuation

```text
Ground Truth:
Northern Rhodesia is a member of the Federation .

Prediction:
Northern Rhodesia is a member of the Federation
```

The recognized text is otherwise correct, but the final punctuation is missing.

---

# Error Categories

The observed errors can be grouped into several categories.

## 1. Capitalization Errors

Example:

```text
Though → though
```

The semantic content is correct, but case-sensitive evaluation still records an error.

---

## 2. Spacing / Tokenization Errors

Example:

```text
M Ps → MPs
```

The prediction is linguistically reasonable, but it differs from the IAM ground-truth transcription format.

---

## 3. Character Substitution Errors

Example:

```text
defended → defenched
```

A small number of visually ambiguous characters can cause an otherwise correct word to be recognized incorrectly.

---

## 4. Character / Word Generation Errors

Example:

```text
institution → institutionalism
```

The decoder generated a plausible but incorrect continuation of the handwritten word.

---

## 5. Word-Level Substitution Errors

Example:

```text
met → need
```

The predicted word differs from the ground truth while remaining linguistically plausible within the sentence.

---

## 6. Punctuation Errors

Examples:

```text
. → ,
```

or:

```text
Federation . → Federation
```

The text itself may be correct while punctuation differs from the ground truth.

---

# Observations

## 1. Pretrained TrOCR Performs Strongly on the Selected IAM Samples

Across the largest exploratory run (N=100), TrOCR achieved:

```text
Average CER:       1.15%
Average WER:       3.68%
Exact Match Rate: 81%
```

This indicates that the pretrained handwriting model can recognize many IAM line images accurately without additional IAM-specific fine-tuning.

---

## 2. The N=20 Pilot Was Not Sufficiently Stable

The N=20 evaluation produced:

```text
CER = 2.39%
```

compared with:

```text
N=50  → CER = 1.08%
N=100 → CER = 1.15%
```

A small number of difficult predictions have a larger influence on the mean when the evaluation contains only 20 samples.

The notable example:

```text
institution → institutionalism
```

had a CER of approximately:

```text
0.385
```

A single error of this magnitude can substantially influence a 20-sample average.

This demonstrates why conclusions should not be drawn from very small evaluation subsets.

---

## 3. N=50 and N=100 Show More Stable Character-Level Performance

CER changed only slightly:

```text
N=50  → 1.08%
N=100 → 1.15%
```

This suggests that character-level performance became more stable as the evaluation size increased.

However, this should not be interpreted as statistical convergence because the samples were not randomly selected and do not represent an established IAM test split.

---

## 4. Exact Match Is Much Stricter Than CER

At N=100:

```text
Exact Match Rate = 81%
```

This means 19 of the 100 evaluated lines contained at least one difference from the ground truth.

Some differences were very small, including:

- capitalization
- punctuation
- spacing
- a single incorrect character

Therefore, a prediction can achieve a very low CER while still failing Exact Match.

This distinction may become particularly important for structured forms.

For fields such as:

```text
Student ID
Date
Account Number
Phone Number
Name
```

even one incorrect character may make the extracted field unusable.

---

## 5. Language-Like Substitutions Are an Interesting Error Category

Some errors produced linguistically plausible text rather than random character sequences.

Examples include:

```text
institution
→ institutionalism
```

and:

```text
Robertson later disclosed he had sent a letter
→ Robertson later disclosed the fact sent a letter
```

These observations are consistent with the behavior expected from an autoregressive Transformer decoder that uses previously generated tokens as context.

However, additional controlled experiments are required before concluding that decoder language modeling directly caused these errors.

---

## 6. Punctuation Contributes to Measured Errors

Several predictions were textually correct except for punctuation.

Examples include:

```text
talks .
→ talks ,
```

and:

```text
Federation .
→ Federation
```

Because CER, WER, and Exact Match operate on the provided transcription strings, these differences affect the reported metrics.

Future analysis may therefore consider both:

1. strict evaluation using the original IAM transcription
2. normalized evaluation where punctuation and case normalization are explicitly defined

Strict evaluation should remain the primary baseline for reproducibility.

---

# Limitations

## Exploratory Sample Selection

Although the experiment was expanded to 100 samples, the evaluation still uses:

```python
df.head(N)
```

Therefore, the experiment evaluates the first N usable entries in the generated IAM manifest.

These samples are not randomly selected and do not correspond to an established IAM benchmark split.

---

## Limited Writer Diversity

Consecutive IAM entries may originate from nearby forms and writers.

Therefore, the first 100 entries may not adequately represent the diversity of handwriting styles present across the complete IAM dataset.

---

## No Official Test Split

The N=20, N=50, and N=100 results should be treated as exploratory pipeline-validation experiments.

They should not be directly compared against published IAM benchmark results.

A reproducible baseline requires evaluation using an established IAM test split.

---

## No Fine-Tuning

The pretrained TrOCR checkpoint was evaluated directly without additional IAM-specific fine-tuning.

---

## No Additional Preprocessing

No additional image enhancement, denoising, thresholding, or deskewing was performed.

The experiment therefore represents the performance of the pretrained TrOCR pipeline without preprocessing optimization.

---

## Recognition Only

The experiment evaluates cropped handwritten text-line recognition.

It does not evaluate:

- text detection
- structured field detection
- form layout understanding
- semantic entity classification
- field extraction
- template information
- entity relationships

These components will become important for the final structured handwritten-form thesis problem.

---

# Relevance to Thesis

EXP002 establishes the initial handwriting-recognition baseline:

```text
Handwritten Line
       ↓
Pretrained TrOCR
       ↓
Text Prediction
       ↓
CER / WER / Exact Match
```

The experiment demonstrates that pretrained TrOCR can already recognize many IAM handwritten lines accurately without IAM-specific fine-tuning.

However, the final thesis problem extends beyond handwriting recognition.

The eventual system may require:

```text
Structured Form
       ↓
Field / Text Detection
       ↓
Handwriting Recognition
       ↓
Layout Understanding
       ↓
Field Classification
       ↓
Relationship Understanding
       ↓
Structured Output
```

Future experiments can compare the EXP002 baseline against:

- IAM-fine-tuned TrOCR
- preprocessing strategies
- structured-form datasets
- field-specific context
- spatial information
- template-aware recognition

---

# Next Step — Official IAM Evaluation

The exploratory sample-size progression is complete:

```text
N=20   ✓
N=50   ✓
N=100  ✓
```

Increasing arbitrary N further is not necessary.

The next step is to create a reproducible evaluation using an established IAM train/validation/test split.

The target structure will be:

```text
IAM
│
├── train.csv
├── validation.csv
└── test.csv
```

The pretrained TrOCR model will then be evaluated on **all valid samples in the established test split**.

This will provide the final pretrained baseline for EXP002.

---

## Planned Comparison

After establishing the official baseline, the next major experiment can evaluate IAM-specific fine-tuning.

```text
EXP002
Pretrained TrOCR
        ↓
Established IAM Test Set
        ↓
Baseline CER / WER / Exact Match


            VS.


EXP003
IAM Fine-Tuned TrOCR
        ↓
Same IAM Test Set
        ↓
Fine-Tuned CER / WER / Exact Match
```

Using the same test set and metrics will allow a controlled comparison between pretrained and IAM-fine-tuned TrOCR.

---

# Current Status

```text
IAM dataset preparation          ✓
CER / WER / Exact Match metrics  ✓
Pretrained TrOCR inference       ✓
N=20 pilot evaluation            ✓
N=50 evaluation                  ✓
N=100 evaluation                 ✓
Error analysis                   ✓
Established IAM split            NEXT
IAM test-set baseline            PENDING
IAM fine-tuning                  PENDING
Structured-form evaluation       FUTURE
```