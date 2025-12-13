import logging
from typing import List, Optional, Dict

from openai import OpenAI

from .settings import settings
from .personalities import default_persona_system

logger = logging.getLogger("bloomed-terminal.inference")
logging.basicConfig(level=logging.INFO)

_CLIENT = None

def load_model(model_dir: Optional[str] = None) -> None:
    """
    Initialize the DeepSeek API client.
    """
    global _CLIENT
    if _CLIENT is not None:
        return

    if not settings.deepseek_api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY environment variable is required. "
            "Please set it in your .env file or environment."
        )

    logger.info("Initializing DeepSeek API client...")
    _CLIENT = OpenAI(
        api_key=settings.deepseek_api_key,
        base_url=settings.deepseek_base_url,
    )
    logger.info(f"DeepSeek client initialized with model: {settings.deepseek_model}")

def _ensure_persona_system(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    If no system prompt is present, inject Bloomed Terminal's house-voice system.
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
    Core text generation using DeepSeek API: returns assistant content as a string.
    """
    global _CLIENT
    if _CLIENT is None:
        load_model()

    messages = _ensure_persona_system(messages)

    max_tokens = int(max_new_tokens or settings.max_new_tokens)
    temp = float(temperature if temperature is not None else settings.temperature)
    top_p_val = float(top_p if top_p is not None else settings.top_p)

    try:
        response = _CLIENT.chat.completions.create(
            model=settings.deepseek_model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temp,
            top_p=top_p_val,
            stop=stop,
        )

        content = response.choices[0].message.content
        return content.strip() if content else ""

    except Exception as e:
        logger.error(f"DeepSeek API error: {e}")
        raise
