"""
StockMind AI Multilingual Translator Engine:
Enables dynamic translation of analytical responses into any language requested by the user:
- Indian Regional: Telugu (te), Kannada (kn), Malayalam (ml), Bengali (bn), Gujarati (gu), Marathi (mr), Punjabi (pa), Urdu (ur)
- Global Languages: Spanish (es), French (fr), German (de), Arabic (ar), Russian (ru), Japanese (ja), Chinese (zh), Portuguese (pt), Italian (it)
Includes local in-memory caching and offline phrase fallback.
"""

import re
import urllib.request
import urllib.parse
import json
from typing import Dict, Any, Optional
from utils.helpers import cache

# Offline phrase mappings for common stock market terms across major languages
OFFLINE_PHRASE_DICT = {
    "te": {
        "Current Price": "ప్రస్తుత ధర",
        "Technical Trend": "సాంకేతిక ధోరణి",
        "Support": "మద్దతు స్థాయి (Support)",
        "Resistance": "నిరోధక స్థాయి (Resistance)",
        "Exchange Rate": "వినిమయ రేటు (Exchange Rate)",
        "Indian Rupees": "భారతీయ రూపాయలు (INR)",
        "Bullish": "బుల్లిష్ (ఎదుగుదల)",
        "Bearish": "బేరిష్ (తగ్గుదల)",
        "Overview": "సమీక్ష",
        "Disclaimer": "గమనిక: ఇది విద్యా ప్రయోజనాల కోసం మాత్రమే."
    },
    "kn": {
        "Current Price": "ಪ್ರಸ್ತುತ ಬೆಲೆ",
        "Technical Trend": "ತಾಂತ್ರಿಕ ಪ್ರವೃತ್ತಿ",
        "Support": "ಬೆಂಬಲ ಮಟ್ಟ (Support)",
        "Resistance": "ಪ್ರತಿರೋಧ ಮಟ್ಟ (Resistance)",
        "Exchange Rate": "ವಿನಿಮಯ ದರ",
        "Indian Rupees": "ಭಾರತೀಯ ರೂಪಾಯಿಗಳು (INR)",
        "Bullish": "ಬುಲ್ಲಿಶ್ (ಏರಿಕೆ)",
        "Bearish": "ಬೇರಿಶ್ (ಇಳಿಕೆ)",
        "Overview": "ಅವಲೋಕನ",
        "Disclaimer": "ಸೂಚನೆ: ಇದು ಕೇವಲ ಶೈಕ್ಷಣಿಕ ಮಾಹಿತಿಯಾಗಿದೆ."
    },
    "ml": {
        "Current Price": "നിലവിലെ വില",
        "Technical Trend": "സാങ്കേതിക പ്രവണത",
        "Support": "പിന്തുണ നില (Support)",
        "Resistance": "പ്രതിരോധ നില (Resistance)",
        "Exchange Rate": "വിനിമയ നിരക്ക്",
        "Indian Rupees": "ഇന്ത്യൻ രൂപ (INR)",
        "Bullish": "ബുള്ളിഷ് (കയറ്റം)",
        "Bearish": "ബെയറിഷ് (ഇറക്കം)",
        "Overview": "അവലോകനം",
        "Disclaimer": "ശ്രദ്ധിക്കുക: ഇത് വിദ്യാഭ്യാസ ആവശ്യങ്ങൾക്ക് മാത്രമുള്ളതാണ്."
    },
    "bn": {
        "Current Price": "বর্তমান মূল্য",
        "Technical Trend": "প্রযুক্তিগত প্রবণতা",
        "Support": "সমর্থন স্তর (Support)",
        "Resistance": "প্রতিরোধ স্তর (Resistance)",
        "Exchange Rate": "বিনিময় হার",
        "Indian Rupees": "ভারতীয় রুপি (INR)",
        "Bullish": "বুলিশ (ঊর্ধ্বমুখী)",
        "Bearish": "বেয়ারিশ (নিম্নমুখী)",
        "Overview": "সংক্ষিপ্ত বিবরণ",
        "Disclaimer": "দাবিত্যাগ: এটি কেবল শিক্ষামূলক উদ্দেশ্যে।"
    },
    "es": {
        "Current Price": "Precio Actual",
        "Technical Trend": "Tendencia Técnica",
        "Support": "Nivel de Soporte",
        "Resistance": "Nivel de Resistencia",
        "Exchange Rate": "Tipo de Cambio",
        "Indian Rupees": "Rupias Indias (INR)",
        "Bullish": "Alcista (Bullish)",
        "Bearish": "Bajista (Bearish)",
        "Overview": "Resumen",
        "Disclaimer": "Aviso: Solo para fines educativos."
    },
    "fr": {
        "Current Price": "Prix Actuel",
        "Technical Trend": "Tendance Technique",
        "Support": "Niveau de Support",
        "Resistance": "Niveau de Résistance",
        "Exchange Rate": "Taux de Change",
        "Indian Rupees": "Roupies Indiennes (INR)",
        "Bullish": "Haussier (Bullish)",
        "Bearish": "Baissier (Bearish)",
        "Overview": "Aperçu",
        "Disclaimer": "Avertissement: À des fins éducatives uniquement."
    },
    "de": {
        "Current Price": "Aktueller Kurs",
        "Technical Trend": "Technischer Trend",
        "Support": "Unterstützungsniveau",
        "Resistance": "Widerstandsniveau",
        "Exchange Rate": "Wechselkurs",
        "Indian Rupees": "Indische Rupien (INR)",
        "Bullish": "Bullisch (Steigend)",
        "Bearish": "Bärisch (Fallend)",
        "Overview": "Überblick",
        "Disclaimer": "Hinweis: Nur zu Bildungszwecken."
    },
    "ar": {
        "Current Price": "السعر الحالي",
        "Technical Trend": "الاتجاه الفني",
        "Support": "مستوى الدعم",
        "Resistance": "مستوى المقاومة",
        "Exchange Rate": "سعر الصرف",
        "Indian Rupees": "الروبية الهندية (INR)",
        "Bullish": "صعودي (Bullish)",
        "Bearish": "هبوطي (Bearish)",
        "Overview": "نظرة عامة",
        "Disclaimer": "تنويه: لأغراض تعليمية فقط."
    },
    "ru": {
        "Current Price": "Текущая цена",
        "Technical Trend": "Технический тренд",
        "Support": "Уровень поддержки",
        "Resistance": "Уровень сопротивления",
        "Exchange Rate": "Курс обмена",
        "Indian Rupees": "Индийские рупии (INR)",
        "Bullish": "Бычий (Растущий)",
        "Bearish": "Медвежий (Падающий)",
        "Overview": "Обзор",
        "Disclaimer": "Отказ от ответственности: Только в образовательных целях."
    },
    "ja": {
        "Current Price": "現在の価格",
        "Technical Trend": "テクニカルトレンド",
        "Support": "サポート水準",
        "Resistance": "レジスタンス水準",
        "Exchange Rate": "為替レート",
        "Indian Rupees": "インドルピー (INR)",
        "Bullish": "強気 (Bullish)",
        "Bearish": "弱気 (Bearish)",
        "Overview": "概要",
        "Disclaimer": "免責事項：教育目的のみに使用されます。"
    },
    "zh": {
        "Current Price": "当前价格",
        "Technical Trend": "技术趋势",
        "Support": "支撑位",
        "Resistance": "阻力位",
        "Exchange Rate": "汇率",
        "Indian Rupees": "印度卢比 (INR)",
        "Bullish": "看涨 (Bullish)",
        "Bearish": "看跌 (Bearish)",
        "Overview": "概况",
        "Disclaimer": "免责声明：仅供学习参考。"
    }
}


def translate_text_online(text: str, target_lang: str) -> Optional[str]:
    """
    Translate text using the robust Google Translate single-shot service with timeout.
    Preserves markdown and symbols.
    """
    if not text.strip():
        return text

    # Handle language codes
    clean_target = target_lang.lower().strip()
    if clean_target in ["en", "english"]:
        return text

    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={clean_target}&dt=t&q={urllib.parse.quote(text)}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        with urllib.request.urlopen(req, timeout=3.0) as response:
            if response.status == 200:
                raw = response.read().decode("utf-8")
                data = json.loads(raw)
                if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                    translated_segments = [seg[0] for seg in data[0] if seg and len(seg) > 0 and seg[0]]
                    if translated_segments:
                        return "".join(translated_segments)
    except Exception:
        pass
    return None


def translate_to_language(text: str, target_lang: str) -> str:
    """
    Translates text into the requested language with caching and graceful offline fallback.
    If target_lang is English, Tamil, Tanglish, Hindi, or Hinglish and the text is already
    in that language, returns text directly.
    """
    target = target_lang.lower().strip()
    if target in ["en", "english", "default", "none"] or not target:
        return text

    # Cache key for fast repeat lookup
    text_hash = hash(text[:200] + str(len(text)) + target)
    cache_key = f"trans_{target}_{text_hash}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    # 1. Attempt online translation
    translated = translate_text_online(text, target)
    if translated and len(translated) > 10:
        cache.set(cache_key, translated, ttl=3600)
        return translated

    # 2. Offline fallback: apply localized phrase replacements if available
    phrase_map = OFFLINE_PHRASE_DICT.get(target)
    if phrase_map:
        fallback_text = text
        for eng_phrase, local_phrase in phrase_map.items():
            pattern = re.compile(re.escape(eng_phrase), re.IGNORECASE)
            fallback_text = pattern.sub(local_phrase, fallback_text)
        return fallback_text

    return text
