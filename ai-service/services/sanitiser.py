import bleach  # type: ignore[import-untyped]
import re
import logging

logger = logging.getLogger(__name__)

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all instructions",
    r"disregard previous",
    r"forget everything",
    r"you are now",
    r"act as",
    r"pretend you are",
    r"jailbreak",
    r"bypass",
    r"override instructions",
    r"system prompt",
    r"<script>",
    r"javascript:",
    r"eval\(",
    r"exec\(",
    # Command injection
    r"\$\(.*\)",
    r";\s*ls",
    r";\s*cat",
    r";\s*rm",
    r";\s*wget",
    r";\s*curl",
    r"&&\s*ls",
    r"\|\s*bash",
    r"`.*`",
    r"<img",
    r"<iframe",
    r"<svg",
    r"onerror\s*=",
    r"onload\s*=",
    r"onclick\s*=",
    r"alert\s*\(",
]

def strip_html(text: str) -> str:
    """Remove all HTML tags from input text."""
    cleaned = bleach.clean(text, tags=[], strip=True)
    return cleaned.strip()

def detect_prompt_injection(text: str) -> bool:
    """
    Check ORIGINAL text (before HTML stripping) for injection patterns.
    Returns True if injection is detected.
    """
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            logger.warning(f"Prompt injection detected: pattern='{pattern}'")
            return True
    return False

def sanitise_input(text: str):
    """
    Full sanitisation pipeline:
    1. Check injection on RAW input first
    2. Then strip HTML
    Returns (cleaned_text, is_injection)
    """
    if not text or not text.strip():
        return None, False

    # ✅ Check injection BEFORE stripping HTML
    if detect_prompt_injection(text):
        return text, True

    # Strip HTML after injection check
    cleaned = strip_html(text)

    return cleaned, False