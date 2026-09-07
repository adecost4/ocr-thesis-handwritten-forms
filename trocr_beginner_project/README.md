# TrOCR Beginner Project

A beginner-friendly starter project for learning handwritten OCR using Microsoft's TrOCR model.

This project demonstrates:

- Running inference with a pretrained TrOCR model
- Loading images from a CSV manifest
- Understanding the OCR pipeline
- Preparing for fine-tuning on IAM or your own handwriting dataset

---

## Project structure

```
trocr_beginner_project/
│
├── data/
│   ├── sample/
│   │   ├── images/
│   │   └── sample.csv
│   │
│   └── processed/
│
├── notebooks/
│   └── 01_trocr_beginner.ipynb
│
├── src/
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<username>/<repo>.git
cd <repo>/trocr_beginner_project
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run

Open

```
notebooks/01_trocr_beginner.ipynb
```

using

- VS Code
- Jupyter Notebook
- JupyterLab
- Google Colab

Run all cells.

---

## Sample dataset

The repository already includes a tiny sample dataset.

```
data/sample/images/
data/sample/sample.csv
```

This lets you verify the entire OCR pipeline before using a larger dataset.

---

## Next steps

Replace the sample data with

- IAM Handwriting Database
- Your own handwritten forms
- Custom OCR datasets

and continue with fine-tuning.
