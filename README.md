# LUMEN.MIND

Processing layer for LUMEN, an evolving AI personality designed to be unpredictable, self-shaping, and non-conventional.

## Architecture

LUMEN runs on **Claude Opus** as its core processing layer, with personality injected through system prompts and long-context conversation history.

### Why Opus over Qwen

The original implementation used LoRA fine-tuning on Qwen/Qwen2.5-7B. We moved to Opus for several reasons:

- **Context window**: 200K tokens vs 1K. LUMEN can now hold entire conversation arcs, reference things from hours ago, and evolve across a session without forgetting. This is the big one. A personality that forgets itself every 1K tokens isn't really evolving.
- **Reasoning depth**: Opus handles the kind of lateral, contradictory thinking that LUMEN needs. Qwen 7B could mimic the surface-level chaos but couldn't sustain coherent personality drift across long interactions.
- **No retraining loop**: Personality iteration used to mean regenerating datasets, retraining LoRA adapters, and hoping the vibes transferred. Now it's a system prompt edit. Faster iteration, tighter feedback loop.
- **Cost vs hardware tradeoff**: Running Qwen 7B with 8-bit quantization still needed a decent GPU. Opus is API-based, so LUMEN can run from anything with an internet connection.

The tradeoff is that we lose parameter-level personality baking. The personality lives in the prompt now, not the weights. For LUMEN's purposes, the context window gain more than compensates.

## Setup

1. Install dependencies
   ```
   pip install -r requirements.txt
   ```

2. Set your API key
   ```
   export ANTHROPIC_API_KEY=your-key-here
   ```

3. Run inference
   ```
   python inference.py
   ```
   Type 'exit' to quit the chat session.

## Files

| File | Purpose |
|------|---------|
| `config.py` | Model config, system prompt, inference parameters |
| `model.py` | Opus client initialization and generation |
| `inference.py` | Interactive chat loop |
| `train.py` | Legacy notice (original Qwen fine-tuning) |
| `data/` | Personality dataset (usable as few-shot context) |
| `utils.py` | Utility functions |

## Legacy

The original Qwen/Qwen2.5-7B LoRA fine-tuning code is preserved in the `legacy/` branch for reference.

## License

MIT License - see LICENSE file for details.
