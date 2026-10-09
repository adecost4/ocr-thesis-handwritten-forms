from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

IAM_DIR = PROJECT_ROOT / "data" / "iam"

LINES_FILE = IAM_DIR / "ascii" / "lines.txt"

LINES_DIR = IAM_DIR / "lines"

OUTPUT_FILE = IAM_DIR / "iam_sample.csv"


# --------------------------------------------------
# Verify required files
# --------------------------------------------------

if not LINES_FILE.exists():
    raise FileNotFoundError(
        f"Missing IAM annotation file:\n{LINES_FILE}"
    )

if not LINES_DIR.exists():
    raise FileNotFoundError(
        f"Missing IAM line-image directory:\n{LINES_DIR}"
    )


# --------------------------------------------------
# Parse IAM lines.txt
# --------------------------------------------------

rows = []

total_annotations = 0
ok_annotations = 0
missing_images = 0
bad_segmentations = 0


with open(LINES_FILE, "r", encoding="utf-8") as f:

    for raw_line in f:

        line = raw_line.strip()

        # Ignore comments and blank lines
        if not line or line.startswith("#"):
            continue

        total_annotations += 1

        # IAM format:
        #
        # id status graylevel components
        # x y w h transcription
        #
        # Split only the first 8 separators so that
        # the complete transcription remains together.

        parts = line.split(maxsplit=8)

        if len(parts) != 9:
            print("Skipping malformed annotation:")
            print(line)
            continue

        (
            line_id,
            status,
            graylevel,
            components,
            x,
            y,
            width,
            height,
            transcription,
        ) = parts

        # Ignore segmentation-error samples
        if status != "ok":
            bad_segmentations += 1
            continue

        ok_annotations += 1

        # IAM uses | as the word separator
        transcription = transcription.replace("|", " ")

        # Example:
        # a01-000u-00
        #
        # becomes:
        # lines/a01/a01-000u/a01-000u-00.png

        folder1 = line_id[:3]
        folder2 = line_id.rsplit("-", 1)[0]

        image_path = (
            LINES_DIR
            / folder1
            / folder2
            / f"{line_id}.png"
        )

        if not image_path.exists():

            missing_images += 1

            continue

        rows.append(
            {
                "id": line_id,
                "image": str(image_path),
                "text": transcription,
            }
        )


# --------------------------------------------------
# Create dataframe
# --------------------------------------------------

df = pd.DataFrame(rows)


# --------------------------------------------------
# Validation
# --------------------------------------------------

if df["id"].duplicated().any():

    duplicates = df[
        df["id"].duplicated(keep=False)
    ]

    raise ValueError(
        "Duplicate IAM line IDs found:\n"
        f"{duplicates['id'].tolist()[:10]}"
    )


# --------------------------------------------------
# Save manifest
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print()
print("IAM Manifest Summary")
print("--------------------")

print(
    "Annotations:",
    total_annotations
)

print(
    "Status OK:",
    ok_annotations
)

print(
    "Bad segmentation:",
    bad_segmentations
)

print(
    "Missing images:",
    missing_images
)

print(
    "Manifest samples:",
    len(df)
)

print()
print(
    "Saved:",
    OUTPUT_FILE
)