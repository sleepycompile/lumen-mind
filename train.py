"""
train.py — Legacy training script

This script was used for LoRA fine-tuning on Qwen/Qwen2.5-7B.
With the migration to Claude Opus as the processing layer, local
fine-tuning is no longer the primary approach.

LUMEN's personality is now shaped through:
  1. System prompt engineering (config.py SYSTEM_PROMPT)
  2. Conversation context (200K token window)
  3. Personality dataset as few-shot examples (data/lumen_personality.json)

To use personality data as context for Opus, see inference.py.
For the original Qwen fine-tuning workflow, check the legacy/ branch.
"""

print("Training has been replaced by Opus API inference.")
print("LUMEN's personality is now injected via system prompts and context.")
print("See inference.py for the current approach.")
print("For legacy Qwen fine-tuning, check the legacy/ branch.")
