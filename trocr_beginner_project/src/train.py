
from __future__ import annotations

import torch
from torch.utils.data import DataLoader
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


def make_collate_fn(processor, max_target_length: int = 128):
    def collate_fn(batch):
        images = [x["image"] for x in batch]
        texts = [x["text"] for x in batch]
        pixel_values = processor(images=images, return_tensors="pt").pixel_values
        labels = processor.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_target_length,
            return_tensors="pt",
        ).input_ids
        labels[labels == processor.tokenizer.pad_token_id] = -100
        return {"pixel_values": pixel_values, "labels": labels}
    return collate_fn


def load_model(model_name: str = "microsoft/trocr-base-handwritten"):
    processor = TrOCRProcessor.from_pretrained(model_name)
    model = VisionEncoderDecoderModel.from_pretrained(model_name)
    model.config.decoder_start_token_id = processor.tokenizer.bos_token_id
    model.config.eos_token_id = processor.tokenizer.eos_token_id
    model.config.pad_token_id = processor.tokenizer.pad_token_id
    model.config.vocab_size = model.config.decoder.vocab_size
    return processor, model
