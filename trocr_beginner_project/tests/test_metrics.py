from src.metrics import (
    calculate_cer,
    calculate_wer,
    exact_field_accuracy,
)

examples = [
    ("hello world", "hello world"),
    ("hello world", "hallo world"),
    ("John Smith", "John Smith"),
    ("John Smith", "John Smit"),
    ("Arizona State University", "Arizona University"),
    ("123456", "123456"),
    ("123456", "123356"),
]

for reference, prediction in examples:
    print("-" * 50)
    print("Reference :", reference)
    print("Prediction:", prediction)
    print(f"CER   : {calculate_cer(reference, prediction):.4f}")
    print(f"WER   : {calculate_wer(reference, prediction):.4f}")
    print(f"Exact : {exact_field_accuracy(reference, prediction)}")