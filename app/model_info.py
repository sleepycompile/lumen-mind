from typing import Dict, Any
from .settings import settings

_cached: Dict[str, Any] | None = None

def get_model_info() -> Dict[str, Any]:
    global _cached
    if _cached is not None:
        return _cached
    _cached = {
        "provider": "DeepSeek AI",
        "model": settings.deepseek_model,
        "base_url": settings.deepseek_base_url,
        "max_tokens": settings.max_new_tokens,
        "temperature": settings.temperature,
        "top_p": settings.top_p,
    }
    return _cached
