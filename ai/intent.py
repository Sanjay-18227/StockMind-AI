"""
Intent Classifier & Entity Extractor:
Parses user queries across English, Tamil, Tanglish, and Hindi into structured intents,
extracting primary and secondary symbols, comparison pairs, and requested timeframes.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from data.market_data import resolve_ticker, COMMON_ALIASES

INTENTS = [
    "MARKET_OVERVIEW",
    "STOCK_COMPARISON",
    "WHY_EXPLANATION",
    "WHY_MOVE",
    "RISK_QUERY",
    "DEEP_TECHNICAL",
    "HOW_IT_WORKS",
    "SUPPORT_RESISTANCE",
    "PREDICTION_QUERY",
    "STOCK_DIRECTION",
    "BUY_SELL_QUERY",
    "TIMEFRAME_HISTORY",
    "STOCK_TIPS",
    "CURRENCY_CONVERSION",
    "LANGUAGE_SWITCH",
    "STOCK_ANALYSIS_SIMPLE",
    "STOCK_ANALYSIS_DETAILED",
    "STOCK_ANALYSIS",
    "GENERAL_GREETING",
    "GENERAL_HOW_ARE_YOU",
    "GENERAL_CAPABILITIES",
    "GENERAL_OFF_TOPIC",
    "GENERAL_CONVERSATION"
]

TIMEFRAME_PATTERNS = {
    "1d": ["1d", "1 day", "today", "intraday", "இன்னைக்கு", "innaikku", "aaj"],
    "5d": ["5d", "5 days", "1 week", "one week", "వారం", "vaaram", "hafte"],
    "1mo": ["1m", "1mo", "1 month", "மாதம்", "maasam", "mahina"],
    "3mo": ["3m", "3mo", "3 months", "quarter"],
    "6mo": ["6m", "6mo", "6 months", "half year"],
    "1y": ["1y", "1 year", "12 months", "வருடம்", "varudam", "saal"],
    "5y": ["5y", "5 years", "last 5 years", "5 வருடம்", "5 saal"],
    "max": ["max", "all time", "maximum", "complete history"]
}

def extract_timeframe(text: str) -> Optional[str]:
    """Extract timeframe from query if explicitly mentioned."""
    lower = text.lower()
    for tf, keywords in TIMEFRAME_PATTERNS.items():
        for kw in keywords:
            if kw in lower:
                return tf
    return None

STOPWORDS = {
    "THE", "AND", "FOR", "WHY", "HOW", "WHAT", "WHEN", "CAN", "YOU", "ARE",
    "THIS", "STOCK", "SHARE", "PRICE", "TODAY", "TELL", "GIVE", "SHOW",
    "ANALYSIS", "ANALYZE", "COMPARE", "VERSUS", "PREDICT", "PREDICTION",
    "BUY", "SELL", "HOLD", "DOWN", "FALL", "DROP", "GOOD", "BEST", "LOOK",
    "TIP", "TIPS", "RULE", "RULES", "ADVICE", "NOW", "IT", "THAT", "ABOUT",
    "WITH", "IN", "ON", "AT", "OF", "ME", "WE", "BRO", "SIR", "YES", "NO",
    "JUST", "EXPLAIN", "DETAIL", "DETAILS", "FULL", "SIMPLE", "WORKING", "WORK",
    "RISK", "LEVEL", "LEVELS", "SUPPORT", "RESISTANCE", "TARGET", "FORECAST",
    "LONG", "TERM", "SHORT", "TOMORROW", "YESTERDAY", "CHANCE", "SITUATION",
    "IS", "AN", "OR", "SO", "VERY", "MUCH", "UP", "SIDE", "WAIT"
}

GENERIC_WORDS = {
    "tip", "tips", "rule", "rules", "stock", "stocks", "share", "shares", "today",
    "good", "best", "all", "now", "market", "it", "this", "that", "why", "how",
    "what", "simple", "deep", "full", "detail", "details", "just", "explain",
    "work", "working", "works", "risk", "level", "levels", "support", "resistance",
    "target", "forecast", "long", "term", "short", "tomorrow", "yesterday",
    "chance", "situation", "about", "with", "and", "or", "in", "on", "at", "of",
    "me", "you", "we", "bro", "sir", "yes", "no", "is", "an", "so", "up", "down",
    "side", "wait"
}

def extract_symbols_from_text(text: str) -> List[str]:
    """
    Search text for known stock aliases, company names, or uppercase ticker patterns,
    ordered by their actual appearance position in the query.
    """
    matches: List[Tuple[int, str]] = []
    lower = text.lower()
    
    # 1. Sort aliases by descending length to prevent sub-string collision
    sorted_aliases = sorted(COMMON_ALIASES.items(), key=lambda x: len(x[0]), reverse=True)
    
    for alias, ticker in sorted_aliases:
        alias_lower = alias.lower()
        if alias_lower in GENERIC_WORDS or alias.upper() in STOPWORDS:
            continue
        # Match word boundaries
        pattern = r"(?:\b|^|\s)" + re.escape(alias_lower) + r"(?:\b|$|\s)"
        for m in re.finditer(pattern, lower):
            matches.append((m.start(), ticker))

    # 2. Check for uppercase or formatted tickers like TCS.NS, RELIANCE, AAPL, MRF, NVDA
    for m in re.finditer(r"\b[A-Za-z0-9\.\^\=\-]{2,14}\b", text):
        w = m.group(0)
        upper_w = w.upper()
        if "." in upper_w or upper_w.startswith("^") or "=" in upper_w:
            matches.append((m.start(), upper_w))
        elif upper_w not in STOPWORDS and upper_w.lower() not in GENERIC_WORDS and len(upper_w) >= 2:
            if upper_w.lower() in COMMON_ALIASES:
                matches.append((m.start(), COMMON_ALIASES[upper_w.lower()]))

    # Sort by position in text and deduplicate preserving order
    matches.sort(key=lambda x: x[0])
    ordered_symbols = []
    for _, sym in matches:
        if sym not in ordered_symbols:
            ordered_symbols.append(sym)

    return ordered_symbols

def classify_intent(text: str, active_symbol: Optional[str] = None) -> Dict[str, Any]:
    """
    Classify intent and extract entities from user query with full conversational context.
    """
    cleaned = text.strip()
    lower = cleaned.lower()

    # Default fallback symbol
    fallback_sym = active_symbol or "TCS.NS"

    # 1. Check for Market Overview
    overview_patterns = [
        "market today", "market status", "how is the market", "how is market",
        "market epdi iruku", "nifty innikku", "nifty epdi", "sensex epdi",
        "market eppadi", "இன்னைக்கு market", "மார்க்கெட் எப்படி", "aaj market kaisa",
        "market outlook", "indices", "overall market", "market summary",
        "nifty இன்னைக்கு எப்படி இருக்கு", "நிப்டி எப்படி இருக்கு", "நிஃப்டி", "market pulse"
    ]
    if any(p in lower for p in overview_patterns) and "compare" not in lower:
        return {
            "intent": "MARKET_OVERVIEW",
            "primary_symbol": "^NSEI",
            "secondary_symbol": None,
            "symbols": ["^NSEI"],
            "timeframe": "1mo",
            "raw_query": cleaned
        }

    # 2. Extract potential stock symbols
    extracted_symbols = extract_symbols_from_text(cleaned)
    primary_symbol = extracted_symbols[0] if len(extracted_symbols) > 0 else fallback_sym
    secondary_symbol = extracted_symbols[1] if len(extracted_symbols) > 1 else None

    # Contextual pronoun check: "this stock", "it", "inda stock", "yeh stock"
    if not extracted_symbols:
        primary_symbol = fallback_sym

    # 3. Check for Stock Comparison
    comparison_patterns = [
        "compare", " vs ", " versus ", "ஒப்பிடு", "vidadhu", "difference", "better", "yaadhu nalladhu", "kisme invest kare"
    ]
    if any(p in lower for p in comparison_patterns):
        # Match forms like "compare TCS and Infosys", "compare it with Infosys", "compare with Infosys"
        comp_match = re.search(r"compare\s+(?:(it|this|this stock|the stock|[A-Za-z0-9\.\^\=\s\-]+?)\s+)?(?:and|with|to|vs)\s+([A-Za-z0-9\.\^\=\s\-]+)", lower)
        if comp_match:
            first_part = (comp_match.group(1) or "").strip()
            second_part = comp_match.group(2).strip()
            if not first_part or first_part in ["it", "this", "this stock", "the stock", "inda stock", "yeh stock"]:
                s1 = fallback_sym
            else:
                s1 = resolve_ticker(first_part)
            s2 = resolve_ticker(second_part)
            return {
                "intent": "STOCK_COMPARISON",
                "primary_symbol": s1,
                "secondary_symbol": s2,
                "symbols": [s1, s2],
                "timeframe": extract_timeframe(cleaned) or "1y",
                "raw_query": cleaned
            }
        elif len(extracted_symbols) >= 2:
            return {
                "intent": "STOCK_COMPARISON",
                "primary_symbol": extracted_symbols[0],
                "secondary_symbol": extracted_symbols[1],
                "symbols": extracted_symbols,
                "timeframe": extract_timeframe(cleaned) or "1y",
                "raw_query": cleaned
            }
        elif len(extracted_symbols) == 1:
            # Comparing active symbol with extracted symbol
            s2 = extracted_symbols[0]
            s1 = fallback_sym if fallback_sym != s2 else ("INFY.NS" if "TCS" in s2 else "TCS.NS")
            return {
                "intent": "STOCK_COMPARISON",
                "primary_symbol": s1,
                "secondary_symbol": s2,
                "symbols": [s1, s2],
                "timeframe": extract_timeframe(cleaned) or "1y",
                "raw_query": cleaned
            }

    # 4. Check for Language Switch (e.g. "Now explain in English", "Tamil-la sollu", "Hindi me batao")
    lang_switch_patterns = [
        "now explain in english", "explain in english", "in english", "english please",
        "tamil-la sollu", "tamil la sollu", "tamilil sollu", "தமிழில் சொல்லு",
        "tanglish-la sollu", "tanglish la sollu", "tanglish please",
        "hindi me batao", "hindi mein batao", "हिंदी में बताओ"
    ]
    if any(p in lower for p in lang_switch_patterns):
        return {
            "intent": "LANGUAGE_SWITCH",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 5. Check for "How it works" / Methodology Option
    how_it_works_patterns = [
        "how it works", "how does it work", "working", "how was this calculated",
        "how do you calculate", "how calculated", "methodology", "calculation formula",
        "epdi calculate panreenga", "kaise calculate kiya", "எப்படி கணக்கிடப்பட்டது"
    ]
    if any(p in lower for p in how_it_works_patterns):
        return {
            "intent": "HOW_IT_WORKS",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 6. Check for "Why?" explanation (Reasoning behind conclusion)
    why_explanation_exact = {"why", "why?", "why so?", "why this conclusion?", "reason enna?", "reason enna", "kyun?", "kyu?", "ஏன்?", "ஏன்", "why so", "why?"}
    if lower in why_explanation_exact or lower.startswith("why this ") or lower.startswith("reason for ") or lower in ["why bullish", "why bearish", "why neutral"]:
        return {
            "intent": "WHY_EXPLANATION",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1mo",
            "raw_query": cleaned
        }

    # 7. Check for "Why did it fall / rise / crash / down?"
    why_patterns = [
        "why did this stock fall", "why did it fall", "why fell", "why drop",
        "down aaga reason", "down aachu", "down aaguthu", "yen down", "yen iranguchu",
        "ஏன் குறைந்தது", "ஏன் இறங்கியது", "down aana reason", "kyun gira", "kyu gira",
        "why crashed", "why down", "why falling", "why tesla falling", "why apple falling",
        "reason என்ன", "காரணம் என்ன", "down ஆக reason", "why rising", "why up"
    ]
    if any(p in lower for p in why_patterns):
        return {
            "intent": "WHY_MOVE",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1mo",
            "raw_query": cleaned
        }

    # 8. Check for Risk Assessment / Query
    risk_patterns = [
        "why is it risky", "why risky", "is this risky", "is it risky", "risk adhigama",
        "risk adhigam", "romba risk", "risk konjam", "risk simple", "risk level",
        "kitna risk", "kitna risk hai", "risk details", "risk analysis", "risk",
        "ஆபத்து", "ஆபத்தானதா", "ரிஸ்க்"
    ]
    if any(p in lower for p in risk_patterns):
        return {
            "intent": "RISK_QUERY",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 9. Check for "Deep Technical" / Detailed Technical Mode
    deep_technical_patterns = [
        "deep technical", "deep technicals", "technical analysis full", "full technical analysis",
        "technical analysis", "all indicators", "detailed technical", "rsi and macd", "bollinger bands",
        "moving averages detail", "technicals", "தொழில்நுட்ப ஆய்வு"
    ]
    if any(p in lower for p in deep_technical_patterns):
        return {
            "intent": "DEEP_TECHNICAL",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 10. Check for Support & Resistance Levels
    sr_patterns = [
        "support level", "resistance level", "support and resistance", "support & resistance",
        "support", "resistance", "key levels", "floor and ceiling", "breakout level",
        "ஆதரவு நிலை", "தடை நிலை", "सपोर्ट", "रेजिस्टेंस"
    ]
    if any(p in lower for p in sr_patterns) and not any(w in lower for w in ["help", "contact", "customer"]):
        return {
            "intent": "SUPPORT_RESISTANCE",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 11. Check for Prediction / Forecast
    prediction_patterns = [
        "predict", "prediction", "forecast", "tomorrow", "next week", "naalaikku",
        "என்ன நடக்கும்", "kal kya hoga", "target", "future price", "what could happen",
        "tomorrow chance epdi", "5-day target", "5 day prediction", "just prediction"
    ]
    if any(p in lower for p in prediction_patterns):
        return {
            "intent": "PREDICTION_QUERY",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 12. Check for Simple Analysis ("Simple ah sollu", "explain simply")
    simple_patterns = [
        "simple ah sollu", "simple overview", "explain simply", "short summary",
        "surukama sollu", "easy explanation", "in simple terms", "simple"
    ]
    if any(p in lower for p in simple_patterns):
        return {
            "intent": "STOCK_ANALYSIS_SIMPLE",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 13. Check for Direction / Bullish vs Bearish
    direction_patterns = [
        "bullish or bearish", "bullish", "bearish", "mela poguma", "keela poguma",
        "மேல போகுமா", "கீழே போகுமா", "eruma", "iranguma", "upar jayega", "niche jayega",
        "will it go up", "will it go down", "trend enna"
    ]
    if any(p in lower for p in direction_patterns):
        return {
            "intent": "STOCK_DIRECTION",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 14. Check for Foreign Currency to Indian Rupees Conversion
    inr_patterns = [
        "dollar to rupee", "dollar to rupees", "dollar to inr", "dollar to indian rupee", "dollar to indian rupees",
        "dollars to rupees", "dollars to inr", "usd to inr", "in rupee", "in rupees", "in inr", "in indian rupee",
        "in indian rupees", "into rupee", "into rupees", "into inr", "into indian rupees", "convert to rupee",
        "convert to rupees", "convert to inr", "convert to indian rupees", "rupee value", "rupees value",
        "price in inr", "price in rupees", "rate in inr", "rate in rupees", "inr price", "change into indian rupees",
        "change to indian rupees", "convert dollar", "dollar to indian",
        "ரூபாயில்", "ரூபாய் மதிப்பு", "ரூபாய்க்கு", "ரூபாய்", "ரூபாய்ல",
        "रुपये में", "रुपए में", "रुपये", "रुपए", "रूपए में", "रूपये", "रुपया",
        "రూపాయల్లో", "రూపాయలు", "రూపాయి", "రూపాయిల్లో",
        "ರೂಪಾಯಿಗಳಲ್ಲಿ", "ರೂಪಾಯಿ", "രൂപയിൽ", "രൂപ", "টাকায়", "টাকা", "રૂપિયામાં", "રૂપિયા"
    ]
    is_inr_requested = False
    for p in inr_patterns:
        if not p.isascii() or " " in p:
            if p in lower:
                is_inr_requested = True
                break
        else:
            if re.search(r"\b" + re.escape(p) + r"\b", lower):
                is_inr_requested = True
                break

    if is_inr_requested and (any(w in lower for w in ["dollar", "usd", "convert", "change", "price", "rate", "value", "மதிப்பு", "விலை", "भाव", "दर"]) or extracted_symbols):
        target_sym = primary_symbol or (extracted_symbols[0] if extracted_symbols else (fallback_sym or "AAPL"))
        return {
            "intent": "CURRENCY_CONVERSION",
            "primary_symbol": target_sym,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "convert_to_inr": True,
            "raw_query": cleaned
        }

    # 15. Check for Stock Market Tips & Trading Rules
    tips_patterns = [
        "stock market tip", "stock market tips", "share market tip", "share market tips",
        "trading tip", "trading tips", "investment tip", "investment tips", "investing tip", "investing tips",
        "stock tip", "stock tips", "market tip", "market tips", "trading rule", "trading rules",
        "investing rule", "investing rules", "golden rule", "golden rules",
        "give tips", "give tip", "give some tips", "give stock market tips", "give a stock market tips",
        "how to trade safely", "trading advice", "investment advice", "best tips",
        "tip", "tips", "advice", "guideline", "guidelines",
        "டிப்ஸ்", "டிப்", "டிப்ஸ் கொடுங்கள்", "முதலீட்டு குறிப்பு", "குறிப்புகள்", "டிப்ஸ் சொல்லுங்க", "டிப்ஸ் என்ன",
        "டிரேடிங் டிப்ஸ்", "பங்குச்சந்தை டிப்ஸ்", "ஸ்டாக் டிப்ஸ்",
        "टिप्स", "सलाह", "सुझाव", "ट्रेडिंग टिप्स", "इन्वेस्टिंग टिप्स", "शेयर मार्केट टिप्स", "मार्केट टिप्स"
    ]
    is_tips = False
    for p in tips_patterns:
        if not p.isascii() or " " in p:
            if p in lower:
                is_tips = True
                break
        else:
            if re.search(r"\b" + re.escape(p) + r"\b", lower):
                is_tips = True
                break

    if is_tips:
        target_sym = None
        if extracted_symbols:
            target_sym = extracted_symbols[0]
        elif any(w in lower for w in ["this stock", "இந்த stock", "inda stock", "yeh stock"]):
            target_sym = fallback_sym

        return {
            "intent": "STOCK_TIPS",
            "primary_symbol": target_sym,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 16. Check for Buy / Sell / Investment setup
    buy_sell_patterns = [
        "buy", "sell", "vaangalaama", "vangalama", "vaanga", "வாங்கலாமா", "வாங்க",
        "kharide", "kharidna", "kharidun", "invest pannalaama", "should i buy",
        "can i invest", "good to buy", "buy side", "wait panradha", "buy side ah"
    ]
    if any(p in lower for p in buy_sell_patterns):
        return {
            "intent": "BUY_SELL_QUERY",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 17. Check for History / Timeframe display
    timeframe_found = extract_timeframe(cleaned)
    if timeframe_found and any(w in lower for w in ["chart", "history", "years", "months", "show me", "last", "long term"]):
        return {
            "intent": "TIMEFRAME_HISTORY",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": timeframe_found,
            "raw_query": cleaned
        }

    # 18. Conversational: How are you?
    how_are_you_patterns = [
        "how are you", "how are u", "how r u", "how do you do",
        "epdi iruka", "eppadi iruka", "epadi irukinga", "epdi irukinga", "epadi irukeenga",
        "எப்படி இருக்கிறீர்கள்", "எப்படி இருக்கீங்க", "எப்படி இருக்கிறாய்", "எப்படி இருக்க?",
        "kaise ho", "kaisa hai", "kya haal", "aap kaise hain", "sab theek",
        "आप कैसे हैं", "कैसे हो", "क्या हाल है", "सब ठीक"
    ]
    stock_reference_terms = [
        "this stock", "இந்த stock", "inda stock", "yeh stock", "stock", "stocks",
        "share", "shares", "பங்கு", "பங்குகள்", "இந்த பங்கு", "company", "ticker"
    ]
    is_stock_referenced = bool(extracted_symbols or any(w in lower for w in stock_reference_terms))

    if not is_stock_referenced and any(p in lower for p in how_are_you_patterns):
        return {
            "intent": "GENERAL_HOW_ARE_YOU",
            "primary_symbol": None,
            "secondary_symbol": None,
            "symbols": [],
            "timeframe": None,
            "raw_query": cleaned
        }

    # 19. Conversational: Capabilities ("What can you do?")
    capabilities_patterns = [
        "what can you do", "what do you do", "who are you", "who r u", "help me",
        "what are your features", "how can you help", "how to use",
        "enna panna mudiyum", "enna seiya mudiyum", "enna help pannuva", "unnala enna panna mudiyum",
        "என்ன செய்ய முடியும்", "என்ன உதவ முடியும்", "யார் நீ",
        "kya kar sakte ho", "tum kya kar sakte ho", "tum kaun ho", "kya madad kar sakte ho",
        "क्या कर सकते हो", "तुम क्या कर सकते हो", "आप क्या कर सकते हैं", "तुम कौन हो",
        "tell me about yourself", "who made you"
    ]
    if not is_stock_referenced and any(p in lower for p in capabilities_patterns):
        return {
            "intent": "GENERAL_CAPABILITIES",
            "primary_symbol": None,
            "secondary_symbol": None,
            "symbols": [],
            "timeframe": None,
            "raw_query": cleaned
        }

    # 20. Conversational: Greetings ("Hello" / "Hi")
    greeting_words = [
        "hi", "hello", "hey", "vanakkam", "வணக்கம்", "namaste", "नमस्ते", "namaskar", "नमस्कार",
        "good morning", "good evening", "good afternoon", "hola", "yo"
    ]
    is_greeting = False
    if not is_stock_referenced:
        for w in greeting_words:
            if not w.isascii():
                if w in lower:
                    is_greeting = True
                    break
            else:
                if re.search(r"\b" + re.escape(w) + r"\b", lower) or lower in ["hi", "hello", "hey", "test"]:
                    is_greeting = True
                    break

    if is_greeting:
        return {
            "intent": "GENERAL_GREETING",
            "primary_symbol": None,
            "secondary_symbol": None,
            "symbols": [],
            "timeframe": None,
            "raw_query": cleaned
        }

    # 21. Check for genuine off-topic questions (e.g. weather, sports, cooking, coding)
    financial_keywords = [
        "stock", "stocks", "share", "shares", "invest", "investing", "investment", "market", "markets",
        "bullish", "bearish", "trade", "trading", "price", "nifty", "sensex", "nasdaq", "dow",
        "dividend", "pe ratio", "p/e", "eps", "target", "support", "resistance", "rsi", "indicator",
        "chart", "fall", "drop", "crash", "rally", "gain", "loss", "profit", "tip", "tips",
        "risk", "risky", "prediction", "forecast", "technical", "technicals", "level", "levels",
        "trend", "why", "how", "reason", "long term", "short term", "adhigam", "adhigama", "epdi", "ippo",
        "situation", "chance", "panradha", "vaangalama", "nalla", "down", "up",
        "பங்கு", "பங்குகள்", "சந்தை", "முதலீடு", "விலை", "லாபம்", "டிப்ஸ்", "ரிஸ்க்",
        "शेयर", "बाजार", "मार्केट", "निवेश", "मुनाफा", "टिप्स", "रिस्क"
    ]
    has_finance_terms = False
    for k in financial_keywords:
        if not k.isascii():
            if k in lower:
                has_finance_terms = True
                break
        else:
            if re.search(r"\b" + re.escape(k) + r"\b", lower):
                has_finance_terms = True
                break

    if not extracted_symbols and not has_finance_terms:
        # User asked something completely unrelated to stocks/markets (e.g. weather, recipes, coding, general trivia)
        return {
            "intent": "GENERAL_OFF_TOPIC",
            "primary_symbol": None,
            "secondary_symbol": None,
            "symbols": [],
            "timeframe": None,
            "raw_query": cleaned
        }

    # 22. Check if user requested detailed / in-depth explanation
    detail_keywords = [
        "detail", "detailed", "deep", "depth", "in-depth", "indicators", "more details",
        "explain more", "full analysis", "விளக்கமா", "detailed-ah", "vistaar", "gehraai"
    ]
    if any(k in lower for k in detail_keywords):
        return {
            "intent": "STOCK_ANALYSIS_DETAILED",
            "primary_symbol": primary_symbol,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": timeframe_found or "1y",
            "raw_query": cleaned
        }

    # 23. Default: Standard Stock Analysis
    return {
        "intent": "STOCK_ANALYSIS",
        "primary_symbol": primary_symbol,
        "secondary_symbol": None,
        "symbols": extracted_symbols,
        "timeframe": timeframe_found or "1y",
        "raw_query": cleaned
    }
