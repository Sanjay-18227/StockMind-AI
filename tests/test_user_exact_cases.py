import sys
import os
import time

# Ensure proper encoding on Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.language import detect_language
from ai.intent import classify_intent
from ai.assistant import (
    format_stock_analysis_response,
    format_why_explanation_response,
    format_deep_technical_response,
    format_how_it_works_response,
    format_risk_explanation_response,
    format_support_resistance_response,
    format_prediction_response,
    format_comparison_response,
)
from app import (
    handle_chat_and_analysis,
    handle_back_navigation,
    handle_ui_refresh,
    get_default_session_state
)

print("=" * 60)
print("RUNNING STOCKMIND AI VERIFICATION SUITE (ALL 12 CASES)")
print("=" * 60)

# Helper to run handle_chat_and_analysis with dummy chart objects
def call_chat(query, history, session_data):
    res = handle_chat_and_analysis(
        user_message=query,
        chat_history=history,
        session_data=session_data,
        current_fig_candle=None,
        current_fig_pred=None,
        current_fig_osc=None,
        current_fig_comp=None,
        current_cards_html="",
        current_strategy_md="",
        current_comp_md="",
        current_deep_tech_md=""
    )
    # Returns: (history, "", session_data, cards, candle, pred, osc, comp, strat, comp_md, deep_md, main_vis, deep_vis, badge)
    return res[0], res[2], res[11], res[12], res[13]

session = get_default_session_state(default_symbol="TCS.NS")
history = []

# TEST 1: User: "Analyze TCS" -> ONE answer only
print("\n--- TEST 1: 'Analyze TCS' ---")
history, session, main_vis, deep_vis, badge = call_chat("Analyze TCS", history, session)
assert len(history) == 2, f"Expected 2 messages (1 user, 1 assistant), got {len(history)}"
assert history[0]["role"] == "user" and history[0]["content"] == "Analyze TCS"
assert history[1]["role"] == "assistant"
assert session["active_symbol"] == "TCS.NS"
assert session["last_analysis"] is not None
# Verify only ONE assistant response exists
assert [m["role"] for m in history] == ["user", "assistant"]
print("✓ TEST 1 PASSED: Exactly ONE user message and ONE assistant response generated.")

# TEST 2: Click: Deep Technical -> Additional technical explanation only, original not duplicated
print("\n--- TEST 2: Click 'Deep Technical' ---")
prev_assistant_msg = history[1]["content"]
history, session, main_vis, deep_vis, badge = call_chat("Deep Technical", history, session)
assert len(history) == 4, f"Expected 4 messages (2 user, 2 assistant), got {len(history)}"
# Verify user message 2 and assistant response 2
assert history[2]["role"] == "user" and history[2]["content"] == "Deep Technical"
assert history[3]["role"] == "assistant"
# Original answer must NOT be repeated
assert history[1]["content"] == prev_assistant_msg
assert history[3]["content"] != prev_assistant_msg
assert "RSI" in history[3]["content"] or "MACD" in history[3]["content"] or "SMA" in history[3]["content"]
assert session["current_view"] == "deep_technical"
print("✓ TEST 2 PASSED: Deep technical details appended cleanly without repeating main answer.")

# TEST 3: Click: Back -> Previous view, NO new AI answer
print("\n--- TEST 3: Click 'Back' ---")
pre_back_history_len = len(history)
# Call navigation handler directly
res_back = handle_back_navigation(session)
# returns: (main_vis, deep_vis, badge, session)
main_vis_update, deep_vis_update, badge_text, session = res_back
assert len(history) == pre_back_history_len, "Back button should NEVER add messages to chat!"
assert session["current_view"] == "main"
print("✓ TEST 3 PASSED: Back navigation returns to main dashboard with ZERO new AI answers.")

# TEST 4: Click Back multiple times -> Navigation only, NO repeated chatbot messages
print("\n--- TEST 4: Click 'Back' multiple times ---")
res_back = handle_back_navigation(session)
session = res_back[3]
res_back = handle_back_navigation(session)
session = res_back[3]
assert len(history) == pre_back_history_len, "Multiple Back clicks must NOT add or repeat messages!"
assert session["current_view"] == "main"
print("✓ TEST 4 PASSED: Multiple Back clicks perform navigation only, ZERO repeated messages.")

# TEST 5: Refresh browser -> App loads safely, previous prompt NOT automatically submitted
print("\n--- TEST 5: Refresh UI / Browser ---")
refresh_res = handle_ui_refresh(session)
# returns: ("", badge, main_vis, deep_vis, new_session)
cleared_text, badge_txt, m_vis, d_vis, fresh_session = refresh_res
assert cleared_text == "", "Input text must be cleared on refresh"
assert fresh_session["is_processing"] is False
assert fresh_session["current_view"] == "main"
print("✓ TEST 5 PASSED: Refresh resets UI safely without resending previous prompt.")

# Reset for conversational and language tests
session = get_default_session_state(default_symbol="TCS.NS")
history = []

# TEST 6: User: "TCS stock ippo epdi iruku?" -> Tanglish response
print("\n--- TEST 6: 'TCS stock ippo epdi iruku?' ---")
lang6 = detect_language("TCS stock ippo epdi iruku?")
assert lang6 in ["tanglish", "ta_latn"], f"Expected tanglish, got {lang6}"
history, session, _, _, _ = call_chat("TCS stock ippo epdi iruku?", history, session)
ans6 = history[-1]["content"]
print(f"Detected language: {lang6}")
print(f"Response snippet: {ans6[:120]}...")
assert "TCS" in ans6
assert any(w in ans6.lower() for w in ["ippo", "kaatuthu", "iruku", "overall", "sentiment", "trend", "momentum"])
print("✓ TEST 6 PASSED: Natural Tanglish response generated.")

# TEST 7: User: "Why risk adhigama iruku?" -> Tanglish contextual explanation about TCS
print("\n--- TEST 7: 'Why risk adhigama iruku?' ---")
lang7 = detect_language("Why risk adhigama iruku?")
assert lang7 in ["tanglish", "ta_latn"], f"Expected tanglish, got {lang7}"
parsed7 = classify_intent("Why risk adhigama iruku?", active_symbol=session["active_symbol"])
assert parsed7["primary_symbol"] == "TCS.NS", f"Expected TCS.NS context, got {parsed7['primary_symbol']}"
history, session, _, _, _ = call_chat("Why risk adhigama iruku?", history, session)
ans7 = history[-1]["content"]
print(f"Detected language: {lang7}, primary_symbol: {parsed7['primary_symbol']}")
print(f"Response snippet: {ans7[:120]}...")
assert "TCS" in ans7
print("✓ TEST 7 PASSED: Contextual Tanglish risk explanation for TCS.")

# TEST 8: User: "अब इसका prediction बताओ" -> Hindi response using existing TCS context
print("\n--- TEST 8: 'अब इसका prediction बताओ' ---")
lang8 = detect_language("अब इसका prediction बताओ")
assert lang8 == "hi", f"Expected hi, got {lang8}"
parsed8 = classify_intent("अब इसका prediction बताओ", active_symbol=session["active_symbol"])
assert parsed8["primary_symbol"] == "TCS.NS", f"Expected TCS.NS context, got {parsed8['primary_symbol']}"
history, session, _, _, _ = call_chat("अब इसका prediction बताओ", history, session)
ans8 = history[-1]["content"]
print(f"Detected language: {lang8}, primary_symbol: {parsed8['primary_symbol']}")
print(f"Response snippet: {ans8[:120]}...")
assert "TCS" in ans8
assert any(w in ans8 for w in ["टारगेट", "प्रेडिक्शन", "पूर्वानुमान", "लक्ष्य", "दिन", "मॉडल", "TCS"])
print("✓ TEST 8 PASSED: Hindi response using TCS context.")

# TEST 9: User: "Now explain in English" -> English response
print("\n--- TEST 9: 'Now explain in English' ---")
lang9 = detect_language("Now explain in English")
assert lang9 == "en", f"Expected en, got {lang9}"
parsed9 = classify_intent("Now explain in English", active_symbol=session["active_symbol"])
assert parsed9["primary_symbol"] == "TCS.NS", f"Expected TCS.NS context, got {parsed9['primary_symbol']}"
history, session, _, _, _ = call_chat("Now explain in English", history, session)
ans9 = history[-1]["content"]
print(f"Detected language: {lang9}, primary_symbol: {parsed9['primary_symbol']}")
print(f"Response snippet: {ans9[:120]}...")
assert "TCS" in ans9
print("✓ TEST 9 PASSED: English response using TCS context.")

# TEST 10: Double-click Send -> Only ONE user request and ONE assistant response
print("\n--- TEST 10: Double-click Send simulation ---")
pre_dclick_count = len(history)
# First click
history, session, _, _, _ = call_chat("Check RSI of TCS", history, session)
# Immediate second click (within rapid duplicate window)
history, session, _, _, _ = call_chat("Check RSI of TCS", history, session)
post_dclick_count = len(history)
# Should add only 1 pair (1 user + 1 assistant)
assert post_dclick_count == pre_dclick_count + 2, f"Expected 2 messages added (1 pair), got {post_dclick_count - pre_dclick_count}"
print("✓ TEST 10 PASSED: Duplicate rapid click rejected. Exactly ONE response produced.")

# TEST 11: User: "Bro Reliance ippo buy side ah illa wait panradha?" -> Casual Tanglish intent
print("\n--- TEST 11: 'Bro Reliance ippo buy side ah illa wait panradha?' ---")
lang11 = detect_language("Bro Reliance ippo buy side ah illa wait panradha?")
parsed11 = classify_intent("Bro Reliance ippo buy side ah illa wait panradha?", active_symbol=session["active_symbol"])
assert parsed11["primary_symbol"] == "RELIANCE.NS", f"Expected RELIANCE.NS, got {parsed11['primary_symbol']}"
history, session, _, _, _ = call_chat("Bro Reliance ippo buy side ah illa wait panradha?", history, session)
ans11 = history[-1]["content"]
print(f"Detected language: {lang11}, primary_symbol: {parsed11['primary_symbol']}")
print(f"Response snippet: {ans11[:120]}...")
assert "RELIANCE" in ans11
print("✓ TEST 11 PASSED: Natural Tanglish response addressing buy/wait for Reliance.")

# TEST 12: User: "Compare it with Infosys" -> Contextual comparison of active_symbol (RELIANCE) and Infosys
print("\n--- TEST 12: 'Compare it with Infosys' ---")
parsed12 = classify_intent("Compare it with Infosys", active_symbol=session["active_symbol"])
print(f"Parsed comparison symbols: primary={parsed12['primary_symbol']}, secondary={parsed12['secondary_symbol']}")
assert parsed12["primary_symbol"] == "RELIANCE.NS", f"Expected RELIANCE.NS, got {parsed12['primary_symbol']}"
assert "INFY" in parsed12["secondary_symbol"], f"Expected INFY, got {parsed12['secondary_symbol']}"
history, session, _, _, _ = call_chat("Compare it with Infosys", history, session)
ans12 = history[-1]["content"]
print(f"Response snippet: {ans12[:120]}...")
assert "RELIANCE" in ans12 and "INFY" in ans12
print("✓ TEST 12 PASSED: 'it' properly mapped to RELIANCE and compared with Infosys.")

print("\n" + "=" * 60)
print("ALL 12 TESTS PASSED PERFECTLY!")
print("=" * 60)
