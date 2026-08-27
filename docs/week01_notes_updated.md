# Week 01 Notes - OCR Thesis Research

## Thesis Topic

Working Title:

**Template-Aware Handwritten OCR for Structured Bank and Government Forms**

Research Goal:

Develop a system capable of extracting and recognizing handwritten information from structured forms using modern OCR techniques, image processing, and deep learning.

---

## Activities Completed

### Environment Setup

* Created GitHub repository
* Setup Google Colab environment
* Installed:

  * PyTorch
  * Transformers
  * Hugging Face libraries
  * OpenCV (planned)
* Connected Google Drive

### TrOCR Experiments

Successfully loaded:

* microsoft/trocr-base-handwritten

Performed OCR inference on:

1. Sample generated images
2. Personal handwritten note

Results:

* Sample image recognized successfully
* Personal handwritten image produced incorrect output

Observation:

Real-world handwritten images are significantly more challenging than clean benchmark examples.

Possible reasons:

* Background noise
* Notebook lines
* Perspective distortion
* Different handwriting style
* Multiple text lines

---

## Key Concepts Learned

### OCR Pipeline

General OCR workflow:

Image
→ Preprocessing
→ Feature Extraction
→ Recognition Model
→ Text Output

### TrOCR

TrOCR is a Transformer-based OCR system.

Architecture:

Image
→ Vision Transformer Encoder
→ Transformer Decoder
→ Text

Advantages:

* End-to-end OCR
* No explicit character segmentation
* State-of-the-art handwritten text recognition

---

## Research Questions

1. Why does TrOCR fail on some real handwritten images?
2. How important is image preprocessing?
3. Can field-specific OCR improve recognition?
4. How can OCR performance be improved on structured forms?
5. What role does template information play in recognition accuracy?

---

## Papers Read

### TrOCR

Status:
Started

Focus Areas:

* Abstract
* Introduction
* Model architecture

Notes:

* Uses Vision Transformer encoder
* Uses Transformer decoder
* Achieves strong results on handwritten datasets

### IAM Dataset

Status:
Started

Notes:

* Standard benchmark dataset
* Contains handwritten forms
* Includes line-level and word-level annotations

---

## Ideas for Thesis Direction

Potential Direction 1:

Template-aware OCR for structured forms

Potential Direction 2:

Field-aware OCR

Examples:

* Name field
* Date field
* Address field

Potential Direction 3:

Image preprocessing pipeline for handwritten form recognition

---

## Challenges Encountered

* Difficulty understanding OCR architecture initially
* Confusion around dataset organization
* TrOCR poor performance on personal handwriting

---

## Next Week Goals

### Learning

* OpenCV basics
* Image preprocessing
* OCR evaluation metrics

### Experiments

* Convert images to grayscale
* Thresholding
* Cropping handwritten regions
* Compare OCR before and after preprocessing

### Reading

* Finish TrOCR paper
* Read 2 additional OCR papers
* Understand IAM dataset structure

### Documentation

* Create literature review spreadsheet
* Add experiment tracking files

---

## Weekly Reflection

This week focused on understanding the OCR research landscape and setting up the development environment.

The most important insight was that state-of-the-art OCR models perform well on clean benchmark images but may struggle on real handwritten notes. This observation highlights the importance of preprocessing and domain-specific adaptation, which may become an important part of the thesis.


---

## Daily Progress Update

### **Date: August 26, 2026**

#### Literature Review & Learning

**Online vs Offline Handwritten Text Recognition (HTR)**

- Studied the differences between **Online HTR** and **Offline HTR**.
- Learned that:
  - **Online HTR** uses dynamic handwriting information such as pen trajectory, stroke order, and timing.
  - **Offline HTR** recognizes handwriting from scanned images without temporal information.
- Identified that this thesis focuses on **Offline HTR**, since handwritten entries will be extracted from scanned structured forms.

#### Deep Learning Models for HTR

Watched a high-level overview comparing the evolution of handwriting recognition models.

- **CNN (Convolutional Neural Networks)**
  - Learns visual features from handwritten images.

- **RNN (Recurrent Neural Networks)**
  - Processes sequential information but struggles with long-term dependencies.

- **LSTM (Long Short-Term Memory)**
  - Improved RNN architecture for learning longer text sequences.
  - Commonly used in CRNN-based HTR systems.

- **Transformer**
  - Uses self-attention instead of recurrence.
  - Foundation of modern HTR systems such as TrOCR.

#### Key Takeaways

- Offline HTR is the primary research area for this thesis.
- There has been a progression in HTR architectures:
  **CNN → RNN → LSTM/CRNN → Transformer (TrOCR)**.
- This study provides the theoretical foundation needed before implementing and comparing baseline HTR models.

#### Next Learning Goals

- Read the TrOCR paper in detail.
- Understand Connectionist Temporal Classification (CTC).
- Begin studying the IAM handwriting dataset.
