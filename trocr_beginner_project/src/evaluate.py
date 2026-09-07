
from __future__ import annotations

import numpy as np
from jiwer import cer as jiwer_cer, wer as jiwer_wer


def compute_metrics_from_strings(pred_texts, ref_texts):
    pred_texts = [s.strip() for s in pred_texts]
    ref_texts = [s.strip() for s in ref_texts]
    return {
        "cer": jiwer_cer(ref_texts, pred_texts),
        "wer": jiwer_wer(ref_texts, pred_texts),
    }
