# Week 03 Notes – OCR Thesis Research

## Week Overview

This week focused on completing the theoretical study of Transformer-based OCR and strengthening my understanding of traditional OCR architectures. I completed the literature review of both the TrOCR and CRNN papers and compared their architectures to understand the evolution of handwritten text recognition systems.

Although implementation-related tasks were planned, this week was primarily dedicated to building a stronger theoretical foundation before moving into dataset evaluation and experiments.

---

## Activities Completed

### Literature Review

Completed reading and reviewing the following research papers:

#### Paper #1

**TrOCR: Transformer-Based Optical Character Recognition with Pre-trained Models**

**Authors:** Minghao Li et al.

Completed reading:

- Model Architecture
- Vision Transformer Encoder
- Transformer Decoder
- Pretraining Strategy
- Fine-tuning Process
- Experimental Results
- Discussion

---

#### Paper #2

**An End-to-End Trainable Neural Network for Image-Based Sequence Recognition and Its Application to Scene Text Recognition**

**Authors:** Baoguang Shi, Xiang Bai, Cong Yao

Studied the complete CRNN architecture and its role as one of the most influential OCR models before Transformer-based approaches.

---

## Topics Learned

### TrOCR Architecture

Developed a deeper understanding of the complete TrOCR pipeline.

```
Input Image
      ↓
Vision Transformer (ViT) Encoder
      ↓
Transformer Decoder
      ↓
Predicted Text
```

Key concepts learned:

- Vision Transformer as an image encoder
- Self-attention mechanism
- Autoregressive text generation
- Large-scale pretraining
- Fine-tuning for handwritten text recognition

---

### CRNN Architecture

Reviewed the traditional end-to-end OCR pipeline.

```
Image
   ↓
 CNN
   ↓
Visual Feature Sequence
   ↓
 BiLSTM
   ↓
  CTC
   ↓
 Text
```

Studied the responsibilities of each component:

- CNN for feature extraction
- BiLSTM for sequence modeling
- CTC for alignment and decoding without character-level segmentation

---

## CRNN vs TrOCR Comparison

Compared both architectures to understand how OCR systems have evolved.

### Comparison Areas

- Feature extraction
- Sequence modeling
- Text decoding
- Pretraining strategy
- Computational complexity
- Generalization ability
- Performance on handwritten text
- Potential use for structured handwritten forms

### Key Observations

**CRNN**

- Modular architecture (CNN + BiLSTM + CTC)
- Lightweight compared to Transformer models
- Lower computational requirements
- Strong baseline for OCR research

**TrOCR**

- End-to-end Transformer architecture
- Benefits from large-scale pretraining
- Better contextual understanding through self-attention
- Improved performance on handwritten text recognition benchmarks

---

## Research Questions Investigated

### Why might TrOCR outperform CRNN?

Studied the influence of:

- Large-scale pretraining
- Transformer-based contextual modeling
- Decoder-based language modeling
- Long-range dependency learning

---

### When might CRNN still be useful?

Considered situations where:

- Computational resources are limited
- Smaller models are preferred
- Faster inference is required
- A traditional OCR baseline is needed for comparison

---

## Research Insights

This week's literature review suggests that the major advancement in TrOCR comes not only from replacing recurrent networks with Transformers, but also from leveraging large-scale pretraining and end-to-end sequence generation.

Understanding CRNN provides an important historical baseline that will be valuable when comparing experimental results later in the thesis.

---

## Challenges Encountered

- Literature review required more time than initially expected.
- Understanding Transformer architecture in detail was more challenging than the earlier CNN/RNN concepts.
- Planned implementation tasks had to be postponed to ensure a solid theoretical understanding before experimentation.

---

## Tasks Carried Forward

The following planned activities were not completed this week:

- IAM dataset exploration
- CER implementation
- WER implementation
- IAM evaluation notebook
- TrOCR baseline evaluation
- Initial error analysis

These tasks will become the primary focus of the next phase of the project.

---

## Next Week Goals

### Dataset

- Study the IAM dataset structure
- Understand dataset splits
- Prepare a small subset for experimentation

### Evaluation

- Learn CER (Character Error Rate)
- Learn WER (Word Error Rate)
- Understand field-level and exact-match accuracy

### Experiments

- Create an IAM evaluation notebook
- Run pretrained TrOCR on an initial IAM subset
- Record baseline CER and WER
- Document correct and incorrect predictions
- Begin categorizing recognition errors

### Documentation

- Continue updating the literature review
- Maintain GitHub implementation log
- Record observations and potential research hypotheses

---

## Weekly Reflection

This week was dedicated to strengthening the theoretical foundation of the thesis by completing the study of both TrOCR and CRNN. Comparing traditional CNN/RNN-based OCR with modern Transformer-based approaches provided a clearer understanding of the evolution of handwritten text recognition systems. Although implementation was delayed, the knowledge gained during this period will support future experiments, baseline comparisons, and the identification of a meaningful research contribution for template-aware handwritten text recognition.