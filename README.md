# Handwritten Text Recognition for Structured Forms

**Master's Thesis Research | Computer Vision • Deep Learning • Document AI**

This repository contains my Master's thesis research on **Handwritten Text Recognition (HTR) for structured documents**, particularly fixed-template forms such as banking and government forms.

The research investigates whether structural information available in fixed-template forms—such as field location, field type, and expected content—can improve handwritten text recognition compared with general-purpose HTR approaches.

> 🚧 **Active Research — 2026–2027**
> The research methodology, experiments, and hypotheses are evolving as the thesis progresses.

---

## Research Objective

The objective of this research is to develop and evaluate a **template-aware handwritten text recognition pipeline** for extracting handwritten information from predefined fields in structured forms.

Beyond developing a functional OCR/HTR system, the thesis aims to identify and experimentally evaluate a focused research hypothesis that provides a measurable improvement over baseline approaches.

---

## Current Research Questions

* How well do pretrained HTR models such as TrOCR generalize to structured forms?
* How does Transformer-based recognition compare with CRNN-based approaches?
* How much does image preprocessing affect handwriting recognition accuracy?
* Can fixed-template information improve field-level recognition?
* Can field-specific constraints reduce recognition errors?

These questions will be refined based on literature review, baseline experiments, and error analysis.

---

## Proposed Pipeline

```text
Scanned / Photographed Form
            |
            v
     Template Alignment
            |
            v
      Field Extraction
            |
            v
Handwritten Text Recognition
      (CRNN / TrOCR)
            |
            v
  Field-aware Processing
            |
            v
     Structured Output
```

---

## Current Implementation

### TrOCR Beginner Project

The first implementation milestone is a beginner-friendly **TrOCR inference pipeline** using Microsoft's pretrained handwritten TrOCR model.

Current implementation includes:

* Loading Microsoft's pretrained `trocr-base-handwritten` model
* Loading handwritten images using a CSV manifest
* Running image-to-text inference
* Testing recognition on clean and real-world handwriting
* Using Google Colab for GPU-based experimentation
* Establishing the project structure for future IAM experiments and fine-tuning

Project:

```text
trocr_beginner_project/
├── data/
│   ├── sample/
│   │   ├── images/
│   │   └── sample.csv
│   └── processed/
├── notebooks/
│   └── 01_trocr_beginner.ipynb
├── src/
├── requirements.txt
└── README.md
```

This starter implementation serves as the foundation for the upcoming **TrOCR baseline evaluation on IAM and structured handwritten form data**.

---

## Technologies

### Currently Using

* Python
* PyTorch
* Hugging Face Transformers
* TrOCR
* Google Colab
* Pandas
* NumPy
* Jupyter Notebooks

### Planned / In Progress

* OpenCV
* CRNN + LSTM
* CTC Loss
* IAM Handwriting Database
* CER / WER evaluation
* Template alignment
* Field extraction

---

## Research Progress

### Completed

* [x] Thesis research direction established
* [x] Research environment setup
* [x] GitHub research repository
* [x] Google Colab environment
* [x] Pretrained TrOCR model setup
* [x] First TrOCR inference pipeline
* [x] CSV-based sample dataset loading
* [x] Initial experiments on clean handwriting
* [x] Initial experiments on real-world handwriting
* [x] Initial thesis research plan

### Currently Working On

* [ ] HTR literature review
* [ ] Understanding TrOCR architecture
* [ ] IAM dataset exploration
* [ ] TrOCR baseline evaluation
* [ ] OpenCV preprocessing experiments
* [ ] CER and WER implementation
* [ ] Documenting baseline failure cases

### Upcoming

* [ ] CNN / RNN / LSTM foundations
* [ ] CRNN + CTC baseline
* [ ] CRNN vs TrOCR comparison
* [ ] Fixed-template form alignment
* [ ] Field extraction pipeline
* [ ] Structured-form dataset experiments
* [ ] Candidate research hypothesis evaluation
* [ ] Proposed thesis contribution

---

## Evaluation

The primary evaluation metrics currently planned are:

* **Character Error Rate (CER)**
* **Word Error Rate (WER)**
* **Exact Field Accuracy**

The evaluation strategy may evolve depending on the final research hypothesis.

---

## Research Roadmap

| Period       | Research Focus                                            |
| ------------ | --------------------------------------------------------- |
| Aug–Sep 2026 | Literature review, HTR foundations, TrOCR/CRNN baselines  |
| Oct–Nov 2026 | Structured forms, template alignment and field extraction |
| Nov–Dec 2026 | Research hypothesis and preliminary experiments           |
| Jan–Mar 2027 | Main experiments, evaluation and error analysis           |
| Mar–May 2027 | Thesis writing, publication, demo and defense             |

---

## Repository Structure

```text
ocr-thesis-handwritten-forms/
│
├── trocr_beginner_project/  # First TrOCR implementation
├── notebooks/               # Research notebooks and experiments
├── src/                     # Reusable Python modules
├── experiments/             # Experiment configurations and results
├── literature/              # Literature review and paper notes
├── docs/                    # Thesis plans and weekly research notes
├── data/                    # Dataset instructions / metadata
├── results/                 # Metrics, tables and figures
├── requirements.txt
└── README.md
```

> Large research datasets and copyrighted papers are not stored directly in this repository.

---

## Experiment Tracking

Experiments will be documented with:

* Research question / hypothesis
* Dataset
* Model and configuration
* Preprocessing
* Baseline
* CER / WER / field accuracy
* Observations
* Failure cases
* Conclusion
* Next experiment

---

## Research Hypothesis Development

The final thesis hypothesis has not yet been fixed.

Current candidate directions include:

1. **Field-aware recognition** — using field type or expected content to reduce recognition errors.
2. **Template-aware recognition** — exploiting known form structure during extraction/recognition.
3. **Preprocessing and robustness** — improving recognition under scan noise, skew, perspective distortion, or background interference.
4. **Domain adaptation** — adapting pretrained handwriting models to structured-form handwriting with limited labeled data.

The final hypothesis will be selected based on literature review, baseline experiments, and systematic error analysis.

---

## Current Focus

**September 2026**

> Establish a reproducible TrOCR baseline, study HTR literature and IAM, implement CER/WER evaluation, and identify meaningful baseline failure cases that may lead to a testable research hypothesis.

---

## Disclaimer

This repository contains ongoing academic research as part of a Master's thesis. Results and conclusions should be considered preliminary until the research is completed.
