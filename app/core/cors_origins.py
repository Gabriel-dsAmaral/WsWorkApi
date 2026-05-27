import json
import os
import re
from urllib.parse import urlparse

DEFAULT_DEV_ORIGIN = "http://localhost:5173"

_VERCEL_ORIGIN_REGEX = r"^https://[\w-]+(-[\w-]+)*\.vercel\.app$"


def is_debug_env() -> bool:
    return os.getenv("DEBUG", "false").strip().lower() in ("true", "1", "yes")


def normalize_origin(origin: str) -> str:
    """Normaliza e valida uma origin CORS (scheme + host, sem path)."""
    value = origin.strip().rstrip("/")
    if not value:
        raise ValueError("CORS origin vazia.")

    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"CORS origin com scheme inválido: {origin!r}")
    if not parsed.netloc:
        raise ValueError(f"CORS origin inválida: {origin!r}")
    if parsed.username or parsed.password:
        raise ValueError(f"CORS origin não pode conter credenciais: {origin!r}")

    return f"{parsed.scheme}://{parsed.netloc}"


def parse_cors_origins(raw: str | None) -> list[str]:
    """
    - http://localhost:5173,https://app.vercel.app
    - [http://localhost:5173,https://app.vercel.app]
    - ["http://localhost:5173","https://app.vercel.app"]
    """
    if raw is None or not raw.strip():
        return []

    text = raw.strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1].strip()

    if text.startswith("["):
        try:
            data = json.loads(text)
            if isinstance(data, list):
                return _dedupe([normalize_origin(str(item)) for item in data if item])
        except json.JSONDecodeError:
            pass

    if text.startswith('"') or (text.startswith("'") and "," not in text):
        try:
            data = json.loads(text if text.startswith("[") else f"[{text}]")
            if isinstance(data, list):
                return _dedupe([normalize_origin(str(item)) for item in data if item])
        except json.JSONDecodeError:
            pass

    origins: list[str] = []
    for part in text.split(","):
        item = part.strip().strip('"').strip("'")
        if item:
            origins.append(normalize_origin(item))
    return _dedupe(origins)


def _dedupe(origins: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for origin in origins:
        if origin not in seen:
            seen.add(origin)
            result.append(origin)
    return result


def get_cors_origins_from_env() -> list[str]:
    explicit = parse_cors_origins(os.getenv("BACKEND_CORS_ORIGINS"))
    if explicit:
        return explicit
    if is_debug_env():
        return [DEFAULT_DEV_ORIGIN]
    return []


def get_cors_origin_regex_from_env() -> str | None:
    raw = os.getenv("BACKEND_CORS_ORIGIN_REGEX")
    if raw is not None:
        value = raw.strip()
        if not value:
            return None
        re.compile(value)
        return value

    if is_debug_env():
        return None

    # Produção sem regex explícita: previews/deploys *.vercel.app
    return _VERCEL_ORIGIN_REGEX


def get_cors_allow_credentials_from_env() -> bool:
    raw = os.getenv("BACKEND_CORS_ALLOW_CREDENTIALS", "true").strip().lower()
    return raw in ("true", "1", "yes")
