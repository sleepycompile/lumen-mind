# Legacy: Qwen 2.5-7B Fine-Tuning

> Deprecated. Retained for reference only.

This was Lumen's original processing layer before migrating to Claude Opus.

## What this was

LoRA fine-tuning on `Qwen/Qwen2.5-7B` with 8-bit quantization to bake Lumen's personality into model weights. The approach worked but had fundamental limitations:

- **1K token context** made personality drift impossible across longer conversations
- **Retraining loop** for every personality iteration (generate dataset, fine-tune, evaluate, repeat)
- **GPU requirement** for both training and inference

## Files

| File | Purpose |
|------|---------|
| `train.py` | LoRA fine-tuning with HuggingFace Trainer + Accelerate |
| `prepare_dataset.py` | Generates personality chat pairs from core description |
| `utils.py` | Perplexity metric for evaluating trained model |

## Dependencies (not in current requirements.txt)

```
torch>=2.0.0
transformers>=4.35.0
peft>=0.5.0
accelerate>=0.23.0
datasets>=2.15.0
bitsandbytes>=0.41.0
```

## Why we moved on

See the main [README](../../README.md#software-stack) for the full rationale.
