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
    "WHY_MOVE",
    "STOCK_DIRECTION",
    "BUY_SELL_QUERY",
    "PREDICTION_QUERY",
    "TIMEFRAME_HISTORY",
    "STOCK_ANALYSIS",
    "STOCK_TIPS",
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
    "TIP", "TIPS", "RULE", "RULES", "ADVICE"
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
    
    GENERIC_WORDS = {"tip", "tips", "rule", "rules", "stock", "stocks", "share", "shares", "today", "good", "best", "all", "now", "market"}
    for alias, ticker in sorted_aliases:
        if alias.lower() in GENERIC_WORDS or alias.upper() in STOPWORDS:
            continue
        # Match word boundaries or non-alphanumeric boundaries
        pattern = r"(?:\b|^|\s)" + re.escape(alias) + r"(?:\b|$|\s)"
        for m in re.finditer(pattern, lower):
            matches.append((m.start(), ticker))

    # 2. Check for uppercase or formatted tickers like TCS.NS, RELIANCE, AAPL, MRF, NVDA
    for m in re.finditer(r"\b[A-Za-z0-9\.\^\=\-]{2,14}\b", text):
        w = m.group(0)
        upper_w = w.upper()
        if "." in upper_w or upper_w.startswith("^") or "=" in upper_w:
            matches.append((m.start(), upper_w))
        elif upper_w not in STOPWORDS and len(upper_w) >= 2:
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
    Classify intent and extract entities from user query.
    """
    cleaned = text.strip()
    lower = cleaned.lower()

    # 1. Check for Market Overview
    overview_patterns = [
        "market today", "market status", "how is the market", "how is market",
        "market epdi iruku", "nifty innikku", "nifty epdi", "sensex epdi",
        "market eppadi", "இன்னைக்கு market", "மார்க்கெட் எப்படி", "aaj market kaisa",
        "market outlook", "indices", "overall market", "market summary",
        "nifty இன்னைக்கு எப்படி இருக்கு", "நிப்டி எப்படி இருக்கு", "நிஃப்டி"
    ]
    if any(p in lower for p in overview_patterns) and "compare" not in lower:
        return {
            "intent": "MARKET_OVERVIEW",
            "primary_symbol": "^NSEI",
            "secondary_symbol": None,
            "timeframe": "1mo",
            "raw_query": cleaned
        }

    # 2. Extract potential stock symbols
    extracted_symbols = extract_symbols_from_text(cleaned)
    primary_symbol = extracted_symbols[0] if len(extracted_symbols) > 0 else active_symbol
    secondary_symbol = extracted_symbols[1] if len(extracted_symbols) > 1 else None

    # Default fallback symbol if query says "this stock" / "இந்த stock" and no active symbol
    if not primary_symbol:
        if any(w in lower for w in ["this stock", "இந்த stock", "inda stock", "yeh stock", "stock"]):
            primary_symbol = active_symbol or "TCS.NS"

    # 3. Check for Stock Comparison
    comparison_patterns = [
        "compare", " vs ", " versus ", "ஒப்பிடு", "vidadhu", "difference", "better", "yaadhu nalladhu", "kisme invest kare"
    ]
    if (any(p in lower for p in comparison_patterns) or secondary_symbol is not None) and (primary_symbol and secondary_symbol):
        return {
            "intent": "STOCK_COMPARISON",
            "primary_symbol": primary_symbol,
            "secondary_symbol": secondary_symbol,
            "timeframe": extract_timeframe(cleaned) or "1y",
            "raw_query": cleaned
        }

    # If user asks compare but only 1 symbol found, check if it's like "Compare TCS and Infosys"
    if any(p in lower for p in comparison_patterns):
        and_match = re.search(r"compare\s+([A-Za-z0-9\s]+?)\s+(?:and|with|to|vs)\s+([A-Za-z0-9\s]+)", lower)
        if and_match:
            s1 = resolve_ticker(and_match.group(1).strip())
            s2 = resolve_ticker(and_match.group(2).strip())
            return {
                "intent": "STOCK_COMPARISON",
                "primary_symbol": s1,
                "secondary_symbol": s2,
                "timeframe": extract_timeframe(cleaned) or "1y",
                "raw_query": cleaned
            }

    # 4. Check for "Why did it fall / rise?"
    why_patterns = [
        "why did this stock fall", "why did it fall", "why fell", "why drop",
        "down aaga reason", "down aachu", "down aaguthu", "yen down", "yen iranguchu",
        "ஏன் குறைந்தது", "ஏன் இறங்கியது", "down aana reason", "kyun gira", "kyu gira",
        "why crashed", "why down", "reason என்ன", "காரணம் என்ன", "down ஆக reason"
    ]
    if any(p in lower for p in why_patterns):
        return {
            "intent": "WHY_MOVE",
            "primary_symbol": primary_symbol or "TCS.NS",
            "secondary_symbol": None,
            "timeframe": "1mo",
            "raw_query": cleaned
        }

    # 5. Check for Direction / Bullish vs Bearish
    direction_patterns = [
        "bullish or bearish", "bullish", "bearish", "mela poguma", "keela poguma",
        "மேல போகுமா", "கீழே போகுமா", "eruma", "iranguma", "upar jayega", "niche jayega",
        "will it go up", "will it go down", "trend enna"
    ]
    if any(p in lower for p in direction_patterns):
        return {
            "intent": "STOCK_DIRECTION",
            "primary_symbol": primary_symbol or "TCS.NS",
            "secondary_symbol": None,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 6. Check for Stock Market Tips & Trading Rules
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
            target_sym = active_symbol or "TCS.NS"

        return {
            "intent": "STOCK_TIPS",
            "primary_symbol": target_sym,
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 7. Check for Buy / Sell / Investment setup
    buy_sell_patterns = [
        "buy", "sell", "vaangalaama", "vangalama", "vaanga", "வாங்கலாமா", "வாங்க",
        "kharide", "kharidna", "kharidun", "invest pannalaama", "should i buy",
        "can i invest", "good to buy"
    ]
    if any(p in lower for p in buy_sell_patterns):
        return {
            "intent": "BUY_SELL_QUERY",
            "primary_symbol": primary_symbol or "TCS.NS",
            "secondary_symbol": None,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 7. Check for Prediction / Forecast
    prediction_patterns = [
        "predict", "prediction", "forecast", "tomorrow", "next week", "naalaikku",
        "என்ன நடக்கும்", "kal kya hoga", "target", "future price", "what could happen"
    ]
    if any(p in lower for p in prediction_patterns):
        return {
            "intent": "PREDICTION_QUERY",
            "primary_symbol": primary_symbol or "TCS.NS",
            "secondary_symbol": None,
            "timeframe": "1y",
            "raw_query": cleaned
        }

    # 8. Check for History / Timeframe display
    timeframe_found = extract_timeframe(cleaned)
    if timeframe_found and any(w in lower for w in ["chart", "history", "years", "months", "show me", "last"]):
        return {
            "intent": "TIMEFRAME_HISTORY",
            "primary_symbol": primary_symbol or "TCS.NS",
            "secondary_symbol": None,
            "timeframe": timeframe_found,
            "raw_query": cleaned
        }

    # 9. Conversational: How are you?
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

    # 10. Conversational: Capabilities ("What can you do?")
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

    # 11. Conversational: Greetings ("Hello" / "Hi")
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

    # 12. Conversational: Off-topic questions
    financial_keywords = [
        "stock", "stocks", "share", "shares", "invest", "investing", "investment", "market", "markets",
        "bullish", "bearish", "trade", "trading", "price", "nifty", "sensex", "nasdaq", "dow",
        "dividend", "pe ratio", "p/e", "eps", "target", "support", "resistance", "rsi", "indicator",
        "chart", "fall", "drop", "crash", "rally", "gain", "loss", "profit", "tip", "tips",
        "பங்கு", "பங்குகள்", "சந்தை", "முதலீடு", "விலை", "லாபம்", "டிப்ஸ்",
        "शेयर", "बाजार", "मार्केट", "निवेश", "मुनाफा", "टिप्स"
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

    # 13. Check if user requested detailed / in-depth explanation
    detail_keywords = [
        "detail", "detailed", "deep", "depth", "in-depth", "indicators", "more details",
        "explain more", "full analysis", "விளக்கமா", "detailed-ah", "vistaar", "gehraai"
    ]
    if any(k in lower for k in detail_keywords):
        return {
            "intent": "STOCK_ANALYSIS_DETAILED",
            "primary_symbol": primary_symbol or "TCS.NS",
            "secondary_symbol": None,
            "symbols": extracted_symbols,
            "timeframe": timeframe_found or "1y",
            "raw_query": cleaned
        }

    # 14. Default: Beginner-friendly Stock Analysis
    return {
        "intent": "STOCK_ANALYSIS",
        "primary_symbol": primary_symbol or "TCS.NS",
        "secondary_symbol": None,
        "symbols": extracted_symbols,
        "timeframe": timeframe_found or "1y",
        "raw_query": cleaned
    }

