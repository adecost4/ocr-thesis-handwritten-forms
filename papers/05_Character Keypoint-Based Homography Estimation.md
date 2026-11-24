# Paper 05 — Character Keypoint-Based Homography Estimation

## Citation

Mahajan, K., Sharma, M., & Vig, L.

**Character Keypoint-Based Homography Estimation in Scanned Documents for Efficient Information Extraction**

TCS Research, New Delhi, India, 2019.

arXiv:1911.05870

---

# Research Problem

Information extraction from scanned or camera-captured structured documents becomes difficult when the incoming document is not geometrically aligned with the original template.

Documents such as:

- insurance claim forms,

- bank forms,

- application forms,

- and other fixed-layout documents

may be scanned or photographed with variations in:

- rotation,

- translation,

- scaling,

- viewpoint,

- illumination,

- and background.

If predefined coordinates are used to extract fields from an unaligned document, the system may crop the wrong region.

The paper therefore investigates:

> How can a scanned or camera-captured textual document be accurately aligned with a known reference template so that predefined information fields can be reliably extracted?

The basic problem is:

```text
Empty Reference Template
          +
Filled Test Document
          ↓
Document Alignment
          ↓
Field Extraction
          ↓
Information Recognition
```

The authors solve the alignment problem using **character-based keypoints and homography estimation**.

---

# Motivation

Structured forms normally contain a fixed layout.

For example:

```text
Name:       __________________

Address:    __________________

Date:       __________________

ID Number:  __________________
```

The coordinates of these fields can be predefined on an empty template.

However, the same form may appear differently after scanning or photographing:

```text
Original Template
       ↓
Rotated / Shifted / Scaled
       ↓
Incoming Form
```

Therefore:

```text
Fixed Coordinates
        +
Unaligned Form
        ↓
Incorrect Field Crop
```

The incoming document should first be transformed into the coordinate system of the reference template.

After alignment:

```text
Aligned Form
     +
Known Template Coordinates
     ↓
Correct Field Extraction
```

The authors argue that reliable document alignment can reduce field-extraction errors and manual effort during document digitization.

---

# What Existed Before This Approach?

## Direct Pixel-Based Alignment

One category of existing methods estimates transformations by comparing pixel intensities.

The paper discusses Lucas–Kanade-based methods as an example.

These approaches rely on useful image-intensity gradients.

However, text documents contain many sharp textual edges rather than smooth gradients.

The authors report that this makes direct pixel-based alignment unsuitable for their scanned-document problem.

---

## Feature-Based Alignment

Another common approach is to detect local image features.

Examples discussed in the paper include:

```text
SIFT
ORB
```

A typical feature-based alignment pipeline is:

```text
Template Image
      ↓
Keypoint Detection
      ↓
Feature Descriptors
      ↓
Keypoint Matching
      ↓
Homography Estimation
      ↓
Alignment
```

However, textual documents contain:

- many sharp edges,

- repeated characters,

- similar visual structures,

- and large numbers of potential feature points.

The authors observe that SIFT and ORB can produce inconsistent keypoints between an original document and its transformed version.

This can lead to inaccurate correspondences and poor homography estimation.

---

# Proposed Approach

Instead of relying on generic visual features, the authors propose using:

**Character-Based Keypoints**

The printed characters already present in the form are used as geometric landmarks.

The high-level pipeline is:

```text
Reference Template
        +
Test Document
        ↓
Threshold Documents
        ↓
Tesseract OCR
        ↓
Detect Printed Words
        ↓
Character-Based Keypoint Extraction
        ↓
Keypoint Matching
        ↓
Homography Estimation
        ↓
Document Alignment
        ↓
Field Extraction
        ↓
OCR / HTR
        ↓
Extracted Information
```

The main idea is that the textual structure of the document itself can provide reliable alignment features.

---

# Step 1 — Image Thresholding

The first step is to threshold both:

```text
Empty Template
```

and:

```text
Filled Test Document
```

Thresholding helps reduce the effect of illumination variations.

Conceptually:

```text
Input Document
      ↓
Thresholding
      ↓
Processed Document
```

In the experiments, the authors report using an empirically determined binarization threshold of:

```text
170
```

---

# Step 2 — OCR-Based Word Detection

The authors use:

```text
Tesseract OCR
```

on both the template and test documents.

Tesseract identifies:

- words,

- word locations,

- and bounding boxes.

Conceptually:

```text
Document
   ↓
Tesseract
   ↓
Detected Words
   ↓
Word Bounding Boxes
```

An important aspect of this approach is that OCR is not being used only for final text recognition.

OCR is also used to help identify **geometric landmarks for document alignment**.

---

# Step 3 — Character-Based Keypoint Extraction

The central contribution of the paper is the use of distinctive points on printed characters as keypoints.

The authors observe that some characters contain clearly identifiable geometric tips.

Examples discussed in the paper include:

```text
A
V
T
Y
4
7
L
r
v
w
```

Depending on the character, the distinctive point may occur at the:

```text
Left
Right
Top
Bottom
```

The authors therefore construct four lists:

```text
begCharList
endCharList
topCharList
bottomCharList
```

These lists identify characters with distinctive geometric points at particular positions.

---

# Why Not Use Every Character?

Not every character provides a reliable keypoint.

For example, the paper avoids characters such as:

```text
O
D
```

because curved portions make precise keypoint localization difficult.

Therefore, the objective is not:

```text
Maximum Number of Keypoints
```

but rather:

```text
Reliable
+
Precise
+
Unambiguous Keypoints
```

This is important because inaccurate keypoints could negatively affect the final homography.

---

# Connected Component Analysis

After identifying suitable words, connected-component analysis is performed.

The first or last connected component of the word is examined depending on the selected character.

Conceptually:

```text
Detected Word
      ↓
Connected Components
      ↓
First / Last Component
      ↓
Character Tip
      ↓
Keypoint
```

The first and last components are used because they are expected to contain the first and last characters of the word.

The authors note that thresholding can sometimes cause characters to touch, so individual characters are not always perfectly separated.

---

# Additional Keypoint Filtering

The authors apply several heuristic checks to improve the reliability of detected keypoints.

## Short Words

Words containing two or fewer characters are ignored.

These are considered more likely to be false-positive Tesseract detections.

---

## Font Size

Very small text is avoided because thresholding may break small characters and produce unreliable detections.

---

## Spell Checking

The authors use the Python:

```text
Enchant
```

spell-checking library.

Candidate words are checked to ensure that they are valid English words.

This prevents OCR-generated junk words from being used for keypoint detection.

---

# Step 4 — Keypoint Matching

A detected word may appear multiple times within the same document.

Therefore, simply finding the same word in both documents is not sufficient.

The authors use:

**Neighborhood Information**

Conceptually:

```text
Template Word
      ↓
Nearby Words
      ↓
Neighborhood Context
      ↓
Compare
      ↓
Candidate Test Word
```

The surrounding words help identify whether a candidate in the test document corresponds to the correct word in the template.

The paper uses a threshold of:

```text
90%
```

A candidate test neighborhood is considered a match when it contains at least 90% of the words present in the corresponding template-word neighborhood.

This is conceptually similar to conventional feature descriptors, where the region surrounding a keypoint provides information for matching.

---

# Step 5 — Homography Estimation

After corresponding character keypoints have been identified, the system estimates the transformation between the test document and the template.

A homography is represented by a:

```text
3 × 3 transformation matrix
```

Conceptually:

```text
Point in Test Document
        ↓
Homography Matrix H
        ↓
Corresponding Point
in Template Coordinate System
```

At least four pairs of corresponding points are required to estimate a homography.

However, the authors provide a larger number of point correspondences to improve robustness.

---

# RANSAC

Some keypoint correspondences may still be incorrect.

The paper therefore uses:

```text
RANSAC
```

to reduce the influence of outliers.

Conceptually:

```text
Matched Keypoints
      ↓
Correct Matches + Outliers
      ↓
RANSAC
      ↓
Reliable Correspondences
      ↓
Homography
```

This improves the robustness of the final transformation.

---

# OpenCV Implementation

The paper uses OpenCV for homography estimation and perspective transformation.

The important operations are:

```text
findHomography()
```

and:

```text
warpPerspective()
```

The pipeline becomes:

```text
Matched Character Keypoints
        ↓
findHomography()
        ↓
Homography Matrix
        ↓
warpPerspective()
        ↓
Aligned Test Document
```

---

# Step 6 — Field Extraction

After the test document has been aligned with the template, field extraction becomes significantly simpler.

The user marks bounding boxes around fields of interest on the reference template.

Examples include:

```text
Name
Pet Name
Address
Hospital
Injury
```

Because the test document is now aligned with the template, corresponding coordinates can be used to retrieve the same fields.

Conceptually:

```text
Reference Template

Name: [Known Bounding Box]

             ↓
       Alignment

Test Document

Name: [Same Coordinates]
             ↓
         Field Crop
```

This is particularly useful for fixed-layout structured forms.

---

# Printed vs Handwritten Classification

After field extraction, the system determines whether the extracted text is:

```text
Printed
```

or:

```text
Handwritten
```

The authors train a five-layer CNN classifier for this task.

The paper reports approximately:

```text
98.5% classification accuracy
```

on fields extracted from their documents.

---

# Text Recognition

Different recognition methods are then used depending on the text type.

For printed text:

```text
Extracted Printed Field
          ↓
      Tesseract
          ↓
    Recognized Text
```

For handwritten text:

```text
Extracted Handwritten Field
          ↓
   HTR Model / Google Vision
          ↓
      Recognized Text
```

This demonstrates an important architectural separation:

```text
Document Alignment
        ↓
Field Extraction
        ↓
Text Recognition
```

The paper's primary contribution is therefore **alignment and extraction**, not a new handwriting-recognition model.

---

# Complete Pipeline

```text
                   EMPTY TEMPLATE
                         +
                   FILLED TEST FORM
                         │
                         ▼
                    Thresholding
                         │
                         ▼
                    Tesseract OCR
                         │
                         ▼
                 Printed Word Detection
                         │
                         ▼
              Character-Based Keypoints
                         │
                         ▼
                  Keypoint Matching
                         │
                         ▼
                       RANSAC
                         │
                         ▼
                Homography Estimation
                         │
                         ▼
                  warpPerspective()
                         │
                         ▼
                 ALIGNED TEST FORM
                         │
                         ▼
                Predefined Field Crops
                         │
                         ▼
                Printed / Handwritten?
                    │             │
                    ▼             ▼
                Tesseract        HTR
                    │             │
                    └──────┬──────┘
                           ▼
                  Extracted Information
```

---

# Datasets

The authors evaluate the proposed approach on two anonymized real-world health-insurance form datasets.

## Dataset 1

The first dataset contains:

```text
15 Insurance Claim Forms
+
1 Empty Reference Template
```

The forms contain both printed and handwritten information.

---

## Dataset 2

The second dataset contains:

```text
15 Life Insurance Application Forms
+
1 Empty Reference Template
```

The filled information in this dataset is handwritten.

The documents include variations in:

- illumination,

- background,

- rotation,

- translation,

- scaling,

- and affine transformation.

For experimentation, all documents are resized to:

```text
1600 × 2400
```

and converted to grayscale.

---

# Evaluation

The authors evaluate the overall information-extraction pipeline.

The primary quantitative measure reported is:

```text
Character Recognition Accuracy
```

for the fields retrieved after document alignment.

This evaluates the practical effect of the alignment and extraction pipeline on downstream information recognition.

---

# Results — Dataset 1

Examples reported for the first insurance dataset include:

| Field | Tesseract | HTR Model | Google Vision |
| - | -: | -: | -: |
| Name | 98.6% | 88.0% | 92.2% |
| Pet Name | 99.2% | 89.5% | 92.9% |
| Address | 98.3% | 80.4% | 85.8% |
| Hospital | 98.7% | 77.3% | 82.5% |
| Injury | 97.1% | 78.0% | 82.6% |

Printed fields recognized using Tesseract achieve high character-recognition accuracy.

Handwritten fields remain more challenging and depend on the downstream handwriting-recognition system.

---

# Results — Dataset 2

Examples reported for the second dataset include:

| Field | HTR Model | Google Vision |
| - | -: | -: |
| Agency Name | 78.7% | 83.5% |
| Agency Address | 78.3% | 84.6% |
| First Name | 80.1% | 84.5% |
| Last Name | 80.7% | 86.7% |
| Applicant Address | 78.4% | 82.6% |
| City | 81.9% | 93.5% |
| State | 83.2% | 89.6% |

These results demonstrate an important distinction:

```text
Correct Alignment
        ↓
Correct Field Extraction
```

does not automatically mean:

```text
Perfect Handwriting Recognition
```

The quality of the downstream HTR system remains important.

---

# Robustness Experiments

The authors test the alignment approach under:

```text
Rotation
Translation
Scaling
```

---

## Rotation

The paper reports that performance remains unaffected for rotations up to approximately:

```text
±7°
```

Beyond this range, Tesseract performance degrades significantly.

This reduces the reliability of keypoint detection and therefore document alignment.

---

## Translation

The method handles horizontal and vertical translations approximately within:

```text
±40%
```

of the document width and height.

---

## Scaling

For the evaluated datasets, the approach works when document width and height are varied approximately between:

```text
50% to 200%
```

of their original values.

Performance eventually degrades if scaling causes the document to become excessively pixelated.

---

# Advantages

## 1. Designed Specifically for Text Documents

The approach uses the textual information already present in structured documents rather than treating the document as a generic natural image.

---

## 2. Template-Aware

The method explicitly uses:

```text
Reference Template
+
Incoming Filled Form
```

This makes it directly applicable to fixed-layout structured forms.

---

## 3. Enables Predefined Field Extraction

After alignment, known coordinates from the template can be reused to extract corresponding fields from incoming documents.

---

## 4. Lightweight Alignment Method

The authors describe the proposed approach as fast and memory-efficient compared with complex deep-learning-based alignment approaches.

---

## 5. Uses Practical Tools

The pipeline relies on:

```text
Tesseract
OpenCV
Connected Components
RANSAC
```

rather than requiring a large learned alignment model.

---

## 6. Handles Several Geometric Variations

The experiments investigate:

- rotation,

- translation,

- scaling,

- illumination variation,

- and background variation.

---

# Limitations

## 1. Dependence on OCR

The alignment method relies on Tesseract successfully detecting printed words.

Therefore:

```text
Poor Tesseract Detection
          ↓
Poor Character Keypoints
          ↓
Poor Correspondences
          ↓
Poor Homography
          ↓
Alignment Failure
```

The paper's rotation experiments demonstrate this dependency.

---

## 2. Requires Suitable Printed Template Text

The approach depends on printed words being present in the template and test documents.

Documents containing very little suitable printed text may not provide enough reliable keypoints.

---

## 3. Handcrafted Character Selection

The method manually defines:

```text
begCharList
endCharList
topCharList
bottomCharList
```

Therefore, part of the alignment process relies on manually selected character properties.

---

## 4. Language Dependence

The implementation uses:

```text
English Characters
+
English Spell Checking
```

This means parts of the original approach are language-specific.

---

## 5. Small Evaluation Dataset

Each dataset contains only:

```text
15 Filled Forms
+
1 Template
```

Therefore, the experiments demonstrate feasibility on real documents but do not establish broad generalization across many different form types.

---

## 6. Rotation Limitation

The reported approach remains unaffected only up to approximately:

```text
±7°
```

before Tesseract performance begins to significantly affect alignment.

---

## 7. HTR Remains a Separate Problem

The proposed approach improves:

```text
Document Alignment
+
Field Extraction
```

but does not itself solve handwritten text recognition.

A separate HTR model is required after field extraction.

---

# Relevance to My Thesis

This paper is highly relevant to the **template-aware component** of my thesis.

My thesis investigates:

**Template-Aware Handwritten Text Recognition for Structured Forms**

The broader thesis pipeline is:

```text
Structured Form
      ↓
Template Alignment
      ↓
Field Extraction
      ↓
Handwritten Text Recognition
      ↓
Field-Aware Processing
      ↓
Structured Output
```

My previous literature primarily focuses on the recognition stage.

For example:

```text
CRNN
TrOCR
HTR-VT
```

address:

```text
Handwritten Image
        ↓
HTR Model
        ↓
Recognized Text
```

This paper instead addresses:

```text
Full Structured Form
        ↓
Template Alignment
        ↓
Field Extraction
```

Therefore, it provides an important bridge between full-document processing and handwritten text recognition.

---

# Connection to My Current TrOCR Baseline

My current TrOCR baseline uses already segmented IAM handwriting lines:

```text
IAM Handwritten Line
        ↓
Pretrained TrOCR
        ↓
Prediction
        ↓
CER / WER / Exact Match
```

However, this assumes that the correct handwriting region has already been identified.

In the actual thesis problem, the input may instead be:

```text
Full Scanned Form
```

Therefore, additional stages are required:

```text
Full Structured Form
        ↓
Template Alignment
        ↓
Field Extraction
        ↓
Handwritten Field
        ↓
TrOCR
        ↓
Recognized Text
```

The approach proposed in this paper provides one possible solution for the alignment and field-extraction stages.

---

# Connection to Template-Aware Recognition

Structured forms contain information that generic HTR datasets do not provide.

Examples include:

```text
Field Position
Field Label
Expected Field Type
Expected Character Set
Expected Format
Template Geometry
```

Once the incoming form is aligned with the reference template, this structural information becomes available.

For example:

```text
Template Field
      ↓
DATE OF BIRTH
      ↓
Known Coordinates
      ↓
Crop from Aligned Form
      ↓
HTR Prediction
      ↓
Field Type = DATE
      ↓
Format Validation
```

Therefore, alignment enables more than simply cropping the handwriting.

It can also provide semantic information about what the recognized text is expected to represent.

---

# Connection to Field-Aware Processing

Suppose the system knows that a particular crop represents:

```text
Field = Date
```

Then expected information may include:

```text
Expected Characters = Digits
Expected Format = MM/DD/YYYY
```

Similarly:

```text
Field = ID Number

Expected Characters = Digits / Alphanumeric
Expected Length = Known Range
```

This creates the possibility of using template information during post-processing or validation.

Therefore:

```text
Template Alignment
        ↓
Field Identification
        ↓
HTR
        ↓
Field-Aware Validation
```

could potentially improve the reliability of structured information extraction.

---

# Potential Research Ideas

## Idea 1 — Template Alignment + TrOCR

Implement:

```text
Reference Template
        +
Filled Structured Form
        ↓
Homography Alignment
        ↓
Field Cropping
        ↓
TrOCR
        ↓
Structured Output
```

This would provide an initial end-to-end prototype for the thesis.

---

## Idea 2 — Measure the Impact of Alignment

Compare:

```text
Unaligned Field Extraction
        ↓
TrOCR
```

against:

```text
Template Alignment
        ↓
Field Extraction
        ↓
TrOCR
```

Possible metrics:

```text
CER
WER
Exact Field Accuracy
```

Research question:

> How much does template alignment affect downstream handwritten-field recognition accuracy?

---

## Idea 3 — Separate Alignment Errors from Recognition Errors

The system can fail at different stages.

For example:

```text
Input Form
    ↓
Alignment
    ↓
Correct Field Crop?
    │
    ├── NO
    │     ↓
    │ Alignment / Extraction Error
    │
    └── YES
          ↓
         HTR
          ↓
Correct Transcription?
          │
          ├── NO
          │     ↓
          │ Recognition Error
          │
          └── YES
                ↓
             Success
```

Separating these errors would provide a more meaningful evaluation of an end-to-end structured-form system.

---

## Idea 4 — Compare Alignment Methods

Possible alignment approaches could include:

```text
Character Keypoints
SIFT
ORB
Template Matching
Other Feature-Based Methods
```

They could be evaluated under controlled:

```text
Rotation
Translation
Scaling
Perspective Variation
```

This could determine which alignment approach is most suitable for the forms used in the thesis.

---

## Idea 5 — Field-Aware Recognition

Once alignment identifies the field type, the HTR result can potentially be validated using field-specific constraints.

For example:

```text
Date
→ Expected date format

Phone Number
→ Expected digits

Student ID
→ Expected character set and length

Name
→ Alphabetic text
```

This could form a later template-aware improvement beyond basic alignment.

---

# Questions and Answers

## 1. What problem does this paper solve?

The paper addresses the alignment of scanned or camera-captured textual documents with a reference template so that predefined information fields can be reliably extracted.

---

## 2. Why is alignment necessary?

Incoming forms may be rotated, translated, scaled, or captured from different viewpoints.

Without alignment, predefined template coordinates may point to incorrect regions.

---

## 3. What is a homography?

A homography is a geometric transformation that maps corresponding points between two views of a planar surface.

It is represented using a:

```text
3 × 3 matrix
```

---

## 4. How many correspondences are required?

At least four matched point pairs are required to estimate a homography.

The authors use more correspondences to improve robustness.

---

## 5. Why not simply use SIFT or ORB?

The paper reports inconsistent keypoint detection when these generic feature descriptors are applied to textual documents.

Sharp textual edges and repetitive structures can produce unreliable correspondences.

---

## 6. What is the main contribution?

The main contribution is a method for using distinctive points on printed characters as reliable keypoints for document alignment.

---

## 7. Why is Tesseract used?

Tesseract detects words and their bounding boxes.

These detected words allow the system to locate suitable characters from which precise keypoints can be extracted.

---

## 8. Why are characters such as A, V, T, and Y useful?

They contain distinctive geometric tips that can be localized more precisely.

---

## 9. Why are characters such as O and D avoided?

Their curved regions make exact keypoint localization less precise.

---

## 10. Why is neighborhood information used?

A word may occur multiple times within the same form.

Nearby words provide contextual information that helps identify the correct corresponding word.

---

## 11. What does the 90% threshold represent?

A candidate neighborhood in the test document is accepted when it contains at least 90% of the words present in the corresponding template-word neighborhood.

---

## 12. Why is RANSAC used?

RANSAC helps remove incorrect or noisy keypoint correspondences before estimating the final homography.

---

## 13. Which OpenCV operations are used?

The paper uses:

```text
findHomography()
```

to estimate the transformation and:

```text
warpPerspective()
```

to align the test document.

---

## 14. What happens after alignment?

The predefined field coordinates from the reference template are used to extract corresponding regions from the aligned test document.

---

## 15. Does the paper propose a new HTR model?

No.

The primary contribution is document alignment and field extraction.

Handwritten fields are recognized using a separate HTR model or Google Vision API.

---

## 16. What datasets are used?

Two anonymized real-world insurance-form datasets are used.

Each contains:

```text
15 Filled Forms
+
1 Empty Reference Template
```

---

## 17. How much rotation does the method handle?

The paper reports that system performance is unaffected for rotations up to approximately:

```text
±7°
```

Beyond this, Tesseract recognition degrades significantly.

---

## 18. How much translation does the method handle?

The reported experiments include horizontal and vertical translations approximately within:

```text
±40%
```

of the document dimensions.

---

## 19. What scaling range is reported?

For the evaluated datasets, the approach works when document width and height are varied approximately between:

```text
50% and 200%
```

of their original values, provided that excessive pixelation does not occur.

---

## 20. Why is this paper important for my thesis?

My current HTR experiments assume that the handwriting has already been extracted.

This paper addresses the preceding stages:

```text
Full Structured Form
        ↓
Template Alignment
        ↓
Field Extraction
        ↓
HTR
```

Therefore, it provides literature support for the **template-aware structured-form component** of the thesis.

---

# Architecture Summary

```text
                   STRUCTURED FORM
                         +
                 REFERENCE TEMPLATE
                         │
                         ▼
                    Thresholding
                         │
                         ▼
                    Tesseract OCR
                         │
                         ▼
               Character Keypoints
                         │
                         ▼
                  Keypoint Matching
                         │
                         ▼
                       RANSAC
                         │
                         ▼
                Homography Estimation
                         │
                         ▼
                 Document Alignment
                         │
                         ▼
                   Field Extraction
                         │
                         ▼
                 Handwritten Field
                         │
                         ▼
               ┌─────────┼─────────┐
               │         │         │
               ▼         ▼         ▼
             CRNN      TrOCR     HTR-VT
               │         │         │
               └─────────┼─────────┘
                         ▼
                  Recognized Text
                         │
                         ▼
                Field-Aware Processing
                         │
                         ▼
                  Structured Output
```

---

# Main Takeaway

The most important lesson from this paper is:

> **For fixed-layout structured documents, accurate template alignment can transform full-document information extraction into a simpler predefined field-extraction problem.**

The paper proposes an alignment approach based on:

```text
OCR-Detected Printed Words
          +
Distinct Character Keypoints
          +
Neighborhood-Based Matching
          +
RANSAC
          +
Homography Estimation
```

The resulting transformation aligns an incoming document with a known reference template.

After alignment:

```text
Known Template Coordinates
          ↓
Field Extraction
          ↓
OCR / HTR
```

becomes possible.

For my thesis, this paper provides an important bridge between:

```text
Full Scanned Structured Form
```

and:

```text
Isolated Handwritten Field
```

My earlier literature on CRNN, TrOCR, and HTR-VT primarily investigates how to recognize handwriting after the text region is available.

This paper addresses how that handwriting region can first be located and extracted from a complete structured form.

Therefore, it supports the broader thesis pipeline:

```text
Structured Form
      ↓
Template Alignment
      ↓
Field Extraction
      ↓
Handwritten Text Recognition
      ↓
Field-Aware Processing
      ↓
Structured Output
```

This makes the paper particularly important for moving the thesis from benchmark HTR experiments on already-segmented IAM lines toward the actual problem of **template-aware handwritten information extraction from complete structured forms**.
