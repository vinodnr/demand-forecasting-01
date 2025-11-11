# backend/tests/test_llm_sanitizer.py
from backend.src.llm.sanitizer import sanitize_prompt
def test_sanitize_email_and_ssn():
    s = 'Contact me at alice@example.com or SSN 123-45-6789'
    out = sanitize_prompt(s)
    assert 'alice@example.com' not in out
    assert '123-45-6789' not in out
