# backend/src/llm/sanitizer.py
import re
PII_PATTERNS = [r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}', r'\\b\\d{3}[-.]?\\d{2}[-.]?\\d{4}\\b']

def sanitize_prompt(text: str) -> str:
    out = text
    for p in PII_PATTERNS:
        out = re.sub(p, '[REDACTED]', out)
    return out
