import sys, os
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import traceback
from ai.language import detect_language
from ai.intent import classify_intent
from ai.assistant import (
    format_market_overview_response,
    format_stock_analysis_response,
    format_comparison_response,
    generate_comparison_analysis,
    format_conversational_response,
    format_stock_tips_response
)
from data.global_market_data import get_market_overview
from data.market_data import resolve_ticker
from model.live_signal import run_complete_stock_analysis

test_queries = [
    "How is the stock market today?",
    "Analyze TCS",
    "Reliance stock epdi iruku?",
    "Apple stock prediction",
    "Compare TCS and Infosys",
    "give a stock market tips",
    "XYZNONEXISTENTSTOCK123"
]

print("=== STARTING CHAT PIPELINE TEST ===")
for q in test_queries:
    print(f"\n--- Testing Query: '{q}' ---")
    try:
        lang = detect_language(q)
        parsed = classify_intent(q, active_symbol="TCS.NS")
        intent = parsed.get("intent")
        primary_sym = parsed.get("primary_symbol") or "TCS.NS"
        secondary_sym = parsed.get("secondary_symbol")
        print(f"Detected: lang={lang}, intent={intent}, primary={primary_sym}, secondary={secondary_sym}")

        if intent in ["GENERAL_GREETING", "GENERAL_HOW_ARE_YOU", "GENERAL_CAPABILITIES", "GENERAL_OFF_TOPIC", "GENERAL_CONVERSATION"] and not parsed.get("symbols"):
            resp = format_conversational_response(intent, lang)
            print("Response length:", len(resp), "Preview:", resp[:60].replace("\n", " "))
        elif intent == "STOCK_TIPS":
            if parsed.get("primary_symbol"):
                res = resolve_ticker(primary_sym)
                an = run_complete_stock_analysis(res)
                resp = format_stock_tips_response(lang, an)
            else:
                resp = format_stock_tips_response(lang)
            print("Response length:", len(resp), "Preview:", resp[:60].replace("\n", " "))
        elif intent == "MARKET_OVERVIEW":
            ov = get_market_overview()
            resp = format_market_overview_response(ov, lang)
            print("Response length:", len(resp), "Preview:", resp[:60].replace("\n", " "))
        elif intent == "STOCK_COMPARISON":
            if not secondary_sym:
                secondary_sym = "INFY.NS" if "TCS" in primary_sym else "TCS.NS"
            comp = generate_comparison_analysis(primary_sym, secondary_sym)
            resp = format_comparison_response(comp, lang)
            print("Response length:", len(resp), "Preview:", resp[:60].replace("\n", " "))
        else:
            resolved = resolve_ticker(primary_sym)
            an = run_complete_stock_analysis(resolved)
            resp = format_stock_analysis_response(an, intent, lang)
            print("Response length:", len(resp), "Preview:", resp[:60].replace("\n", " "))

    except Exception as e:
        print(f"Handled error for '{q}': {e}")

print("\n=== TEST COMPLETED SUCCESSFULLY ===")
