from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

IAM_DIR = PROJECT_ROOT / "data" / "iam"

LINES_FILE = IAM_DIR / "ascii" / "lines.txt"

LINES_DIR = IAM_DIR / "lines"

rows = []

with open(LINES_FILE, encoding="utf-8") as f:

    for line in f:

        if line.startswith("#"):

            continue

        parts = line.strip().split()

        if len(parts) < 9:

            continue

        line_id = parts[0]

        status = parts[1]

        if status != "ok":

            continue

        transcription = " ".join(parts[8:]).replace("|", " ")

        folder1 = line_id[:3]

        folder2 = line_id[:7]

        image_path = (
            LINES_DIR
            / folder1
            / folder2
            / f"{line_id}.png"
        )

        if image_path.exists():

            rows.append({

                "id": line_id,

                "image": str(image_path),

                "text": transcription

            })

df = pd.DataFrame(rows)

print(df.head())

print()

print("Total samples:", len(df))

output = IAM_DIR / "iam_sample.csv"

df.to_csv(output, index=False)

print()

print("Saved:", output)