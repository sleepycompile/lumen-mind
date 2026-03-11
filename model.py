"""
model.py — LUMEN processing layer

Current: Claude Opus via Anthropic API
Previous: Qwen/Qwen2.5-7B with LoRA fine-tuning (see legacy/ branch)

The shift from local fine-tuning to Opus means LUMEN's personality is now
injected through system prompts and conversation context rather than weight
modifications. The tradeoff: we lose parameter-level personality baking but
gain 200K context, stronger reasoning, and the ability to evolve personality
across longer conversations without retraining.
"""

import anthropic
from config import Config


def load_model():
    """Initialize the Anthropic client for Opus inference."""
    client = anthropic.Anthropic(api_key=Config.API_KEY)
    return client


def generate(client, prompt, conversation_history=None):
    """Generate a response from LUMEN.
    
    Args:
        client: Anthropic client instance
        prompt: User input string
        conversation_history: Optional list of prior message dicts
    
    Returns:
        Generated response string
    """
    messages = conversation_history or []
    messages.append({"role": "user", "content": prompt})
    
    response = client.messages.create(
        model=Config.MODEL_NAME,
        max_tokens=Config.MAX_TOKENS,
        temperature=Config.TEMPERATURE,
        top_p=Config.TOP_P,
        system=Config.SYSTEM_PROMPT,
        messages=messages
    )
    
    return response.content[0].text
