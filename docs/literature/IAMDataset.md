# IAM Dataset

## Purpose

The IAM Handwriting Database is one of the most widely used benchmark datasets for **offline handwritten text recognition (HTR)**. It was created to support research in handwriting recognition, writer identification, and document analysis by providing scanned handwritten English text with corresponding ground-truth transcriptions. :contentReference[oaicite:0]{index=0}

---

## Offline or Online?

**Offline handwriting dataset**

IAM contains scanned images of handwritten documents.

Unlike the IAM-OnDB dataset, it **does not contain pen trajectory information** (such as x-y coordinates, pen pressure, or writing speed). Instead, models recognize handwriting directly from images. :contentReference[oaicite:1]{index=1}

---

## Number of Writers

- **657 writers**
- **1,539 scanned forms (pages)**
- **13,353 labeled text lines**
- **115,320 labeled words**
- **5,685 labeled sentences**

The handwriting comes from many different individuals, making the dataset suitable for writer-independent handwriting recognition. :contentReference[oaicite:2]{index=2}

---

## Forms

A **form** is a complete scanned page of handwriting.

Each form contains multiple paragraphs and text lines written by a single writer.

Example:

```
Form
│
├── Paragraph
│
├── Paragraph
│
└── Paragraph
```

Each form is stored as a PNG image with corresponding XML metadata. :contentReference[oaicite:3]{index=3}

---

## Lines

Each form is segmented into individual handwritten text lines.

Example:

```
Form

↓

Line 1

↓

Line 2

↓

Line 3
```

Each line has:

- cropped image
- transcription
- metadata

Most handwritten text recognition research trains directly on these line images. :contentReference[oaicite:4]{index=4}

---

## Words

Each line is further segmented into individual words.

Example:

```
Line

↓

Word 1

↓

Word 2

↓

Word 3
```

Each word image has its own ground-truth transcription and metadata.

The word segmentation was generated automatically and manually verified. :contentReference[oaicite:5]{index=5}

---

## Ground Truth Format

The dataset provides:

- image files (PNG)
- XML annotation files
- ASCII transcription files

The XML files contain:

- writer ID
- form ID
- line IDs
- word IDs
- transcription
- segmentation information
- bounding boxes
- additional metadata from preprocessing

This allows researchers to map every image to its correct transcription. :contentReference[oaicite:6]{index=6}

---

## Image Format

- PNG images
- 300 dpi scanned resolution
- 256 grayscale levels

The dataset includes images at multiple levels:

- forms
- sentences
- text lines
- words

:contentReference[oaicite:7]{index=7}

---

## Dataset Splits

The IAM database provides official writer-independent evaluation protocols.

A commonly used split is:

| Split | Text Lines | Writers |
|--------|-----------:|--------:|
| Train | 6,161 | 283 |
| Validation 1 | 900 | 46 |
| Validation 2 | 940 | 43 |
| Test | 1,861 | 128 |

Many modern HTR papers instead use the **Aachen (RWTH) split**, which also separates writers between training, validation, and testing to enable fair comparison across models. :contentReference[oaicite:8]{index=8}

---

## Why IAM is useful for my thesis

IAM is highly relevant because it provides:

- Offline handwritten English documents.
- High-quality ground-truth annotations.
- Standard benchmark splits used by the HTR community.
- Writer-independent evaluation.
- Line- and word-level images suitable for training Transformer-based OCR models such as TrOCR.

It is an excellent benchmark for evaluating the handwriting recognition component of my thesis before applying the model to real-world forms.

---

## Why IAM is NOT identical to my thesis problem

Although IAM is an excellent handwriting recognition benchmark, it does **not** fully represent my research problem.

IAM contains:

- handwritten text
- scanned pages
- line images
- word images

My thesis focuses on **structured handwritten forms**, which introduce additional challenges:

- predefined fields (e.g., Name, Address, Date)
- fixed document templates
- multiple field types
- handwritten entries mixed with printed text
- empty fields
- checkboxes and form elements
- document layout understanding
- field extraction before handwriting recognition

Therefore, IAM solves only the **handwriting recognition** part of my problem.

A complete system for my thesis will likely require:

```
Structured Form

↓

Form Detection

↓

Field Detection

↓

Field Cropping

↓

Handwritten Text Recognition (e.g., TrOCR)

↓

Structured Output
```

IAM provides an excellent benchmark for evaluating the HTR stage, but additional datasets or custom data will be needed to study form understanding and field extraction.