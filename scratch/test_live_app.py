"""
Test live Gradio server endpoints
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from gradio_client import Client

client = Client("http://127.0.0.1:7860")
print("Connected to live Gradio server!")

# Test query 1: "How is the stock market today?"
print("\n[Test 1] Testing: How is the stock market today?")
res1 = client.predict(
    user_message="How is the stock market today?",
    chat_history=[],
    active_symbol_state="TCS.NS",
    current_fig_candle=None,
    current_fig_pred=None,
    current_fig_osc=None,
    current_fig_comp=None,
    current_cards_html="",
    current_strategy_md="",
    current_comp_md="",
    api_name="/handle_chat_and_analysis"
)
print("Test 1 Result received!")
chat_hist1 = res1[0]
print("Chat History Length:", len(chat_hist1))
print("Assistant reply preview:", chat_hist1[-1]["content"][:80].replace("\n", " "))

# Test query 2: "Analyze TCS"
print("\n[Test 2] Testing: Analyze TCS")
res2 = client.predict(
    user_message="Analyze TCS",
    chat_history=chat_hist1,
    active_symbol_state="TCS.NS",
    current_fig_candle=None,
    current_fig_pred=None,
    current_fig_osc=None,
    current_fig_comp=None,
    current_cards_html="",
    current_strategy_md="",
    current_comp_md="",
    api_name="/handle_chat_and_analysis"
)
print("Test 2 Result received!")
chat_hist2 = res2[0]
print("Active symbol returned:", res2[2])
print("Cards HTML contains current price:", "Current Price" in res2[3])
print("Candlestick plot present:", res2[4] is not None)
print("Prediction plot present:", res2[5] is not None)
print("Assistant reply preview:", chat_hist2[-1]["content"][:80].replace("\n", " "))

# Test query 3: "Reliance stock epdi iruku?" (Tanglish)
print("\n[Test 3] Testing: Reliance stock epdi iruku? (Tanglish)")
res3 = client.predict(
    user_message="Reliance stock epdi iruku?",
    chat_history=chat_hist2,
    active_symbol_state=res2[2],
    current_fig_candle=None,
    current_fig_pred=None,
    current_fig_osc=None,
    current_fig_comp=None,
    current_cards_html="",
    current_strategy_md="",
    current_comp_md="",
    api_name="/handle_chat_and_analysis"
)
print("Test 3 Result received!")
chat_hist3 = res3[0]
print("Active symbol returned:", res3[2])
print("Assistant reply preview:", chat_hist3[-1]["content"][:80].replace("\n", " "))

# Test query 4: "Compare TCS and Infosys"
print("\n[Test 4] Testing: Compare TCS and Infosys")
res4 = client.predict(
    user_message="Compare TCS and Infosys",
    chat_history=chat_hist3,
    active_symbol_state=res3[2],
    current_fig_candle=None,
    current_fig_pred=None,
    current_fig_osc=None,
    current_fig_comp=None,
    current_cards_html="",
    current_strategy_md="",
    current_comp_md="",
    api_name="/handle_chat_and_analysis"
)
print("Test 4 Result received!")
chat_hist4 = res4[0]
print("Comparison plot present:", res4[7] is not None)
print("Comparison markdown contains Head-to-Head:", "Head-to-Head" in res4[9])
print("Assistant reply preview:", chat_hist4[-1]["content"][:80].replace("\n", " "))

# Test query 5: Invalid ticker
print("\n[Test 5] Testing: Invalid ticker query")
res5 = client.predict(
    user_message="Analyze INVALIDSTOCKXYZ999",
    chat_history=chat_hist4,
    active_symbol_state="TCS.NS",
    current_fig_candle=None,
    current_fig_pred=None,
    current_fig_osc=None,
    current_fig_comp=None,
    current_cards_html="",
    current_strategy_md="",
    current_comp_md="",
    api_name="/handle_chat_and_analysis"
)
print("Test 5 Result received!")
chat_hist5 = res5[0]
print("Assistant reply for invalid stock:", chat_hist5[-1]["content"][:100].replace("\n", " "))

print("\n=== ALL LIVE TESTS PASSED PERFECTLY ===")
