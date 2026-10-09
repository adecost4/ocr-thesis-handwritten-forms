from pathlib import Path
import pandas as pd


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

IAM_DIR = PROJECT_ROOT / "data" / "iam"

MANIFEST_PATH = IAM_DIR / "iam_sample.csv"

SPLIT_DIR = IAM_DIR / "splits"


# --------------------------------------------------
# Split files
# --------------------------------------------------

TRAIN_FILE = SPLIT_DIR / "trainset.txt"

VAL1_FILE = SPLIT_DIR / "validationset1.txt"

VAL2_FILE = SPLIT_DIR / "validationset2.txt"

TEST_FILE = SPLIT_DIR / "testset.txt"


# --------------------------------------------------
# Verify files exist
# --------------------------------------------------

required_files = [
    MANIFEST_PATH,
    TRAIN_FILE,
    VAL1_FILE,
    VAL2_FILE,
    TEST_FILE,
]

for file_path in required_files:

    if not file_path.exists():

        raise FileNotFoundError(
            f"Missing required file:\n{file_path}"
        )


# --------------------------------------------------
# Load IAM manifest
# --------------------------------------------------

df = pd.read_csv(MANIFEST_PATH)

print("IAM manifest samples:", len(df))


# --------------------------------------------------
# Read split IDs
# --------------------------------------------------

def read_split_ids(path):

    ids = []

    with open(path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            ids.append(line)

    return ids


train_ids = read_split_ids(TRAIN_FILE)

val1_ids = read_split_ids(VAL1_FILE)

val2_ids = read_split_ids(VAL2_FILE)

test_ids = read_split_ids(TEST_FILE)


print()
print("Split definition sizes")
print("----------------------")

print("Train:", len(train_ids))
print("Validation 1:", len(val1_ids))
print("Validation 2:", len(val2_ids))
print("Test:", len(test_ids))

# --------------------------------------------------
# Build validation split
# --------------------------------------------------

validation_ids = val1_ids + val2_ids


# --------------------------------------------------
# Filter manifest
# --------------------------------------------------

train_df = df[df["id"].isin(train_ids)].copy()

validation_df = df[
    df["id"].isin(validation_ids)
].copy()

test_df = df[df["id"].isin(test_ids)].copy()


# --------------------------------------------------
# Check for overlap
# --------------------------------------------------

train_set = set(train_df["id"])

validation_set = set(validation_df["id"])

test_set = set(test_df["id"])


assert train_set.isdisjoint(validation_set), \
    "Train and validation overlap!"

assert train_set.isdisjoint(test_set), \
    "Train and test overlap!"

assert validation_set.isdisjoint(test_set), \
    "Validation and test overlap!"


# --------------------------------------------------
# Check missing IDs
# --------------------------------------------------

manifest_ids = set(df["id"])


def report_missing(name, expected_ids):

    missing = set(expected_ids) - manifest_ids

    print(
        f"{name}: "
        f"{len(expected_ids)} expected, "
        f"{len(expected_ids) - len(missing)} found, "
        f"{len(missing)} missing"
    )

    if missing:

        print(
            "Example missing IDs:",
            list(sorted(missing))[:5]
        )


print()
print("Manifest coverage")
print("-----------------")

report_missing(
    "Train",
    train_ids
)

report_missing(
    "Validation",
    validation_ids
)

report_missing(
    "Test",
    test_ids
)

# --------------------------------------------------
# Diagnose missing split IDs
# --------------------------------------------------

# Read status for every IAM line from lines.txt
LINES_FILE = IAM_DIR / "ascii" / "lines.txt"

status_by_id = {}

with open(LINES_FILE, "r", encoding="utf-8") as f:
    for raw_line in f:
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split(maxsplit=2)

        if len(parts) >= 2:
            line_id = parts[0]
            status = parts[1]
            status_by_id[line_id] = status


manifest_ids = set(df["id"].astype(str))


def diagnose_missing(name, expected_ids):

    missing = set(expected_ids) - manifest_ids

    missing_err = []
    missing_ok = []
    missing_unknown = []

    for line_id in missing:

        status = status_by_id.get(line_id)

        if status == "err":
            missing_err.append(line_id)

        elif status == "ok":
            missing_ok.append(line_id)

        else:
            missing_unknown.append(line_id)

    print()
    print(f"{name} missing-ID diagnosis")
    print("-" * 35)

    print("Expected:", len(expected_ids))
    print("Found:", len(set(expected_ids) & manifest_ids))
    print("Missing:", len(missing))

    print("Missing because status=err:", len(missing_err))
    print("Missing despite status=ok:", len(missing_ok))
    print("Missing/unknown annotation:", len(missing_unknown))

    if missing_ok:
        print(
            "WARNING - unexplained OK IDs:",
            sorted(missing_ok)[:10]
        )

    if missing_unknown:
        print(
            "WARNING - unknown IDs:",
            sorted(missing_unknown)[:10]
        )


diagnose_missing("Train", train_ids)
diagnose_missing("Validation", validation_ids)
diagnose_missing("Test", test_ids)


# --------------------------------------------------
# Save CSV files
# --------------------------------------------------

train_output = IAM_DIR / "train.csv"

validation_output = IAM_DIR / "validation.csv"

test_output = IAM_DIR / "test.csv"


train_df.to_csv(
    train_output,
    index=False
)

validation_df.to_csv(
    validation_output,
    index=False
)

test_df.to_csv(
    test_output,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print()
print("Generated IAM splits")
print("--------------------")

print(
    "Train:",
    len(train_df)
)

print(
    "Validation:",
    len(validation_df)
)

print(
    "Test:",
    len(test_df)
)

print()

print("Saved:")
print(train_output)
print(validation_output)
print(test_output)

# --------------------------------------------------
# Verify writer/form-level separation
# --------------------------------------------------

# IAM line IDs begin with the form identifier.
# Example:
# a01-000u-00 -> form a01-000u

def get_form_id(line_id):
    return line_id.rsplit("-", 1)[0]


train_forms = set(
    train_df["id"].map(get_form_id)
)

validation_forms = set(
    validation_df["id"].map(get_form_id)
)

test_forms = set(
    test_df["id"].map(get_form_id)
)


assert train_forms.isdisjoint(validation_forms), \
    "Train and validation forms overlap!"

assert train_forms.isdisjoint(test_forms), \
    "Train and test forms overlap!"

assert validation_forms.isdisjoint(test_forms), \
    "Validation and test forms overlap!"


print()
print("Form-level leakage check")
print("------------------------")
print("Train vs Validation: PASS")
print("Train vs Test:       PASS")
print("Validation vs Test:  PASS")