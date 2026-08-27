# Handwritten Text Recognition for Structured Forms

**Master's Thesis Research | Computer Vision • Deep Learning • Document AI**

This repository contains my Master's thesis research on **Handwritten Text
Recognition (HTR) for structured documents**, particularly fixed-template
forms such as banking and government forms.

The research investigates whether structural information available in
fixed-template forms—such as field location, field type, and expected
content—can improve handwritten text recognition compared with
general-purpose HTR approaches.

---

## Research Objective

Develop and evaluate a template-aware handwritten text recognition pipeline
for extracting handwritten information from predefined fields in structured
forms.

A key research objective is to identify and experimentally evaluate a focused
hypothesis that provides measurable improvement over existing baseline
approaches.

---

## Current Research Questions

- How well do pretrained HTR models such as TrOCR generalize to structured forms?
- How does TrOCR compare with CRNN-based recognition?
- How much does document preprocessing affect recognition accuracy?
- Can fixed-template information improve field-level recognition?
- Can field-specific constraints reduce recognition errors?

These questions will evolve as the literature review and experiments progress.

---

## Proposed Pipeline

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

---

## Technologies

- Python
- PyTorch
- Hugging Face Transformers
- TrOCR
- OpenCV
- Google Colab
- Pandas / NumPy

Planned:
- CRNN + CTC
- IAM Handwriting Dataset
- CER / WER evaluation

---

## Current Progress

### Completed

- [x] Research environment setup
- [x] Google Colab development environment
- [x] Pretrained TrOCR inference
- [x] Initial experiments on clean and real-world handwriting
- [x] GitHub research repository
- [x] Initial thesis research plan

### In Progress

- [ ] HTR literature review
- [ ] TrOCR baseline evaluation
- [ ] IAM dataset exploration
- [ ] OpenCV preprocessing experiments
- [ ] CER and WER implementation

### Upcoming

- [ ] CRNN + CTC baseline
- [ ] CRNN vs TrOCR comparison
- [ ] Fixed-template form alignment
- [ ] Field extraction pipeline
- [ ] Structured-form dataset experiments
- [ ] Research hypothesis evaluation

---

## Repository Structure

    ocr-thesis-handwritten-forms/
    |
    ├── notebooks/       # Colab/Jupyter experiments
    ├── src/             # Reusable Python modules
    ├── experiments/     # Experiment configurations and results
    ├── literature/      # Literature review and research notes
    ├── docs/            # Thesis planning and weekly progress
    ├── data/            # Dataset instructions (datasets not committed)
    ├── results/         # Evaluation results and figures
    ├── requirements.txt
    └── README.md

---

## Evaluation

The primary evaluation metrics will include:

- Character Error Rate (CER)
- Word Error Rate (WER)
- Exact Field Accuracy

Additional metrics may be introduced depending on the final research
hypothesis.

---

## Research Progress

| Period | Focus |
|---|---|
| Aug–Sep 2026 | Literature, HTR foundations, TrOCR/CRNN baselines |
| Oct–Nov 2026 | Structured forms and field extraction |
| Nov–Dec 2026 | Research hypothesis and preliminary experiments |
| Jan–Mar 2027 | Main experiments and evaluation |
| Mar–May 2027 | Thesis, publication, demo and defense |

---

## Experiment Tracking

Experiments are documented under `experiments/`.

Each experiment records:

- Research question / hypothesis
- Dataset
- Model
- Preprocessing
- Configuration
- CER / WER / field accuracy
- Observations
- Conclusions
- Next experiment

---

## Status

🚧 **Active Master's Thesis Research — 2026–2027**

The research methodology, hypotheses, and implementation are actively evolving
as experiments and literature review progress.
