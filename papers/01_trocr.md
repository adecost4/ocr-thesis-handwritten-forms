# Paper 01 — TrOCR

## Citation

Li, M., Lv, T., Chen, J., Cui, L., Lu, Y., Florencio, D., Zhang, C., Li, Z., & Wei, F. (2023). **TrOCR: Transformer-Based Optical Character Recognition with Pre-trained Models.** *Proceedings of the AAAI Conference on Artificial Intelligence*, 37(11), 13094–13102.

Paper: https://arxiv.org/abs/2109.10282

---

## Research Problem

Traditional OCR systems rely on multiple specialized components such as CNNs for feature extraction, RNNs/LSTMs for sequence modeling, and CTC or attention-based decoders for text prediction. These pipelines are complex, require task-specific engineering, and cannot fully leverage the success of pretrained Transformer models.

The authors investigate whether OCR can be reformulated as an end-to-end Transformer encoder–decoder task using pretrained vision and language models.

---

## What existed before TrOCR?

Typical OCR pipeline:

```
Image
   ↓
CNN
   ↓
Visual Feature Sequence
   ↓
BiLSTM / RNN
   ↓
CTC or Attention Decoder
   ↓
Recognized Text
```

Characteristics:

- CNN extracts visual features.
- BiLSTM captures sequential context.
- CTC aligns image features with text without character-level annotations.
- Many systems also use external language models.

Representative methods:

- CRNN
- Rosetta
- SAR
- ABINet
- ViTSTR

---

## Proposed Architecture

```
Image
    ↓
Vision Transformer (Encoder)
    ↓
Visual Features
    ↓
Transformer Decoder
    ↓
Recognized Text
```

Instead of predicting characters using CTC, TrOCR treats OCR as a sequence generation task similar to machine translation.

Main components:

- Vision Transformer (ViT) encoder
- Transformer decoder
- Cross-attention between image and text representations
- Autoregressive decoding

---

## Pretraining

The model is initialized using pretrained Transformer models.

- Encoder initialized from a pretrained Vision Transformer.
- Decoder initialized from a pretrained language Transformer.
- Additional pretraining performed on large synthetic text-image datasets.

Benefits:

- Learns strong visual representations.
- Learns linguistic context before OCR fine-tuning.
- Reduces the amount of labeled OCR data needed.

---

## Fine-tuning

The pretrained model is fine-tuned on downstream OCR datasets.

Fine-tuning tasks include:

- Handwritten text recognition
- Printed document OCR
- Scene text recognition

The same encoder–decoder architecture is used for all tasks.

---

## Datasets

### Handwritten Text

- IAM

### Printed / Scene Text

- IIIT5K
- SVT
- IC13
- IC15
- SVTP
- CUTE80
- SROIE

---

## Evaluation Metrics

The paper evaluates performance using:

- Character Error Rate (CER)
- Word Error Rate (WER)
- Recognition Accuracy

Lower CER and WER indicate better OCR performance.

---

## Main Results

The paper reports state-of-the-art performance across multiple OCR benchmarks.

Key findings:

- Outperforms CNN-RNN based OCR systems.
- Achieves strong results on the IAM handwritten dataset.
- Performs competitively on printed and scene text recognition.
- Demonstrates that pretrained Transformer models transfer effectively to OCR tasks.

---

## Advantages

- End-to-end architecture.
- Eliminates CNN + RNN + CTC pipeline.
- Uses pretrained vision and language models.
- Learns visual and language context jointly.
- Works for handwritten, printed, and scene text.
- Requires minimal task-specific engineering.

---

## Limitations

- Large model requiring significant computational resources.
- Depends on large-scale synthetic pretraining.
- Focuses on text recognition rather than complete document understanding.
- Evaluation is mainly on English OCR benchmarks.

---

## What I Don't Understand Yet

- How does the Vision Transformer convert image patches into tokens?
- How does cross-attention connect image features with text generation?
- Why does autoregressive decoding outperform CTC?
- How are WordPiece tokens converted into complete words?
- What are the computational trade-offs compared to CRNN?

---

## Relevance to My Thesis

This paper serves as the foundation of my thesis because it replaces the traditional OCR pipeline with an end-to-end Transformer architecture.

It demonstrates that:

- Vision Transformers can replace CNN feature extractors.
- Transformer decoders can replace BiLSTMs and CTC.
- Pretrained models significantly improve handwritten OCR.
- Fine-tuning enables adaptation to custom handwriting datasets.

The paper provides the baseline model that I plan to extend and evaluate on handwritten document datasets.

---

## Potential Research Ideas

- Fine-tune TrOCR on historical handwritten manuscripts.
- Compare TrOCR with Florence-2 and Donut.
- Apply LoRA or other parameter-efficient fine-tuning methods.
- Investigate multilingual handwritten OCR.
- Improve robustness to noisy scans and low-resolution documents.
- Study the impact of preprocessing techniques on recognition accuracy.
- Build lightweight TrOCR models for deployment on edge devices.

---

## Key Takeaways

- TrOCR replaces CNN + RNN + CTC with a Transformer encoder–decoder architecture.
- OCR is reformulated as an image-to-text generation problem.
- Pretraining on vision and language tasks greatly improves OCR performance.
- The model achieves state-of-the-art results on handwritten, printed, and scene text recognition.
- TrOCR establishes a new direction for Transformer-based OCR research and serves as an excellent baseline for handwriting recognition projects.

---

## Study Questions & Answers

### Why use an encoder-decoder architecture?

OCR is treated as an image-to-text generation problem.

The encoder first converts the input image into a sequence of visual representations. The decoder then generates the text one token at a time while attending to both the encoded image features and the previously generated tokens.

This architecture allows TrOCR to jointly model visual understanding and language generation in a single end-to-end framework.

---

### What does the image encoder learn?

The image encoder (Vision Transformer) learns visual representations of the input image.

Instead of extracting convolutional feature maps like CNNs, it:

- splits the image into 16×16 patches,
- converts each patch into an embedding,
- applies self-attention to learn relationships among all image patches,
- produces contextual visual features representing the entire text image.

These visual features are passed to the decoder.

---

### What does the decoder do?

The Transformer decoder generates the output text autoregressively.

At each decoding step it:

1. looks at the visual features from the encoder,
2. looks at previously generated tokens,
3. predicts the next WordPiece token.

Generation continues until the End-of-Sequence (EOS) token is produced.

Unlike previous OCR systems, TrOCR does not require a CTC decoder or an external language model.

---

### What is pretraining vs. fine-tuning?

**Pretraining**

The model is first trained on very large synthetic text-image datasets.

The goal is to learn:

- general visual representations
- language representations
- relationships between images and text

before seeing the target OCR dataset.

**Fine-tuning**

The pretrained model is then trained on a smaller labeled OCR dataset (such as IAM).

Fine-tuning adapts the general knowledge learned during pretraining to the specific OCR task.

---

### Why might TrOCR work better than CNN/RNN systems?

Compared to CNN-RNN pipelines, TrOCR has several advantages:

- uses pretrained vision and language models,
- captures long-range dependencies through self-attention,
- jointly models image understanding and language generation,
- eliminates separate CNN, RNN, CTC, and external language model components,
- performs end-to-end sequence generation.

The paper shows these advantages lead to state-of-the-art performance on handwritten, printed, and scene text benchmarks.

---

### What assumptions does TrOCR make about its input?

TrOCR assumes:

- the input is already a cropped text-line or word image,
- the image is resized to 384×384 pixels,
- the resized image is divided into 16×16 patches,
- text detection has already been completed.

The paper focuses only on **text recognition**, not text detection or document layout analysis.