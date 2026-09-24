# Paper 02 — CRNN

## Citation

Shi, B., Bai, X., & Yao, C. (2015). **An End-to-End Trainable Neural Network for Image-based Sequence Recognition and Its Application to Scene Text Recognition.** arXiv:1507.05717.

Paper: https://arxiv.org/abs/1507.05717

---

## Research Problem

Traditional OCR systems often required:

- Character segmentation before recognition.
- Handcrafted visual features.
- Multiple independently trained modules.
- Character-level annotations.

These approaches struggled with variable-length text and were difficult to optimize end-to-end.

The authors propose an end-to-end neural network that directly recognizes image sequences without explicit character segmentation.

---

## What existed before CRNN?

Earlier OCR methods generally followed one of these approaches:

### Character-based OCR

```
Image
   ↓
Character Detection
   ↓
Character Classification
   ↓
Word Assembly
```

Problems:

- Requires accurate character segmentation.
- Sensitive to touching or overlapping characters.
- Needs character-level annotations.

---

### CNN Classification

```
Image
   ↓
CNN
   ↓
Fixed Dictionary Classification
```

Problems:

- Predicts from a predefined vocabulary.
- Cannot recognize unseen words.
- Not suitable for variable-length sequences.

---

### RNN + Handcrafted Features

```
Image
   ↓
Handcrafted Features (e.g., HOG)
   ↓
RNN
   ↓
Text
```

Problems:

- Feature extraction is independent of sequence learning.
- Cannot be trained end-to-end.

---

## Proposed Architecture

```
Image
    ↓
CNN
    ↓
Feature Sequence
    ↓
Bidirectional LSTM
    ↓
CTC Transcription
    ↓
Recognized Text
```

Three major components:

1. CNN extracts visual features.
2. Bidirectional LSTM models sequential context.
3. CTC converts frame predictions into the final text sequence.

---

## CNN Feature Extraction

The convolutional layers learn visual representations directly from images.

Instead of recognizing individual characters, the CNN converts the input image into a sequence of feature vectors.

Each column of the feature map represents a small region of the original image.

Advantages:

- No handcrafted features.
- No character segmentation.
- Learns robust visual representations automatically.

---

## Sequence Modeling (BiLSTM)

The feature sequence is passed into Bidirectional LSTM layers.

The BiLSTM learns contextual information from:

- left-to-right
- right-to-left

This helps distinguish ambiguous characters using surrounding context.

Example:

```
minimum
```

The repeated vertical strokes become easier to interpret when neighboring characters are considered.

---

## CTC (Connectionist Temporal Classification)

CTC converts frame-level predictions into the final text.

Instead of requiring character locations, CTC learns all possible alignments between image frames and text.

Example:

```
Prediction

HH--EE-LLL-LOO

↓

HELLO
```

Benefits:

- No character segmentation.
- No character-level labels.
- Works with variable-length sequences.

---

## Training

CRNN is trained end-to-end.

Training requires only:

- input image
- corresponding text label

Character positions are not needed.

The CNN, BiLSTM, and CTC are optimized jointly using a single loss function.

---

## Datasets

Training:

- Synth90k (8 million synthetic word images)

Evaluation:

- IIIT5K
- SVT
- ICDAR 2003
- ICDAR 2013

The paper also demonstrates CRNN on Optical Music Recognition (OMR) to show that the architecture generalizes beyond text.

---

## Evaluation Metrics

The paper reports:

- Recognition Accuracy
- Lexicon-based Accuracy
- Lexicon-free Accuracy

Performance is evaluated on standard scene text recognition benchmarks.

---

## Main Results

CRNN achieved state-of-the-art or highly competitive performance on multiple OCR benchmarks.

Key findings:

- Outperformed many existing scene text recognition methods.
- Worked without explicit character segmentation.
- Required only word-level annotations.
- Generalized well to Optical Music Recognition.
- Used a much smaller model (approximately 8.3 million parameters) than many competing CNN-based approaches.

---

## Advantages

- End-to-end trainable.
- No character segmentation.
- No handcrafted features.
- Handles variable-length text.
- Requires only word-level labels.
- Supports unconstrained text recognition.
- Compact architecture with relatively few parameters.

---

## Limitations

- Uses CNNs with limited receptive fields compared to Transformers.
- Sequential processing in BiLSTMs reduces parallelism.
- Relies on CTC for alignment instead of directly modeling language generation.
- Does not leverage pretrained vision or language models.
- Performance depends heavily on the quality of learned visual features.

---

## What I Don't Understand Yet

- How exactly does CTC compute all valid alignments?
- Why is Bidirectional LSTM better than a standard LSTM?
- How does the receptive field affect recognition accuracy?
- How are feature maps converted into sequential feature vectors?
- Why are column-wise features sufficient for text recognition?

---

## Relevance to My Thesis

CRNN represents the dominant OCR architecture before Transformer-based approaches.

Understanding CRNN is important because TrOCR directly replaces each of its major components:

| CRNN | TrOCR |
|------|--------|
| CNN | Vision Transformer |
| BiLSTM | Transformer Decoder |
| CTC | Autoregressive Generation |

Studying CRNN provides the historical foundation needed to understand why Transformer-based OCR became successful.

---

## Potential Research Ideas

- Compare CRNN and TrOCR on handwritten OCR.
- Evaluate CNN features versus Vision Transformer features.
- Investigate lightweight CRNN models for mobile OCR.
- Compare CTC decoding with autoregressive decoding.
- Study the impact of synthetic training data on recognition accuracy.

---

## Key Takeaways

- CRNN introduced one of the first successful end-to-end OCR architectures.
- It combines CNN feature extraction, BiLSTM sequence modeling, and CTC transcription.
- It eliminates character segmentation and handcrafted features.
- It handles variable-length text using sequence learning.
- CRNN became the foundation for many modern OCR systems and provides the baseline that later Transformer-based models, such as TrOCR, sought to improve.