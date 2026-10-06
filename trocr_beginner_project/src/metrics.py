"""
metrics.py

Utility functions for evaluating OCR predictions.

Metrics included:
- Character Error Rate (CER)
- Word Error Rate (WER)
- Exact Field Accuracy
"""

from jiwer import cer, wer


def calculate_cer(reference: str, prediction: str) -> float:
    """
    Calculate Character Error Rate (CER).

    Lower is better.
    0.0 indicates a perfect prediction.
    """
    return cer(reference, prediction)


def calculate_wer(reference: str, prediction: str) -> float:
    """
    Calculate Word Error Rate (WER).

    Lower is better.
    0.0 indicates a perfect prediction.
    """
    return wer(reference, prediction)


def exact_field_accuracy(reference: str, prediction: str) -> int:
    """
    Returns:
        1 if prediction exactly matches the reference.
        0 otherwise.
    """
    return int(reference.strip() == prediction.strip())