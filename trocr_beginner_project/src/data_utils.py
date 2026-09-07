
from __future__ import annotations

from pathlib import Path
from typing import Tuple
import pandas as pd


def load_manifest(csv_path: str | Path, image_root: str | Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if not {"image_path", "text"}.issubset(df.columns):
        raise ValueError("CSV must contain columns: image_path,text")

    csv_path = Path(csv_path)
    image_root = Path(image_root)

    def resolve(p: str) -> str:
        pp = Path(p)
        if pp.is_absolute():
            return str(pp)
        return str((image_root / pp).resolve())

    df = df.copy()
    df["image_path"] = df["image_path"].map(resolve)
    df["text"] = df["text"].fillna("").astype(str)
    return df
