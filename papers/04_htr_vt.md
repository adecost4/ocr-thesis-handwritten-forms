# Paper 04 — HTR-VT

## Citation

Li, Y., Chen, D., Tang, T., & Shen, X.

**HTR-VT: Handwritten Text Recognition with Vision Transformer**

Accepted for publication in *Pattern Recognition*, 2024.

---

# Research Problem

Handwritten Text Recognition (HTR) aims to convert images containing handwritten text into machine-readable character sequences.

Traditional HTR systems commonly use CNNs for visual feature extraction followed by recurrent networks such as BLSTMs for sequence modeling.

More recent Transformer-based approaches have demonstrated strong performance, but Transformers typically require large amounts of training data.

This creates a problem for HTR because labeled handwriting datasets are relatively small.

For example, datasets such as IAM and READ2016 contain only several thousand training text lines.

Previous Transformer-based HTR approaches often addressed this problem through:

- large-scale pretraining,
- synthetic handwriting data,
- external training data,
- or pretrained vision/language models.

HTR-VT investigates whether a Transformer-based HTR system can achieve competitive performance **without relying on large-scale pretraining or additional synthetic/external data**.

The main research problem can therefore be summarized as:

> How can Vision Transformers be made data-efficient enough for handwritten text recognition when only relatively small labeled handwriting datasets are available?

---

# Motivation

Vision Transformers have demonstrated strong performance in many computer-vision tasks.

However, standard ViT models do not contain the same strong visual inductive biases as CNNs and often depend on large amounts of training data.

This is problematic for handwritten text recognition because:

- labeled handwriting data is limited,
- handwriting varies significantly between writers,
- characters may be visually ambiguous,
- backgrounds may contain noise,
- and models can easily overfit small datasets.

The authors therefore investigate modifications that allow Transformer-based HTR to work effectively with limited labeled data.

---

# What Existed Before HTR-VT?

## Traditional HTR

A common traditional architecture is:

```text
Handwritten Image
        ↓
CNN
        ↓
Visual Feature Sequence
        ↓
BiLSTM / BLSTM
        ↓
CTC
        ↓
Text
```

The CNN extracts local visual features.

The recurrent network models sequential dependencies.

CTC aligns the visual feature sequence with the target character sequence without requiring explicit character segmentation.

---

## Transformer-Based HTR

Transformer-based approaches replace recurrent sequence modeling with self-attention.

However, many Transformer HTR approaches depend on:

- large-scale synthetic data,
- external datasets,
- pretraining,
- or pretrained vision/language components.

TrOCR is an important example.

Its general architecture is:

```text
Image
   ↓
Pretrained Vision Transformer Encoder
   ↓
Visual Representation
   ↓
Pretrained Transformer Decoder
   ↓
Autoregressive Text Generation
```

TrOCR achieves strong performance but benefits substantially from large-scale pretraining.

HTR-VT explores whether competitive Transformer-based HTR can instead be achieved using a simpler and more data-efficient architecture.

---

# Proposed Architecture

The core HTR-VT architecture is:

```text
Handwritten Text-Line Image
            ↓
     CNN Feature Extractor
        (ResNet-18)
            ↓
   Spatial Visual Features
            ↓
      Span Feature Masking
       (during training)
            ↓
    Transformer Encoder
            ↓
          MLP Head
            ↓
  Character Predictions
            ↓
           CTC
            ↓
      Recognized Text
```

The architecture contains three particularly important ideas:

1. CNN feature extraction
2. Span feature masking
3. Sharpness-Aware Minimization (SAM)

Unlike TrOCR, the main HTR-VT architecture does not require an autoregressive Transformer decoder.

---

# CNN Feature Extractor

Instead of directly dividing the image into fixed patches as standard ViT does, HTR-VT first processes the handwriting image using a CNN.

The authors use a modified:

```text
ResNet-18
```

as the feature extractor.

Conceptually:

```text
Handwriting Image
        ↓
Local strokes
Curves
Edges
Character shapes
        ↓
ResNet-18
        ↓
Visual Feature Tokens
```

These visual features are then passed to the Transformer encoder.

The motivation is that CNNs provide a useful inductive bias for extracting local visual patterns.

This is particularly useful for handwriting because individual characters are formed from local strokes and shapes.

The Transformer can then model relationships across the resulting visual features.

Therefore, HTR-VT combines:

```text
CNN
↓
Strong local feature extraction

+

Transformer
↓
Global/contextual modeling
```

---

# Transformer Encoder

The visual features produced by the CNN are treated as input tokens for the Transformer encoder.

The Transformer encoder uses multi-head self-attention to model relationships between features across the handwritten text line.

This allows the model to capture broader context than purely local convolutional operations.

Conceptually:

```text
Local CNN features
        ↓
Transformer self-attention
        ↓
Relationships across the text line
        ↓
Context-aware representation
```

The model uses sinusoidal positional embeddings to preserve positional information.

Unlike standard ViT, the model does not use the additional classification token because the goal is sequence recognition rather than image classification.

---

# Span Feature Masking

One of the main contributions of HTR-VT is **span feature masking**.

During training, contiguous groups of visual feature tokens are replaced by learnable mask tokens.

Conceptually:

```text
Original features

0 1 2 3 4 5 6 7 8 9

        ↓

Span masking

0 1 M M M 5 6 7 8 9
```

where:

```text
M = learnable masked token
```

The purpose is to prevent the model from depending entirely on local visual information.

If part of the visual sequence is hidden, the Transformer must use surrounding features and contextual information.

This acts as a regularization technique and helps reduce overfitting.

The authors use:

```text
Mask ratio = 0.4
Span length = 8
```

in their final experiments.

---

# Why Span Masking May Help HTR

Handwritten characters can be visually ambiguous.

For example:

```text
The c?t sat
```

If one character is difficult to recognize visually, contextual information from neighboring characters and words may help.

Span masking encourages the Transformer to learn relationships beyond individual local tokens.

The paper's attention visualizations indicate that span masking causes tokens to attend to broader regions of the handwritten text line compared with no masking or simple random masking.

Therefore:

```text
Span masking
      ↓
Less dependence on one local feature
      ↓
More contextual attention
      ↓
Potentially more robust recognition
```

---

# Sharpness-Aware Minimization (SAM)

HTR-VT also uses:

**Sharpness-Aware Minimization (SAM)**

as an optimization strategy.

The basic idea is that standard optimization attempts to find model parameters that minimize training loss.

SAM instead encourages solutions where the loss remains relatively low even when the model parameters are slightly perturbed.

Conceptually:

```text
Sharp Minimum

      \ /
       V
       *

vs.

Flat Minimum

    _________
   /         \
  /     *     \
```

A flatter minimum may generalize better to unseen data.

This is particularly relevant when training Transformers on relatively small handwriting datasets where overfitting is a concern.

SAM is therefore primarily a:

```text
training/generalization technique
```

rather than an image preprocessing method.

---

# Connectionist Temporal Classification (CTC)

HTR-VT uses CTC for sequence alignment and recognition.

CTC allows a model to learn the relationship between:

```text
Visual feature sequence
```

and:

```text
Target character sequence
```

without requiring explicit character-level segmentation.

Conceptually:

```text
CNN
 ↓
Transformer Encoder
 ↓
Character Probabilities
 ↓
CTC Alignment
 ↓
Text
```

This is different from TrOCR, which uses an autoregressive Transformer decoder.

---

# HTR-VT vs CRNN

## CRNN

```text
Image
 ↓
CNN
 ↓
BiLSTM
 ↓
CTC
 ↓
Text
```

## HTR-VT

```text
Image
 ↓
CNN
 ↓
Transformer Encoder
 ↓
CTC
 ↓
Text
```

The main difference is sequence modeling.

CRNN uses:

```text
BiLSTM
```

while HTR-VT uses:

```text
Transformer self-attention
```

Both use CNN visual features and CTC-based sequence alignment.

HTR-VT can therefore be viewed as replacing recurrent sequence modeling with Transformer-based contextual modeling.

---

# HTR-VT vs TrOCR

## TrOCR

```text
Image
 ↓
Transformer Image Encoder
 ↓
Visual Representation
 ↓
Autoregressive Transformer Decoder
 ↓
Text
```

## HTR-VT

```text
Image
 ↓
CNN Feature Extractor
 ↓
Transformer Encoder
 ↓
MLP
 ↓
CTC
 ↓
Text
```

Important differences include:

| Aspect | TrOCR | HTR-VT |
|---|---|---|
| Visual extraction | Transformer image encoder | CNN / ResNet-18 |
| Sequence modeling | Transformer decoder | Transformer encoder |
| Alignment | Autoregressive decoding | CTC |
| Decoder | Yes | No in final architecture |
| Large-scale pretraining | Central to approach | Not required |
| External/synthetic data | Used during TrOCR pretraining | Not required by HTR-VT |
| Main goal | Powerful pretrained OCR | Data-efficient HTR |
| Context | Autoregressive decoder context | Encoder self-attention |
| Regularization | Pretraining/fine-tuning strategy | Span masking + SAM |

---

# Data Efficiency

Data efficiency is one of the central ideas of the paper.

The authors aim to train a competitive Transformer-based HTR model without relying on:

```text
large-scale external pretraining
synthetic pretraining data
external language models
```

Instead, HTR-VT uses:

```text
CNN inductive bias
        +
Transformer contextual modeling
        +
Span masking
        +
SAM
        +
CTC
```

This makes the approach particularly relevant to HTR datasets where labeled data is limited.

---

# Datasets

HTR-VT is evaluated on three handwritten text recognition datasets.

## IAM

Modern English handwriting.

The split reported in the paper is:

```text
Training:     6,482 lines
Validation:     976 lines
Test:         2,915 lines
Charset:         79
```

IAM contains handwriting from 657 writers.

---

## READ2016

Historical German handwriting.

```text
Training:     8,349
Validation:   1,040
Test:         1,138
Charset:         89
```

---

## LAM

Historical Italian handwriting.

```text
Training:    19,830
Validation:   2,470
Test:         3,523
Charset:         89
```

LAM is the largest dataset used in the paper.

---

# Evaluation Metrics

The paper uses:

- Character Error Rate (CER)
- Word Error Rate (WER)

## CER

```text
CER =
(character substitutions + insertions + deletions)
-------------------------------------------------
number of ground-truth characters
```

Lower is better.

---

## WER

```text
WER =
(word substitutions + insertions + deletions)
---------------------------------------------
number of ground-truth words
```

Lower is better.

These are the same core metrics used in EXP002 of this thesis project.

---

# Main Results

## IAM

HTR-VT reports:

```text
CER = 4.7%
WER = 14.9%
Parameters = 53.5M
```

The paper reports TrOCR in the same comparison table at approximately:

```text
CER = 3.4%
Parameters = 385M
```

However, TrOCR relies on large-scale pretraining and additional data, while HTR-VT is designed to train without such external pretraining.

Therefore, the comparison is not simply:

```text
3.4 < 4.7
therefore TrOCR is universally better
```

The approaches have different training assumptions and resource requirements.

---

## READ2016

HTR-VT reports:

```text
CER = 3.9%
WER = 16.5%
```

The authors describe this as competitive with existing approaches.

---

## LAM

HTR-VT reports:

```text
CER = 2.8%
WER = 7.4%
```

The paper reports strong performance on LAM and presents it as one of the main successes of the proposed architecture.

---

# Ablation Study

The ablation experiments are important because they show which parts of HTR-VT contribute to performance.

---

## CNN Feature Extractor

The authors found that standard ViT performs poorly on IAM.

IAM validation results include approximately:

```text
Standard ViT:
CER = 26.6
WER = 57.1

HTR-VT without CNN extractor:
CER = 20.7
WER = 53.5

Full HTR-VT:
CER = 3.3
WER = 10.8
```

This shows that the CNN feature extractor is a critical component of the architecture.

---

## Span Masking

Removing span masking produces worse validation performance.

On IAM:

```text
Without Span Mask:
CER = 3.7
WER = 12.1

Full HTR-VT:
CER = 3.3
WER = 10.8
```

This suggests that span masking provides useful regularization and contextual learning.

---

## SAM

Without SAM:

```text
IAM Validation CER = 3.4
IAM Validation WER = 11.2
```

With the full approach:

```text
IAM Validation CER = 3.3
IAM Validation WER = 10.8
```

The improvement is smaller than the CNN extractor improvement but remains consistent with the paper's goal of improving generalization.

---

# Transformer Depth

The authors experiment with different numbers of Transformer encoder layers.

On IAM, the best configuration uses:

```text
4 Transformer encoder layers
6 attention heads
```

The authors report that simply increasing Transformer size does not necessarily improve performance.

This supports the paper's focus on data-efficient architecture rather than simply increasing model complexity.

---

# Transformer Decoder Experiment

One particularly interesting ablation investigates adding a Transformer decoder.

IAM results include:

| Decoder Layers | Test CER | Test WER |
|---:|---:|---:|
| 0 | **4.7** | **14.9** |
| 1 | 8.1 | 21.6 |
| 2 | 7.8 | 21.1 |
| 4 | 7.7 | 21.3 |

Adding a Transformer decoder did not improve performance.

The authors report that it did not improve convergence or prevent overfitting.

This supports their simpler:

```text
CNN
→ Transformer Encoder
→ CTC
```

architecture.

---

# Training Details

The final model uses approximately:

```text
Transformer layers: 4
Attention heads: 6
Embedding dimension: 768
MLP hidden dimension: 3072

Mask ratio: 0.4
Span length: 8

Input resolution:
512 × 64

Training iterations:
100,000

Optimizer:
AdamW + SAM

Batch size:
128
```

Training was performed on a single:

```text
RTX 4090 (24 GB)
```

and took approximately:

```text
16 hours
```

The paper also uses augmentation such as:

- random transformations,
- erosion,
- dilation,
- color jitter,
- elastic distortion.

---

# Advantages

## 1. Data Efficiency

The architecture is specifically designed to perform well without large-scale external pretraining.

---

## 2. Simpler Transformer Architecture

Only the Transformer encoder is required in the final architecture.

An autoregressive decoder is not necessary.

---

## 3. Combines CNN and Transformer Strengths

CNN:

```text
local visual feature extraction
```

Transformer:

```text
global/contextual relationships
```

---

## 4. Competitive Performance

HTR-VT achieves competitive results on IAM and READ2016 and strong results on LAM.

---

## 5. Reduced Model Size Compared with TrOCR

The paper reports approximately:

```text
HTR-VT: 53.5M parameters
TrOCR:  385M parameters
```

in its comparison.

---

## 6. Useful Ablation Studies

The paper separately investigates:

- CNN feature extraction,
- SAM,
- span masking,
- Transformer depth,
- attention heads,
- masking parameters,
- and Transformer decoder usage.

This makes it easier to understand which design decisions contribute to performance.

---

# Limitations

## 1. Line-Level Recognition

The primary experiments operate on already segmented handwritten text lines.

The model does not directly solve:

- form-field detection,
- document alignment,
- layout understanding,
- structured information extraction,
- or full-page structured-form recognition.

---

## 2. Requires Training

Unlike using an already pretrained TrOCR checkpoint directly, HTR-VT requires model training on the target HTR datasets.

---

## 3. Computational Requirements

Although the architecture is more data-efficient than large-scale pretrained approaches, training still requires substantial GPU computation.

The reported training uses an RTX 4090 for approximately 16 hours.

---

## 4. Fixed Input Resolution

The implementation uses a fixed image resolution of:

```text
512 × 64
```

which may affect very long or unusually shaped handwriting lines.

---

## 5. Manual/Specific Architectural Choices

The approach still depends on several training choices such as:

- masking ratio,
- span length,
- augmentation,
- SAM,
- CNN backbone,
- Transformer depth.

These require experimental tuning.

---

# Relevance to My Thesis

HTR-VT is highly relevant because my thesis investigates handwritten text recognition as a component of structured handwritten-form understanding.

My current EXP002 baseline uses:

```text
Pretrained TrOCR
        ↓
IAM handwritten lines
        ↓
CER / WER / Exact Match
```

HTR-VT provides an alternative recognition architecture:

```text
CNN
 ↓
Transformer Encoder
 ↓
CTC
 ↓
Text
```

This gives a useful comparison between two different Transformer-based recognition paradigms.

---

# Connection to EXP002 Error Analysis

My EXP002 systematic error analysis found that the dominant errors in the manually reviewed diagnostic sample were:

```text
Word substitution        72
Character substitution   62
Punctuation              24
Spacing                  21
Capitalization            1
```

Severe high-CER failures were dominated by word substitutions.

HTR-VT is interesting in this context because it does not use an autoregressive Transformer decoder in its final architecture.

Instead, it uses:

```text
Transformer Encoder
+
CTC
```

This raises a possible future research question:

> Do encoder+CTC and autoregressive encoder-decoder HTR systems exhibit different error patterns on structured handwritten fields?

This is currently a research question, not a conclusion.

---

# Connection to Difficult Handwriting

My EXP002 error analysis also found that many severe errors were associated with handwriting manually classified as difficult.

HTR-VT combines:

```text
CNN local feature extraction
+
Transformer contextual modeling
+
span masking
```

The span masking mechanism is particularly interesting because it encourages the model to use broader contextual information when local visual evidence is unavailable or ambiguous.

This may be relevant when individual handwritten characters are difficult to distinguish visually.

---

# Potential Research Ideas

## Idea 1 — TrOCR vs HTR-VT Error Analysis

Evaluate both models using the same handwritten dataset and compare:

```text
CER
WER
Exact Match
Error categories
```

Especially investigate whether:

```text
TrOCR
autoregressive decoder
```

and:

```text
HTR-VT
CTC
```

produce different types of word-level and character-level errors.

---

## Idea 2 — Structured-Field Recognition

Evaluate both architectures on structured fields such as:

```text
Name
Date
Student ID
Phone Number
Account Number
```

The main metric could include:

```text
Exact Field Accuracy
```

in addition to CER and WER.

---

## Idea 3 — Field Constraints

HTR-VT and TrOCR both perform general text recognition.

Structured forms provide additional information such as:

```text
field type
expected character set
expected length
template position
```

Future work could investigate whether field-specific constraints improve recognition accuracy.

---

## Idea 4 — Context vs Visual Evidence

Investigate samples where the handwriting is visually ambiguous.

Compare whether:

```text
autoregressive language context
```

and:

```text
Transformer encoder + CTC context
```

respond differently to ambiguous handwriting.

---

# Questions and Answers

## 1. What problem does HTR-VT try to solve?

HTR-VT addresses the difficulty of training Transformer-based handwritten text recognition systems when labeled handwriting datasets are relatively small.

Standard Vision Transformers generally require large amounts of data.

Previous Transformer HTR approaches often relied on large-scale pretraining, synthetic datasets, or external data.

HTR-VT attempts to provide a data-efficient Transformer-based HTR system that performs competitively without requiring these resources.

---

## 2. Why are Transformers difficult to train on small HTR datasets?

Vision Transformers have weaker built-in visual inductive biases than CNNs and generally benefit from large amounts of training data.

HTR datasets such as IAM contain only several thousand training lines.

With limited data, Transformers can:

- overfit,
- converge slowly,
- or learn unstable representations.

HTR-VT addresses this through CNN feature extraction, span masking, and SAM.

---

## 3. Why does HTR-VT use a CNN before the Transformer?

The CNN extracts strong local visual features such as:

- strokes,
- edges,
- curves,
- and character shapes.

These features provide a useful inductive bias for handwriting.

The Transformer can then focus on modeling broader contextual relationships between those features.

Therefore:

```text
CNN
=
local visual representation

Transformer
=
global/contextual representation
```

---

## 4. Why ResNet-18?

The authors use ResNet-18 because it provides effective visual feature extraction while remaining relatively simple.

Their CNN-backbone ablation reports better IAM performance with ResNet-18 than ResNet-50 or VGG-16.

Reported test CER values include:

```text
ResNet-18: 4.7
ResNet-50: 4.9
VGG-16:    7.2
```

Therefore, ResNet-18 was selected as the final backbone.

---

## 5. What does the Transformer encoder contribute?

The Transformer encoder models relationships between visual features across the complete handwritten text line.

Self-attention allows each visual token to consider information from other positions.

This provides broader contextual modeling than relying only on local CNN features.

---

## 6. What is span feature masking?

Span feature masking is a training regularization technique.

Contiguous groups of CNN-generated visual tokens are replaced by learnable mask tokens.

Example:

```text
Original:

0 1 2 3 4 5 6 7 8 9

Masked:

0 1 M M M 5 6 7 8 9
```

The model must learn to recognize text even when some local visual information is unavailable.

---

## 7. Why might span masking help handwriting recognition?

Handwritten characters may be visually ambiguous.

Masking contiguous features encourages the Transformer to use information from surrounding regions rather than depending entirely on one local feature.

The attention visualizations in the paper indicate that span masking encourages attention over broader regions of the handwritten line.

This may improve contextual modeling and reduce overfitting.

---

## 8. What is SAM trying to achieve?

Sharpness-Aware Minimization attempts to find model parameters located in flatter regions of the loss landscape.

The goal is to improve generalization.

This is useful for HTR because limited training data can make Transformer models prone to overfitting.

SAM is therefore a training optimization strategy rather than image preprocessing.

---

## 9. Why does HTR-VT use CTC?

CTC allows the model to align a sequence of visual predictions with a shorter target character sequence without requiring explicit character segmentation.

It therefore enables:

```text
visual feature sequence
        ↓
character probabilities
        ↓
CTC
        ↓
text
```

---

## 10. Why doesn't HTR-VT require an autoregressive decoder?

The Transformer encoder produces contextualized visual features, and CTC handles the alignment between those features and the target character sequence.

Therefore, the model can generate the final text without requiring a separate autoregressive Transformer decoder.

---

## 11. What happened when the authors added a Transformer decoder?

Performance became worse.

The reported IAM results include:

```text
0 decoder layers:
CER = 4.7
WER = 14.9

1 decoder layer:
CER = 8.1
WER = 21.6

2 decoder layers:
CER = 7.8
WER = 21.1

4 decoder layers:
CER = 7.7
WER = 21.3
```

The authors report that adding a decoder did not improve convergence or prevent overfitting.

---

## 12. How is HTR-VT different from CRNN?

CRNN:

```text
CNN
 ↓
BiLSTM
 ↓
CTC
```

HTR-VT:

```text
CNN
 ↓
Transformer Encoder
 ↓
CTC
```

Both use CNN visual features and CTC.

The major difference is sequence/context modeling:

```text
CRNN → recurrent BiLSTM

HTR-VT → Transformer self-attention
```

---

## 13. How is HTR-VT different from TrOCR?

TrOCR uses:

```text
Transformer image encoder
+
autoregressive Transformer decoder
+
large-scale pretraining
```

HTR-VT uses:

```text
CNN feature extractor
+
Transformer encoder
+
CTC
+
span masking
+
SAM
```

HTR-VT specifically focuses on data-efficient training without large-scale external pretraining.

---

## 14. What does "data-efficient" mean in this paper?

Data-efficient means achieving competitive HTR performance without requiring massive external or synthetic pretraining datasets.

HTR-VT attempts to learn effectively from relatively small handwriting datasets by using:

- CNN inductive bias,
- span masking,
- SAM,
- and a simpler encoder-only Transformer architecture.

---

## 15. What were HTR-VT's IAM CER and WER results?

The paper reports:

```text
IAM Test CER = 4.7%
IAM Test WER = 14.9%
```

for HTR-VT.

---

## 16. Why shouldn't I directly compare HTR-VT's IAM CER with my EXP002 CER?

My EXP002 uses a different IAM split/filtering protocol from the HTR-VT paper.

My EXP002 baseline evaluates:

```text
1,480 usable status=ok test lines
```

while HTR-VT reports a test split containing:

```text
2,915 lines
```

Other differences may include:

- preprocessing,
- image resizing,
- model training,
- split definitions,
- filtering,
- decoding,
- and evaluation implementation.

Therefore:

```text
My TrOCR CER = 3.33%
HTR-VT CER   = 4.7%
```

does **not** establish that my TrOCR setup outperforms HTR-VT.

A valid comparison would require both models to be evaluated under the same experimental protocol.

---

## 17. Which HTR-VT ideas might be relevant to my TrOCR error analysis?

Several ideas are relevant.

### CNN Local Features

My analysis identified many character substitutions and difficult handwriting cases.

Strong local visual features may help distinguish ambiguous character shapes.

### Transformer Context

Word substitutions were common among severe failures.

Contextual modeling may influence how models interpret ambiguous visual evidence.

### Span Masking

Span masking encourages the model to use surrounding context when local evidence is incomplete.

This could be relevant to difficult handwriting.

### CTC vs Autoregressive Decoding

TrOCR uses autoregressive decoding while HTR-VT uses CTC.

Comparing their error patterns may help determine whether the decoding strategy influences word substitutions or other errors.

---

## 18. How could HTR-VT become a useful comparison model later in my thesis?

HTR-VT could serve as an alternative Transformer-based HTR architecture.

A future controlled experiment could evaluate:

```text
TrOCR
vs.
HTR-VT
```

using the same:

- training/test protocol,
- handwriting images,
- ground truth,
- CER,
- WER,
- Exact Match,
- and error-analysis procedure.

This would allow investigation of whether:

```text
autoregressive encoder-decoder recognition
```

and:

```text
encoder + CTC recognition
```

behave differently on structured handwritten fields.

This could be particularly useful for fields where exact transcription is more important than general linguistic plausibility.

---

# Architecture Summary

```text
                    CRNN
                      │
              CNN → BiLSTM → CTC
                      │
                      │
                      ▼
                   HTR-VT
                      │
       CNN → Transformer Encoder → CTC
                      │
              ┌───────┴───────┐
              │               │
         Span Mask           SAM
       Regularization     Optimization
                      │
                      ▼
                    Text


                   TrOCR
                      │
          Transformer Encoder
                      ↓
     Autoregressive Transformer Decoder
                      ↓
                    Text
```

---

# Main Takeaway

The most important lesson from HTR-VT is:

> **Transformer-based handwritten text recognition does not necessarily require a large pretrained encoder-decoder architecture.**

HTR-VT demonstrates an alternative approach:

```text
CNN local visual features
        +
Transformer contextual modeling
        +
CTC sequence alignment
        +
Span masking
        +
SAM
```

with the goal of achieving strong HTR performance using limited labeled data.

For my thesis, this provides an important alternative to TrOCR and suggests that future experiments should consider not only model accuracy but also:

- data requirements,
- model size,
- decoding strategy,
- error behavior,
- and Exact Match performance on structured handwritten fields.