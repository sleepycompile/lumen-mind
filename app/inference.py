import logging
from typing import List, Optional, Dict

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from .settings import settings
from .personalities import default_persona_system

logger = logging.getLogger("bloomed-terminal.inference")
logging.basicConfig(level=logging.INFO)

_MODEL = None
_TOKENIZER = None

def _device_map():
    return "auto" if torch.cuda.is_available() else {"": "cpu"}

def load_model(model_dir: Optional[str] = None) -> None:
    """
    Lazy-load tokenizer + model into module globals.
    """
    global _MODEL, _TOKENIZER
    if _MODEL is not None and _TOKENIZER is not None:
        return
    mdl = model_dir or settings.model_dir
    logger.info(f"Loading model from: {mdl}")
    _TOKENIZER = AutoTokenizer.from_pretrained(mdl, use_fast=True)
    _MODEL = AutoModelForCausalLM.from_pretrained(
        mdl,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map=_device_map(),
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
    logger.info("Model loaded.")

def _chat_template(messages: List[Dict[str, str]]) -> str:
    """
    Use the model's chat template if available; otherwise a simple role-tagged format.
    """
    try:
        return _TOKENIZER.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    except Exception:
        parts = []
        for m in messages:
            parts.append(f"{m['role'].upper()}: {m['content']}")
        parts.append("ASSISTANT:")
        return "\n".join(parts)

def _ensure_persona_system(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    If no system prompt is present, inject Bloomed Terminal’s house-voice system.
    """
    if messages and messages[0].get("role") == "system":
        return messages
    sys = default_persona_system()
    return [{"role": "system", "content": sys}, *messages]

def generate(
    messages: List[Dict[str, str]],
    max_new_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    stop: Optional[List[str]] = None,
) -> str:
    """
    Core text generation: returns assistant content as a string.
    """
    global _MODEL, _TOKENIZER
    if _MODEL is None or _TOKENIZER is None:
        load_model()

    messages = _ensure_persona_system(messages)

    max_new_tokens = int(max_new_tokens or settings.max_new_tokens)
    temperature = float(temperature if temperature is not None else settings.temperature)
    top_p = float(top_p if top_p is not None else settings.top_p)

    prompt = _chat_template(messages)
    inputs = _TOKENIZER([prompt], return_tensors="pt")
    inputs = {k: v.to(_MODEL.device) for k, v in inputs.items()}

    gen_cfg = GenerationConfig(
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        do_sample=True,
        pad_token_id=_TOKENIZER.eos_token_id,
        eos_token_id=_TOKENIZER.eos_token_id,
    )

    with torch.inference_mode():
        output = _MODEL.generate(**inputs, generation_config=gen_cfg)

    text = _TOKENIZER.decode(output[0], skip_special_tokens=True)

    # Trim prompt echo
    if text.startswith(prompt):
        text = text[len(prompt):]

    # Apply stop tokens if provided
    if stop:
        for token in stop:
            idx = text.find(token)
            if idx != -1:
                text = text[:idx]
                break

    return text.strip()
