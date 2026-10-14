"""
Language Detection Engine:
Detects English, Tamil (Script), Tanglish (Tamil in Latin script), Hindi, and Hinglish.
Ensures replies are delivered in the user's preferred conversational style.
"""

import re
from typing import Dict, Any

# Common Tanglish conversational keywords & suffixes
TANGLISH_KEYWORDS = {
    "ippo", "epdi", "iruku", "irukku", "mela", "keela", "poguma", "pogum", "vaangalaama",
    "vangalama", "vaanga", "vanga", "enna", "aachu", "aayiduchi", "yen", "panna", "parkalaam",
    "paakalaam", "romba", "nalla", "kudunga", "thanga", "theriyuma", "solunga", "solra",
    "konjam", "paathu", "mudiyuma", "illa", "illai", "padu", "iruntha", "irundha", "aana",
    "aanal", "valarum", "eri", "irangi", "eruma", "down aachu", "down aaguthu", "down aaga",
    "reason enna", "innikku", "innaikku", "naalaikku", "epadi", "irukudhu", "nalladha"
}

# Common Hinglish conversational keywords
HINGLISH_KEYWORDS = {
    "kaisa", "kaisi", "kaise", "hai", "hain", "kya", "hoga", "hogi", "gir", "gaya", "gayi",
    "badhega", "badhegi", "kharide", "kharidna", "kharidun", "beche", "bechna", "bechun",
    "aaj", "kal", "batao", "bataiye", "kyun", "kyu", "chal", "raha", "rahi", "lag", "raha",
    "upar", "niche", "chahiye", "thoda", "bahut", "accha", "bura"
}

def is_tamil_script(text: str) -> bool:
    """Check if text contains Tamil Unicode range (U+0B80 to U+0BFF)."""
    tamil_chars = [c for c in text if '\u0B80' <= c <= '\u0BFF']
    return len(tamil_chars) >= 2

def is_devanagari_script(text: str) -> bool:
    """Check if text contains Devanagari Hindi Unicode range (U+0900 to U+097F)."""
    hindi_chars = [c for c in text if '\u0900' <= c <= '\u097F']
    return len(hindi_chars) >= 2

def detect_language(text: str) -> str:
    """
    Classify query language: 'en', 'ta', 'tanglish', 'hi', 'hinglish'.
    """
    cleaned = text.strip()
    if not cleaned:
        return "en"

    # 1. Native script detection
    if is_tamil_script(cleaned):
        return "ta"
    if is_devanagari_script(cleaned):
        return "hi"

    # 2. Tokenize words for Tanglish / Hinglish detection
    words = re.findall(r"[a-zA-Z]+", cleaned.lower())
    word_set = set(words)

    # Tanglish check
    tanglish_matches = word_set.intersection(TANGLISH_KEYWORDS)
    if tanglish_matches or any("aaguthu" in w or "aachu" in w or "iruku" in w for w in words):
        return "tanglish"

    # Check for Tanglish phrases
    lower_text = cleaned.lower()
    for kw in TANGLISH_KEYWORDS:
        if kw in lower_text:
            return "tanglish"

    # Hinglish check
    hinglish_matches = word_set.intersection(HINGLISH_KEYWORDS)
    if hinglish_matches:
        return "hinglish"

    return "en"
