
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset


@dataclass
class Sample:
    image_path: str
    text: str


class HandwritingDataset(Dataset):
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.reset_index(drop=True)

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int):
        row = self.df.iloc[idx]
        image = Image.open(row["image_path"]).convert("RGB")
        return {"image": image, "text": str(row["text"])}
