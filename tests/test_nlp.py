import sys, os
sys.path.insert(0, os.path.abspath("."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from ai.language import detect_language
from ai.intent import classify_intent

queries = [
    "How is the stock market today?",
    "Analyze TCS.",
    "Is Reliance bullish or bearish?",
    "What is happening with Apple stock?",
    "Why did this stock fall?",
    "Show me the last 5 years of this stock.",
    "Compare TCS and Infosys.",
    "What could happen tomorrow?",
    "இந்த stock இப்ப எப்படி இருக்கு?",
    "Reliance stock மேல போகுமா?",
    "TCS stock வாங்கலாமா?",
    "Nifty இன்னைக்கு எப்படி இருக்கு?",
    "Apple stock down ஆக reason என்ன?",
    "TCS stock ippo epdi iruku?",
    "give a stock market tips",
    "Give me stock market tips.",
    "Tips for TCS.",
    "trading tips",
    "ஸ்டாக் மார்க்கெட் டிப்ஸ் குடுங்க",
    "trading tips batao"
]

print(f"{'Query':<35} | {'Lang':<8} | {'Intent':<20} | {'Sym':<10}")
print("-" * 80)
for q in queries:
    lang = detect_language(q)
    parsed = classify_intent(q, active_symbol="TCS.NS")
    sym = str(parsed["primary_symbol"])
    intent = parsed["intent"]
    print(f"{q:<35} | {lang:<8} | {intent:<20} | {sym:<10}")
