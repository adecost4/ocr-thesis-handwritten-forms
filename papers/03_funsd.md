# Paper 03 — FUNSD

## Citation

Jaume, G., Ekenel, H. K., & Thiran, J.-P. (2019). **FUNSD: A Dataset for Form Understanding in Noisy Scanned Documents.**

Paper: https://arxiv.org/abs/1905.13538

---

## Research Problem

Traditional OCR focuses mainly on converting text in an image into machine-readable text.

For forms, recognizing the text alone is not sufficient.

A system also needs to understand:

- where text appears,
- which words belong together,
- what role each text entity has,
- and how different entities are related.

The paper defines **Form Understanding (FoUn)** as automatically extracting and structuring written information contained in a form.

FUNSD was introduced as a benchmark dataset for studying these problems on real, noisy scanned forms.

---

## What is Form Understanding?

Form Understanding is the task of extracting and structuring written information from forms.

The process goes beyond OCR.

A form-understanding system needs to:

1. detect and recognize text,
2. analyze the spatial layout,
3. group words into semantic entities,
4. classify those entities,
5. determine relationships between entities.

Example:

```text
Name:        John Smith
Date:        09/30/2026
```

OCR may produce:

```text
Name
John Smith
Date
09/30/2026
```

Form understanding should recover:

```text
Name ─────→ John Smith
Date ─────→ 09/30/2026
```

The objective is therefore not merely transcription, but reconstruction of the semantic structure of the document.

---

## Why OCR Alone Is Not Enough

OCR answers:

> What text is present?

Form understanding additionally asks:

> Where is the text?

> Which words belong together?

> What does the text represent?

> Which entities are related?

For example:

```text
Employee Name       John Smith
Employee ID         123456
```

Perfect OCR could recognize every word correctly while still failing to determine that:

```text
Employee Name → John Smith
Employee ID   → 123456
```

Therefore, OCR is an important component of form understanding but does not solve the complete problem.

---

## Dataset

FUNSD contains:

- 199 fully annotated scanned forms
- real documents
- low-resolution scans
- multiple document structures
- realistic scanning and printing noise

The forms were sampled from the form category of the RVL-CDIP dataset.

The original RVL-CDIP documents come from the Truth Tobacco Industry Document archive and include material such as scientific, marketing, and advertising documents.

---

## Dataset Split

| Split | Forms | Words | Entities | Relations |
|---|---:|---:|---:|---:|
| Training | 149 | 22,512 | 7,411 | 4,236 |
| Testing | 50 | 8,973 | 2,332 | 1,076 |
| **Total** | **199** | **31,485** | **9,743** | **5,312** |

---

## Annotation Format

Each form is represented using a JSON file.

A form contains a list of semantic entities.

Each semantic entity contains information such as:

```json
{
    "id": 0,
    "text": "Registration No.",
    "box": [94, 169, 191, 186],
    "linking": [[0, 1]],
    "label": "question",
    "words": [...]
}
```

Each semantic entity includes:

- unique ID
- text
- bounding box
- semantic label
- links to other entities
- individual words

Each word also contains:

- textual content
- bounding box

Bounding boxes use:

```text
[x_left, y_top, x_right, y_bottom]
```

---

## Semantic Entity Labels

FUNSD defines four semantic entity classes:

### QUESTION

A prompt or field requesting information.

Example:

```text
Registration No.
Name
Date of Birth
Address
```

---

### ANSWER

The information associated with a question.

Example:

```text
Registration No. → 533

Name → John Smith
```

---

### HEADER

Text that identifies or organizes a section of the form.

Example:

```text
EMPLOYEE INFORMATION
PERSONAL DETAILS
```

---

### OTHER

Text that does not fit into the question, answer, or header categories.

---

## Entity Class Distribution

| Split | Header | Question | Answer | Other |
|---|---:|---:|---:|---:|
| Training | 441 | 3,266 | 2,802 | 902 |
| Testing | 122 | 1,077 | 821 | 312 |

Questions and answers are the most common semantic entities in the dataset.

---

## Entity Linking

Entity linking determines relationships between semantic entities.

For example:

```text
Registration No. ─────→ 533
      QUESTION           ANSWER
```

FUNSD represents the relationship as:

```text
[question_id, answer_id]
```

For example:

```json
"linking": [[0, 1]]
```

Entity linking therefore allows the system to reconstruct question-answer relationships instead of simply returning disconnected text.

---

## Form Understanding Tasks

The paper decomposes form understanding into three main tasks:

### 1. Word Grouping

Determine which words belong to the same semantic entity.

Example:

```text
Registration + No.
```

should be grouped into:

```text
Registration No.
```

---

### 2. Semantic Entity Labeling

Assign each semantic entity one of four labels:

```text
QUESTION
ANSWER
HEADER
OTHER
```

---

### 3. Entity Linking

Determine relationships between semantic entities.

Example:

```text
Name ─────────→ John Smith
```

---

## Why Spatial Layout Matters

Forms communicate information through both text and position.

For example:

```text
Name:          John Smith
Address:       Phoenix
Student ID:    123456
```

The relative positions of these elements provide clues about their relationships.

Two text elements positioned near each other may form a question-answer pair.

Therefore, form understanding requires both:

```text
Textual information
        +
Spatial information
```

The FUNSD annotations provide bounding boxes so models can reason about document layout.

---

## Why Noisy Scanned Forms Are Difficult

FUNSD intentionally contains real scanned documents with substantial variation and noise.

The documents are approximately 100 dpi and may contain degradation caused by repeated scanning and printing.

Challenges include:

- low resolution,
- scanning artifacts,
- printing artifacts,
- different form layouts,
- varying document structures,
- text detection errors,
- OCR errors.

This makes FUNSD more representative of real-world document processing than clean digitally generated forms.

---

## Baseline Tasks and Metrics

The paper evaluates several components of the form-understanding pipeline.

### Text Detection

Methods evaluated include:

- Tesseract
- EAST
- Google Vision
- Faster R-CNN

Metrics:

- Precision
- Recall
- F1 score

The retrained Faster R-CNN baseline achieved the highest reported text-detection F1 score of **0.76**.

---

### OCR

The paper evaluates:

- Tesseract
- Google Vision

using Levenshtein similarity.

Google Vision achieved:

```text
Text Detection + OCR: 76.4%
OCR:                  94.4%
```

The large difference demonstrates an important point:

> Accurate recognition alone does not guarantee that all relevant text has been successfully detected.

---

### Word Grouping

Word grouping is treated as a clustering problem.

Metric:

```text
Adjusted Rand Index (ARI)
```

Results:

```text
Tesseract      0.20
Google Vision  0.41
```

The paper notes that these baselines perform poorly because they do not sufficiently consider spatial layout and textual content.

---

### Semantic Entity Labeling

The baseline combines:

- BERT semantic features,
- bounding-box spatial features,
- sequence-length metadata.

These features are passed through a multilayer perceptron.

Reported F1:

```text
0.57
```

---

### Entity Linking

Entity linking is formulated as binary classification over pairs of semantic entities.

Reported baseline:

```text
Precision: 2.1%
Recall:    99.2%
F1:        0.04
```

The very low F1 score demonstrates that understanding relationships between form entities is particularly challenging.

The authors suggest that relational information could naturally be represented using graphs.

---

## Main Contributions

The paper contributes:

1. A formal definition of the form-understanding problem.
2. A dataset of 199 fully annotated noisy scanned forms.
3. An annotation structure covering words, semantic entities, bounding boxes, and relationships.
4. Baselines for text detection, OCR, word grouping, semantic labeling, and entity linking.
5. Metrics for evaluating different stages of form understanding.

---

## Advantages

- Real scanned forms rather than synthetic documents.
- Rich spatial annotations.
- Semantic entity labels.
- Explicit relationships between entities.
- Supports several document-understanding tasks.
- Encourages template-agnostic form understanding.
- Provides standardized train/test splits.
- Useful for studying the transition from OCR to structured information extraction.

---

## Limitations

The paper explicitly identifies two important limitations.

### Limited Dataset Size and Diversity

FUNSD contains only 199 forms.

Although forms were selected from several fields, the authors cannot guarantee that the dataset contains enough variation to build a completely generalizable form-understanding system.

### Mostly Machine-Written Text

Most textual content in FUNSD is machine-written.

Some handwriting exists, particularly in:

- signatures,
- dates,

but handwritten text is not the main focus of the dataset.

This is particularly important for my thesis.

---

## IAM vs FUNSD

| Aspect | IAM | FUNSD |
|---|---|---|
| Primary Goal | Handwriting recognition | Form understanding |
| Main Input | Handwritten documents/lines | Noisy scanned forms |
| Handwriting | Central | Limited |
| OCR | Main task | Component of larger task |
| Spatial Layout | Not primary HTR objective | Central |
| Semantic Entities | No | Yes |
| Question/Answer Labels | No | Yes |
| Entity Relationships | No | Yes |
| Bounding Boxes | Used for segmentation | Used for structural understanding |
| Useful for My Thesis | HTR benchmark | Form-structure benchmark |

The two datasets therefore address complementary parts of my thesis problem.

```text
IAM
 │
 └── Handwriting Recognition
             │
             ▼
        MY THESIS
             ▲
             │
FUNSD
 │
 └── Form Understanding
```

---

## Relevance to My Thesis

My thesis focuses on OCR for **structured handwritten forms**.

FUNSD is important because it demonstrates that recognizing text is only one component of understanding a form.

A structured handwritten-form system may require:

```text
Form Image
     ↓
Text / Field Detection
     ↓
Handwriting Recognition
     ↓
Spatial Layout Understanding
     ↓
Semantic Entity Classification
     ↓
Entity / Field Linking
     ↓
Structured Output
```

FUNSD provides useful concepts and annotations for:

- field structure,
- spatial layout,
- semantic entities,
- question-answer relationships,
- template-agnostic form understanding.

These ideas can complement handwriting-recognition approaches such as TrOCR.

---

## Why FUNSD Is Not Identical to My Thesis Problem

FUNSD does not directly solve my complete research problem.

The major difference is that FUNSD contains **mostly machine-written text**, while my thesis focuses on **handwritten content in structured forms**.

Therefore:

```text
IAM
provides strong handwriting data
but limited form semantics.

FUNSD
provides strong form semantics
but limited handwriting.

My thesis
combines handwriting recognition
with structured form understanding.
```

This gap may provide an important motivation for the research.

---

## Potential Research Ideas

- Combine TrOCR handwriting recognition with FUNSD-style form understanding.
- Investigate whether field labels improve handwritten OCR accuracy.
- Use spatial information to provide context for ambiguous handwriting.
- Use known form templates to constrain OCR predictions.
- Study question-answer relationships in handwritten forms.
- Compare text-only OCR against layout-aware recognition.
- Investigate whether field type can improve recognition.

Example:

```text
Field: DATE

Ambiguous handwriting:
10/12/25

Knowing that the field is a DATE
could constrain possible interpretations.
```

This suggests that form structure could potentially provide contextual information to the handwriting-recognition system.

---

## Key Takeaways

- FUNSD introduces a benchmark for understanding noisy scanned forms.
- Form understanding goes beyond OCR.
- The dataset represents forms as interconnected semantic entities.
- Entities are labeled as QUESTION, ANSWER, HEADER, or OTHER.
- Spatial layout is important for understanding relationships between text elements.
- Entity linking connects related semantic entities.
- Real-world noise makes document understanding more difficult.
- FUNSD and IAM address complementary aspects of my thesis.
- IAM focuses on handwriting recognition.
- FUNSD focuses on document structure and relationships.
- Structured handwritten-form recognition requires concepts from both areas.