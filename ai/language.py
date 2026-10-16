"""
Language Detection Engine:
Detects English, Tamil (Script), Tanglish (Tamil in Latin script), Hindi, Hinglish,
regional Indian languages (Telugu, Kannada, Malayalam, Bengali, Gujarati, Punjabi),
and global international languages (Spanish, French, German, Arabic, Russian, Japanese, Chinese, etc.).
Ensures replies are delivered in the user's preferred conversational style and language.
"""

import re
import urllib.request
import urllib.parse
import json
from typing import Dict, Any, Optional
from utils.helpers import cache

# Common Tanglish conversational keywords & suffixes
TANGLISH_KEYWORDS = {
    "ippo", "epdi", "iruku", "irukku", "mela", "keela", "poguma", "pogum", "vaangalaama",
    "vangalama", "vaanga", "vanga", "enna", "aachu", "aayiduchi", "yen", "panna", "parkalaam",
    "paakalaam", "romba", "nalla", "kudunga", "thanga", "theriyuma", "solunga", "solra",
    "sollu", "konjam", "paathu", "mudiyuma", "illa", "illai", "padu", "iruntha", "irundha", "aana",
    "aanal", "valarum", "eri", "irangi", "eruma", "down aachu", "down aaguthu", "down aaga",
    "reason enna", "innikku", "innaikku", "naalaikku", "epadi", "irukudhu", "nalladha",
    "adhigam", "adhigama", "adhigamaa", "panradha", "pannalama", "edukalama", "vaangalama",
    "risk ah", "down ah", "up ah", "chance epdi", "situation", "paravala", "mattum"
}

# Common Hinglish conversational keywords
HINGLISH_KEYWORDS = {
    "kaisa", "kaisi", "kaise", "hai", "hain", "kya", "hoga", "hogi", "gir", "gaya", "gayi",
    "badhega", "badhegi", "kharide", "kharidna", "kharidun", "beche", "bechna", "bechun",
    "aaj", "kal", "batao", "bataiye", "kyun", "kyu", "chal", "raha", "rahi", "lag", "raha",
    "upar", "niche", "chahiye", "thoda", "bahut", "accha", "bura", "girega", "samjhao", "bhai"
}

# European vocabulary markers
SPANISH_KEYWORDS = {"hola", "¿", "cómo", "precio", "acciones", "mercado", "comprar", "vender", "análisis", "cuál", "gracias"}
FRENCH_KEYWORDS = {"bonjour", "comment", "prix", "actions", "marché", "acheter", "vendre", "analyse", "merci", "pourquoi"}
GERMAN_KEYWORDS = {"hallo", "wie", "aktien", "aktie", "markt", "kurs", "kaufen", "verkaufen", "analyse", "danke"}
PORTUGUESE_KEYWORDS = {"olá", "como", "preço", "ações", "mercado", "comprar", "vender", "análise", "obrigado"}
ITALIAN_KEYWORDS = {"ciao", "come", "prezzo", "azioni", "mercato", "comprare", "vendere", "analisi", "grazie"}


def is_tamil_script(text: str) -> bool:
    """Check if text contains Tamil Unicode range (U+0B80 to U+0BFF)."""
    return len([c for c in text if '\u0B80' <= c <= '\u0BFF']) >= 2

def is_devanagari_script(text: str) -> bool:
    """Check if text contains Devanagari Hindi Unicode range (U+0900 to U+097F)."""
    return len([c for c in text if '\u0900' <= c <= '\u097F']) >= 2

def is_telugu_script(text: str) -> bool:
    """Check if text contains Telugu Unicode range (U+0C00 to U+0C7F)."""
    return len([c for c in text if '\u0C00' <= c <= '\u0C7F']) >= 2

def is_kannada_script(text: str) -> bool:
    """Check if text contains Kannada Unicode range (U+0C80 to U+0CFF)."""
    return len([c for c in text if '\u0C80' <= c <= '\u0CFF']) >= 2

def is_malayalam_script(text: str) -> bool:
    """Check if text contains Malayalam Unicode range (U+0D00 to U+0D7F)."""
    return len([c for c in text if '\u0D00' <= c <= '\u0D7F']) >= 2

def is_bengali_script(text: str) -> bool:
    """Check if text contains Bengali Unicode range (U+0980 to U+09FF)."""
    return len([c for c in text if '\u0980' <= c <= '\u09FF']) >= 2

def is_gujarati_script(text: str) -> bool:
    """Check if text contains Gujarati Unicode range (U+0A80 to U+0AFF)."""
    return len([c for c in text if '\u0A80' <= c <= '\u0AFF']) >= 2

def is_punjabi_script(text: str) -> bool:
    """Check if text contains Gurmukhi Punjabi Unicode range (U+0A00 to U+0A7F)."""
    return len([c for c in text if '\u0A00' <= c <= '\u0A7F']) >= 2

def is_arabic_script(text: str) -> bool:
    """Check if text contains Arabic/Urdu Unicode range (U+0600 to U+06FF)."""
    return len([c for c in text if '\u0600' <= c <= '\u06FF']) >= 2

def is_cyrillic_script(text: str) -> bool:
    """Check if text contains Cyrillic / Russian Unicode range (U+0400 to U+04FF)."""
    return len([c for c in text if '\u0400' <= c <= '\u04FF']) >= 2

def is_japanese_script(text: str) -> bool:
    """Check if text contains Japanese Hiragana/Katakana (U+3040 to U+30FF)."""
    return len([c for c in text if '\u3040' <= c <= '\u30FF']) >= 2

def is_chinese_script(text: str) -> bool:
    """Check if text contains Chinese CJK Ideographs (U+4E00 to U+9FFF)."""
    return len([c for c in text if '\u4E00' <= c <= '\u9FFF']) >= 2

def is_korean_script(text: str) -> bool:
    """Check if text contains Korean Hangul (U+AC00 to U+D7AF)."""
    return len([c for c in text if '\uAC00' <= c <= '\uD7AF']) >= 2


def detect_language_online(text: str) -> Optional[str]:
    """Fast online language detector fallback."""
    if len(text.strip()) < 5:
        return None
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={urllib.parse.quote(text[:120])}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                if len(data) > 2 and isinstance(data[2], str) and data[2]:
                    return data[2].lower()
    except Exception:
        pass
    return None


def detect_language(text: str) -> str:
    """
    Classify query language dynamically:
    - Supports Tamil (ta), Tanglish, Hindi (hi), Hinglish
    - Regional Indian scripts: Telugu (te), Kannada (kn), Malayalam (ml), Bengali (bn), Gujarati (gu), Punjabi (pa)
    - World scripts: Arabic (ar), Russian (ru), Japanese (ja), Chinese (zh), Korean (ko)
    - European languages: Spanish (es), French (fr), German (de), Portuguese (pt), Italian (it)
    - Defaults to 'en' (English).
    """
    cleaned = text.strip()
    if not cleaned:
        return "en"

    # Cache lookup
    cache_key = f"lang_detect_{hash(cleaned)}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    # 1. Native Script Range Matching (Deterministic & Zero Latency)
    if is_tamil_script(cleaned):
        cache.set(cache_key, "ta", ttl=3600)
        return "ta"
    if is_devanagari_script(cleaned):
        cache.set(cache_key, "hi", ttl=3600)
        return "hi"
    if is_telugu_script(cleaned):
        cache.set(cache_key, "te", ttl=3600)
        return "te"
    if is_kannada_script(cleaned):
        cache.set(cache_key, "kn", ttl=3600)
        return "kn"
    if is_malayalam_script(cleaned):
        cache.set(cache_key, "ml", ttl=3600)
        return "ml"
    if is_bengali_script(cleaned):
        cache.set(cache_key, "bn", ttl=3600)
        return "bn"
    if is_gujarati_script(cleaned):
        cache.set(cache_key, "gu", ttl=3600)
        return "gu"
    if is_punjabi_script(cleaned):
        cache.set(cache_key, "pa", ttl=3600)
        return "pa"
    if is_arabic_script(cleaned):
        cache.set(cache_key, "ar", ttl=3600)
        return "ar"
    if is_cyrillic_script(cleaned):
        cache.set(cache_key, "ru", ttl=3600)
        return "ru"
    if is_japanese_script(cleaned):
        cache.set(cache_key, "ja", ttl=3600)
        return "ja"
    if is_chinese_script(cleaned):
        cache.set(cache_key, "zh", ttl=3600)
        return "zh"
    if is_korean_script(cleaned):
        cache.set(cache_key, "ko", ttl=3600)
        return "ko"

    # Check for explicit language switches
    lower_text = cleaned.lower()
    if any(p in lower_text for p in ["in english", "explain in english", "now explain in english", "english-la sollu", "english me"]):
        cache.set(cache_key, "en", ttl=3600)
        return "en"
    if any(p in lower_text for p in ["in tamil", "tamil-la sollu", "tamil la explain", "தமிழுக்கு"]):
        cache.set(cache_key, "ta", ttl=3600)
        return "ta"
    if any(p in lower_text for p in ["in tanglish", "tanglish-la sollu", "tanglish la"]):
        cache.set(cache_key, "tanglish", ttl=3600)
        return "tanglish"
    if any(p in lower_text for p in ["in hindi", "hindi me batao", "hindi mein", "हिंदी में"]):
        cache.set(cache_key, "hi", ttl=3600)
        return "hi"
    if any(p in lower_text for p in ["in hinglish", "hinglish me batao", "hinglish mein"]):
        cache.set(cache_key, "hinglish", ttl=3600)
        return "hinglish"

    # 2. Tokenize words for Latin Script dialects & European languages
    words = re.findall(r"[a-zA-Z]+", cleaned.lower())
    word_set = set(words)

    # Tanglish check
    tanglish_matches = word_set.intersection(TANGLISH_KEYWORDS)
    if tanglish_matches or any("aaguthu" in w or "aachu" in w or "iruku" in w for w in words):
        cache.set(cache_key, "tanglish", ttl=3600)
        return "tanglish"

    for kw in TANGLISH_KEYWORDS:
        if kw in lower_text:
            cache.set(cache_key, "tanglish", ttl=3600)
            return "tanglish"

    # Hinglish check
    hinglish_matches = word_set.intersection(HINGLISH_KEYWORDS)
    if hinglish_matches:
        cache.set(cache_key, "hinglish", ttl=3600)
        return "hinglish"

    # European languages check
    if word_set.intersection(SPANISH_KEYWORDS) or "¿" in cleaned:
        cache.set(cache_key, "es", ttl=3600)
        return "es"
    if word_set.intersection(FRENCH_KEYWORDS):
        cache.set(cache_key, "fr", ttl=3600)
        return "fr"
    if word_set.intersection(GERMAN_KEYWORDS):
        cache.set(cache_key, "de", ttl=3600)
        return "de"
    if word_set.intersection(PORTUGUESE_KEYWORDS):
        cache.set(cache_key, "pt", ttl=3600)
        return "pt"
    if word_set.intersection(ITALIAN_KEYWORDS):
        cache.set(cache_key, "it", ttl=3600)
        return "it"

    # 3. Optional fast online detection for any other Latin-script language
    if len(words) >= 3 and not any(w in {"stock", "share", "today", "price", "is", "the", "for", "what", "how", "analyze", "compare"} for w in words):
        online_lang = detect_language_online(cleaned)
        if online_lang and online_lang != "en":
            cache.set(cache_key, online_lang, ttl=3600)
            return online_lang

    cache.set(cache_key, "en", ttl=3600)
    return "en"
