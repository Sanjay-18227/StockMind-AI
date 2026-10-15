"""
Multilingual AI Assistant Engine:
Generates natural conversational responses in English, Tamil, Tanglish, and Hindi.
Adapts structure dynamically to the user's question, strictly grounding all output
in quantitative indicators, statistics, risk metrics, and ML predictions.
Supports optional Gemini LLM enrichment when API key is provided.
"""

import os
import requests
from typing import Dict, Any, Optional
from utils.helpers import format_currency, format_percent, format_large_number
from data.global_market_data import get_market_overview
from model.live_signal import run_complete_stock_analysis

def generate_comparison_analysis(symbol_a: str, symbol_b: str, timeframe: str = "1y") -> Dict[str, Any]:
    """
    Run side-by-side analysis for two stocks and return normalized metrics.
    """
    analysis_a = run_complete_stock_analysis(symbol_a, period=timeframe)
    analysis_b = run_complete_stock_analysis(symbol_b, period=timeframe)

    qa, qb = analysis_a["quote"], analysis_b["quote"]
    sa, sb = analysis_a["statistics"], analysis_b["statistics"]
    ia, ib = analysis_a["indicators"]["latest"], analysis_b["indicators"]["latest"]
    ra, rb = analysis_a["risk"], analysis_b["risk"]

    # Normalized comparison series for chart (Base 100)
    series_a = analysis_a["historical_series"]
    series_b = analysis_b["historical_series"]

    # Align dates
    dates_a = series_a["dates"]
    dates_b = series_b["dates"]
    common_dates = sorted(list(set(dates_a).intersection(set(dates_b))))

    price_map_a = dict(zip(dates_a, series_a["close"]))
    price_map_b = dict(zip(dates_b, series_b["close"]))

    norm_a = []
    norm_b = []
    if common_dates:
        base_a = price_map_a[common_dates[0]]
        base_b = price_map_b[common_dates[0]]
        for d in common_dates:
            norm_a.append(round((price_map_a[d] / (base_a + 1e-9)) * 100, 2))
            norm_b.append(round((price_map_b[d] / (base_b + 1e-9)) * 100, 2))

    comparison = {
        "stock_a": {
            "symbol": qa["symbol"],
            "name": qa["name"],
            "price": qa["current_price"],
            "currency_symbol": qa["currency_symbol"],
            "change_pct": qa["change_percent"],
            "return_1y": sa["return_1y_pct"],
            "volatility": sa["annualized_volatility_pct"],
            "max_drawdown": sa["max_drawdown_pct"],
            "sharpe": sa["sharpe_ratio"],
            "rsi": ia["rsi_14"],
            "trend": ia["trend_bias"],
            "risk_level": ra["risk_level"],
            "market_cap": format_large_number(qa["market_cap"], qa["currency"])
        },
        "stock_b": {
            "symbol": qb["symbol"],
            "name": qb["name"],
            "price": qb["current_price"],
            "currency_symbol": qb["currency_symbol"],
            "change_pct": qb["change_percent"],
            "return_1y": sb["return_1y_pct"],
            "volatility": sb["annualized_volatility_pct"],
            "max_drawdown": sb["max_drawdown_pct"],
            "sharpe": sb["sharpe_ratio"],
            "rsi": ib["rsi_14"],
            "trend": ib["trend_bias"],
            "risk_level": rb["risk_level"],
            "market_cap": format_large_number(qb["market_cap"], qb["currency"])
        },
        "correlation": sa["correlation_with_benchmark"],
        "chart_data": {
            "dates": common_dates,
            "normalized_a": norm_a,
            "normalized_b": norm_b
        }
    }
    return comparison


def format_conversational_response(intent: str, lang: str) -> str:
    """
    Format warm, friendly, beginner-friendly conversational replies:
    - Greetings ("Hello" / "Hi") -> Greet warmly and ask how you can help with stocks today.
    - "How are you?" -> Respond politely and guide them toward stock questions.
    - "What can you do?" -> Explain clearly what you can help with.
    - Off-topic questions -> Politely bring the focus back to stock-market discussions.
    """
    if intent == "GENERAL_HOW_ARE_YOU":
        if lang == "tanglish":
            return (
                "**Naan romba nalla iruken, kettadhukku mikka nandri!** 😊\n\n"
                "Market trends, stock analysis, and predictions-ah ungalukku simple-a explain panna naan ready! "
                "Inaikku entha company or stock pathi paakalaam? (e.g., *'Analyze TCS'*, *'Reliance epdi iruku?'*)"
            )
        elif lang == "ta":
            return (
                "**நான் மிகவும் நன்றாக உள்ளேன், கேட்டதற்கு மிக்க நன்றி!** 😊\n\n"
                "பங்குச்சந்தை நிலவரங்கள் மற்றும் விலை போக்குகளை எளிமையாக விளக்க நான் தயாராக உள்ளேன். "
                "இன்று நாம் எந்த பங்கை பற்றி பார்க்கலாம்? (எ.கா. *TCS*, *Reliance*, அல்லது *Nifty*)"
            )
        elif lang in ["hi", "hinglish"]:
            return (
                "**मैं बिल्कुल बढ़िया हूँ, पूछने के लिए धन्यवाद!** 😊\n\n"
                "मैं आपके साथ स्टॉक्स, ट्रेंड्स और मार्केट का सरल विश्लेषण करने के लिए तैयार हूँ। "
                "आज आप किस शेयर या कंपनी के बारे में चर्चा करना चाहेंगे? (जैसे *TCS*, *Reliance*, या *Nifty*)"
            )
        else:
            return (
                "**I'm doing great, thank you for asking!** 😊\n\n"
                "I'm fully ready to track live prices, explain trends, and analyze stocks with you. "
                "Which company or stock are you looking at today? You can ask things like *'Analyze TCS'*, *'Is Apple bullish?'*, or *'How is the market today?'*."
            )

    elif intent == "GENERAL_CAPABILITIES":
        if lang == "tanglish":
            return (
                "### 🤖 StockMind AI-ஆல் உங்களுக்கு என்னென்ன உதவிகள் கிடைக்கும்?\n\n"
                "பங்குச்சந்தையை எளிய முறையில் beginners-க்கும் புரிய வைக்க நான் உதவுகிறேன்:\n\n"
                "• **Stock Insights:** Current price, trend (bullish/bearish), support & resistance levels, மற்றும் risk assessment.\n"
                "• **எளிய காரணங்கள்:** தேவையில்லாத technical jargon இல்லாம stock ஏன் down/up ஆச்சு என்ற விளக்கம்.\n"
                "• **Stocks ஒப்பீடு:** இரண்டு பங்குகளை அருகருகே compare பண்ணி சிறந்ததை அறியலாம் (e.g., *'Compare TCS and Infosys'*).\n"
                "• **Market நிலவரம்:** Nifty, Sensex மற்றும் இன்றைய சந்தை போக்கு.\n"
                "• **பன்மொழி உரையாடல்:** English, தமிழ், Tanglish, அல்லது Hindi-ல் இயல்பாக கேட்கலாம்!\n\n"
                "இப்போ எந்த பங்கை பற்றி பேச ஆரம்பிக்கலாம்?"
            )
        elif lang == "ta":
            return (
                "### 🤖 StockMind AI உங்களுக்கு எவ்வாறு உதவும்?\n\n"
                "பங்குச்சந்தை தகவல்களை எவரும் எளிதாக புரிந்துகொள்ள உதவும் உங்கள் உதவியாளர் நான்:\n\n"
                "• **பங்கு ஆய்வு:** தற்போதைய விலை, சந்தைப் போக்கு (Bullish/Bearish), ஆதரவு & தடை நிலைகள் மற்றும் இடர் அளவு.\n"
                "• **எளிய விளக்கம்:** ஒரு பங்கு ஏன் உயர்ந்தது அல்லது குறைந்தது என்ற நேரடியான விளக்கம்.\n"
                "• **பங்குகள் ஒப்பீடு:** இரு பங்குகளை ஒப்பிட்டுப் பார்க்கும் வசதி (எ.கா. *'Compare TCS and Infosys'*).\n"
                "• **சந்தை நிலவரம்:** Nifty, Sensex குறியீடுகளின் இன்றைய நிலை.\n"
                "• **தமிழ் உரையாடல்:** எந்தவித நிதிச் சொற்கள் கட்டாயமும் இன்றி எளிமையாக பேசலாம்.\n\n"
                "எந்த பங்கை பற்றி முதலில் தெரிந்து கொள்ள விரும்புகிறீர்கள்?"
            )
        elif lang in ["hi", "hinglish"]:
            return (
                "### 🤖 StockMind AI आपकी कैसे मदद कर सकता है?\n\n"
                "मैं शेयर बाजार की जानकारी को हर किसी के लिए, विशेषकर शुरुआती लोगों के लिए आसान बनाता हूँ:\n\n"
                "• **स्टॉक विश्लेषण:** करंट प्राइस, ट्रेंड (Bullish/Bearish), मुख्य सपोर्ट और रेजिस्टेंस, तथा रिस्क लेवल।\n"
                "• **सरल कारण:** कोई स्टॉक क्यों गिरा या बढ़ा, बिना कठिन शब्दों के आसान व्याख्या।\n"
                "• **शेयरों की तुलना:** दो कंपनियों के प्रदर्शन की सीधी तुलना (जैसे *'Compare TCS and Infosys'*)।\n"
                "• **मार्केट मूड:** Nifty और Sensex का ताज़ा हाल।\n"
                "• **अपनी भाषा में बातचीत:** हिंदी, English, हिंग्लिश में सहजता से पूछें!\n\n"
                "आप किस शेयर के बारे में जानकारी चाहते हैं?"
            )
        else:
            return (
                "### 🤖 How I Can Help You as StockMind AI\n\n"
                "My goal is to make stock-market information simple, clear, and actionable for everyone, especially beginners:\n\n"
                "• **Clear Stock Overviews:** Current price, trend (bullish/bearish/neutral), key support & resistance floors, and risk levels.\n"
                "• **Jargon-Free Explanations:** Understand *why* a stock moved up or down without confusing terminology.\n"
                "• **Side-by-Side Comparisons:** Compare any two stocks directly (e.g., *'Compare TCS and Infosys'*).\n"
                "• **Market Pulse:** Quick check on broader market indices like Nifty 50 and Sensex.\n"
                "• **Multilingual Friendly:** Talk naturally in English, Tamil, Tanglish, or Hindi.\n\n"
                "Which stock would you like to explore first?"
            )

    elif intent == "GENERAL_OFF_TOPIC":
        if lang == "tanglish":
            return (
                "**Naan stock market and financial analysis-க்காகவே பிரத்யேகமாக உருவாக்கப்பட்ட assistant!** 📈\n\n"
                "நாம மீண்டும் பங்குச்சந்தை விவாதத்திற்கு வரலாம் — inaikku entha stock, company, or market trend pathi pesalaam? "
                "Ungalukku ethavathu stock pathi doubt iruntha kelunga, simple-a explain panren!"
            )
        elif lang == "ta":
            return (
                "**நான் பிரத்யேகமாக பங்குச்சந்தை மற்றும் நிறுவன ஆய்வுகளுக்கு மட்டுமே பதிலளிக்கக்கூடிய உதவியாளர்!** 📈\n\n"
                "நாம் மீண்டும் பங்குச்சந்தை விவாதத்திற்கு வருவோம் — இன்று உங்களுக்கு எந்த பங்கு அல்லது முதலீடு பற்றி விவாதிக்க வேண்டும்? "
                "பங்குச்சந்தை சார்ந்த எந்த கேள்வியையும் தயங்காமல் கேளுங்கள்!"
            )
        elif lang in ["hi", "hinglish"]:
            return (
                "**मैं खास तौर पर शेयर बाजार, कंपनी विश्लेषण और मार्केट ट्रेंड्स के लिए हूँ!** 📈\n\n"
                "चलिए बाजार की चर्चा पर वापस आते हैं — आज आप किस शेयर या कंपनी के बारे में बात करना चाहेंगे? "
                "शेयर बाजार से संबंधित किसी भी सवाल के लिए बेझिझक पूछें!"
            )
        else:
            return (
                "**I specialize specifically in stock-market analysis, company performance, and financial trends!** 📈\n\n"
                "Let's bring our focus back to the market — which stock, company, or sector would you like to discuss today? "
                "Feel free to ask about any stock (like TCS, Reliance, Apple), market trends, or stock comparisons!"
            )

    else:
        # Default GREETING ("Hello" / "Hi")
        if lang == "tanglish":
            return (
                "**வணக்கம்! நான் StockMind AI.** 👋📈\n\n"
                "பங்குச்சந்தை தகவல்களை எல்லோருக்கும் புரியற மாதிரி எளிமையா சொல்ல நான் ரெடி! "
                "இன்னைக்கு உங்களுக்கு பங்குகள் (stocks) அல்லது market நிலவரத்தில் நான் எப்படி உதவ முடியும்?\n\n"
                "*உதாரணத்திற்கு: `TCS stock ippo epdi iruku?`, `Reliance bullish-a?`, அல்லது `How is the market today?`*"
            )
        elif lang == "ta":
            return (
                "**வணக்கம்! நான் StockMind AI.** 👋📈\n\n"
                "பங்குச்சந்தை தகவல்களை எளிதாக புரிந்துகொள்ள நான் உங்களுக்கு உதவுகிறேன். "
                "இன்று உங்களுக்கு எந்த பங்கு அல்லது சந்தை நிலவரத்தில் உதவ வேண்டும்?\n\n"
                "*உதாரணத்திற்கு: `TCS பங்கு எப்படி உள்ளது?`, `Reliance மேல போகுமா?`, அல்லது `இன்றைய சந்தை நிலவரம் என்ன?`*"
            )
        elif lang in ["hi", "hinglish"]:
            return (
                "**नमस्ते! मैं StockMind AI हूँ।** 👋📊\n\n"
                "शेयर बाजार की जानकारी को सरल और आसान भाषा में समझाने के लिए मैं यहाँ हूँ। "
                "आज मैं स्टॉक्स या मार्केट के बारे में आपकी क्या मदद कर सकता हूँ?\n\n"
                "*उदाहरण: `TCS का हाल कैसा है?`, `Reliance bullish है या bearish?`, या `आज मार्केट कैसा है?`*"
            )
        else:
            return (
                "**Hello! 👋 Welcome to StockMind AI.**\n\n"
                "I'm your smart, friendly stock-market assistant, designed to make investing and market information easy to understand for everyone.\n\n"
                "How can I help you with stocks or market trends today? You can ask about any company (like TCS, Reliance, Apple), check today's market mood, or compare two stocks!"
            )


def format_stock_tips_response(lang: str, analysis: Optional[Dict[str, Any]] = None) -> str:
    """
    Format actionable, professional stock market tips & golden trading rules.
    If a specific stock analysis is provided (e.g. "tips for TCS"), combines stock-specific
    actionable levels (support floor, resistance target, RSI caution, position stop-loss)
    with institutional trading rules.
    Otherwise, delivers complete institutional stock market guidelines.
    """
    if analysis is not None:
        q = analysis["quote"]
        ind = analysis["indicators"]["latest"]
        sr = analysis["support_resistance"]
        rk = analysis["risk"]
        sg = analysis["strategy"]

        sym = q["symbol"]
        name = q["name"]
        curr = format_currency(q["current_price"], q["currency_symbol"])
        chg = format_percent(q["change_percent"])
        rsi = ind["rsi_14"]
        trend = ind["trend_bias"]
        sup = format_currency(sr["nearest_support"], q["currency_symbol"])
        res = format_currency(sr["nearest_resistance"], q["currency_symbol"])
        inval = format_currency(sg["invalidation_level"], q["currency_symbol"])
        risk = rk["risk_level"]
        rr = sg["risk_reward_ratio"]

        # Formulate tactical advice based on RSI and trend
        if rsi >= 70:
            rsi_tip_en = f"RSI is currently Overbought ({rsi:.1f}). Avoid buying aggressively at resistance {res}; wait for a healthy pullback towards {sup}."
            rsi_tip_tang = f"RSI Overbought-ல் ({rsi:.1f}) இருக்கு. உச்சத்தில் அவசரப்பட்டு வாங்காதீங்க; {sup} support நோக்கி pullback வரும் வரை காத்திருங்கள்."
            rsi_tip_ta = f"RSI மிகை-வாங்குதல் (Overbought {rsi:.1f}) நிலையில் உள்ளது. உச்சத்தில் வாங்காமல் {sup} ஆதரவு வரை காத்திருப்பது நல்லது."
            rsi_tip_hi = f"RSI ओवरबॉट ज़ोन ({rsi:.1f}) में है। ऊपरी स्तरों पर तुरंत खरीदारी से बचें, {sup} सपोर्ट की ओर गिरावट का इंतजार करें।"
        elif rsi <= 35:
            rsi_tip_en = f"RSI is currently Oversold ({rsi:.1f}) near support {sup}. Look for bullish volume confirmation or reversal candlestick before entry."
            rsi_tip_tang = f"RSI Oversold-ல் ({rsi:.1f}) இருக்கு. ஆதரவு {sup} அருகில் reversal volume வருகிறதா என்று கவனித்து என்ட்ரி எடுக்கலாம்."
            rsi_tip_ta = f"RSI மிகை-விற்பனை (Oversold {rsi:.1f}) நிலையில் உள்ளது. {sup} ஆதரவு அருகே திருப்புமுனை சமிக்ஞை தென்படுகிறதா என கவனிக்கவும்."
            rsi_tip_hi = f"RSI ओवरसोल्ड ज़ोन ({rsi:.1f}) में है। {sup} सपोर्ट के पास रिवर्सल कैंडल या वॉल्यूम की पुष्टि के बाद ही ट्रेड प्लान करें।"
        else:
            rsi_tip_en = f"RSI is balanced ({rsi:.1f}). Trade strictly with the {trend} trend using a disciplined stop-loss."
            rsi_tip_tang = f"RSI சமநிலையில் ({rsi:.1f}) இருக்கு. {trend} போக்குக்கு ஏற்றவாறு Stop-loss உடன் trade செய்யலாம்."
            rsi_tip_ta = f"RSI சமநிலையான ({rsi:.1f}) அளவில் உள்ளது. சந்தைப் போக்குக்கு ({trend}) இணங்க Stop-loss உடன் வர்த்தகம் செய்யவும்."
            rsi_tip_hi = f"RSI संतुलित स्तर ({rsi:.1f}) पर है। {trend} ट्रेंड के अनुसार स्टॉप-लॉस के साथ ट्रेड करें।"

        if lang == "tanglish":
            return (
                f"### 💡 {name} ({sym}) - Actionable Stock Tips & Trading Levels\n\n"
                f"• **Current Price:** **{curr}** ({chg})\n"
                f"• **Technical Trend:** **{trend}**\n"
                f"• **Key Support (Safety Floor):** **{sup}** *(Stop-Loss Reference)*\n"
                f"• **Key Resistance (Target Zone):** **{res}** *(Profit-Booking Area)*\n"
                f"• **RSI Momentum ({rsi:.1f}):** {rsi_tip_tang}\n\n"
                f"---\n"
                f"#### 🎯 இந்த பங்குக்கான 4 முக்கிய Tips:\n"
                f"1. **Entry Strategy:** அவசரப்பட்டு Resistance ({res}) அருகில் வாங்காதீர்கள். {sup} ஆதரவு அருகில் pullback வரும்போது வாங்கலாம்.\n"
                f"2. **Stop-Loss Discipline:** {inval}-க்கு கீழே விலை இறங்கினால் setup தவறானது என்று ஏற்றுக்கொண்டு வெளியேறவும்.\n"
                f"3. **Position Sizing:** இந்த ஒரு பங்கில் உங்கள் மொத்த முதலீட்டில் 1-2%-க்கு மேல் நஷ்டம் வராதவாறு share quantity-ஐ தேர்வு செய்யுங்கள்.\n"
                f"4. **Risk-to-Reward:** இந்த பங்கின் தற்போதைய setup R:R ratio: **{rr}**.\n\n"
                f"---\n"
                f"⚠️ *முக்கிய குறிப்பு: இது கல்வி சார்ந்த Technical Analysis மட்டுமே. தனிப்பட்ட நிதி ஆலோசனை (Financial Advice) அல்ல.*"
            )
        elif lang == "ta":
            return (
                f"### 💡 {name} ({sym}) - முதலீட்டு குறிப்புகள் & முக்கிய நிலைகள்\n\n"
                f"• **தற்போதைய விலை:** **{curr}** ({chg})\n"
                f"• **சந்தை போக்கு (Trend):** **{trend}**\n"
                f"• **ஆதரவு நிலை (Support):** **{sup}** *(நஷ்டத் தடுப்பு குறிப்பு)*\n"
                f"• **தடை நிலை (Resistance):** **{res}** *(இலக்கு / லாப பதிவு எல்லை)*\n"
                f"• **RSI வேகம் ({rsi:.1f}):** {rsi_tip_ta}\n\n"
                f"---\n"
                f"#### 🎯 இந்த பங்கை வர்த்தகம் செய்வதற்கான முக்கிய குறிப்புகள்:\n"
                f"1. **நுழைவு உத்தி (Entry):** {sup} ஆதரவு எல்லைக்கு அருகில் அல்லது {res} நிலையை வால்யூமுடன் உடைக்கும் போது மட்டுமே வாங்குவது பாதுகாப்பானது.\n"
                f"2. **நஷ்டத் தடுப்பு (Stop-Loss):** {inval} அளவுக்கு கீழே விலை சென்றால் நஷ்டத்தை ஏற்று வெளியேறவும்.\n"
                f"3. **மூலதன மேலாண்மை:** ஒரு வர்த்தகத்தில் மொத்த கணக்கில் 1-2% மேல் இழக்க வேண்டாம்.\n"
                f"4. **இடர் - வருவாய் விகிதம்:** தற்போதைய அமைப்பு விகிதம்: **{rr}**.\n\n"
                f"---\n"
                f"⚠️ *மறுப்பு: இது கல்வி மற்றும் விழிப்புணர்வு நோக்கங்களுக்கான ஆய்வு மட்டுமே.*"
            )
        elif lang in ["hi", "hinglish"]:
            return (
                f"### 💡 {name} ({sym}) - ट्रेडिंग टिप्स और मुख्य लेवल्स\n\n"
                f"• **करंट प्राइस:** **{curr}** ({chg})\n"
                f"• **टेक्निकल ट्रेंड:** **{trend}**\n"
                f"• **अहम सपोर्ट (Support):** **{sup}** *(स्टॉप-लॉस स्तर)*\n"
                f"• **अहम रेजिस्टेंस (Resistance):** **{res}** *(टारगेट / प्रॉफिट बुकिंग ज़ोन)*\n"
                f"• **RSI मोमेंटम ({rsi:.1f}):** {rsi_tip_hi}\n\n"
                f"---\n"
                f"#### 🎯 {name} के लिए 4 ज़रूरी टिप्स:\n"
                f"1. **एंट्री स्ट्रैटेजी:** रेजिस्टेंस ({res}) के ठीक पास चेज़ करने से बचें। {sup} के पास डिप्स पर ही एंट्री की योजना बनाएं।\n"
                f"2. **स्टॉप-लॉस अनुशासन:** {inval} के नीचे क्लोजिंग मिलने पर ट्रेड से बाहर निकलें।\n"
                f"3. **कैपिटल प्रोटेक्शन:** इस ट्रेड में कुल पोर्टफोलियो का 1-2% से अधिक रिस्क न लें।\n"
                f"4. **रिस्क-रिवॉर्ड रेश्यो:** इस सेटअप का अनुमानित R:R: **{rr}**।\n\n"
                f"---\n"
                f"⚠️ *अस्वीकरण: यह केवल शैक्षणिक और तकनीकी विश्लेषण पर आधारित जानकारी है, व्यक्तिगत वित्तीय सलाह नहीं।*"
            )
        else:
            return (
                f"### 💡 {name} ({sym}) — Actionable Stock Tips & Key Levels\n\n"
                f"• **Current Price:** **{curr}** ({chg})\n"
                f"• **Prevailing Trend:** **{trend}**\n"
                f"• **Key Support (Floor):** **{sup}** *(Primary Stop-Loss Anchor)*\n"
                f"• **Key Resistance (Ceiling):** **{res}** *(Upside Target & Profit Zone)*\n"
                f"• **RSI Condition ({rsi:.1f}):** {rsi_tip_en}\n\n"
                f"---\n"
                f"#### 🎯 4 Execution Rules for Trading {name}:\n"
                f"1. **Entry Discipline:** Do not chase gap-ups or buy right under resistance ({res}). The highest-probability entry is on a confirmed test of support ({sup}).\n"
                f"2. **Strict Invalidation Level:** A sustained breakdown below **{inval}** invalidates the bullish thesis. Cut the loss without hesitation.\n"
                f"3. **Position Sizing Rule:** Size your shares so that hitting the stop-loss at {inval} risks no more than 1% to 2% of your total trading capital.\n"
                f"4. **Risk-to-Reward Ratio:** This technical setup currently offers an estimated R:R ratio of **{rr}**.\n\n"
                f"---\n"
                f"⚠️ *Disclaimer: Educational technical setup. Not individual investment advice. Always manage risk rigorously.*"
            )

    # General Stock Market Tips (No specific stock specified)
    if lang == "tanglish":
        return (
            "### 💡 பங்குச்சந்தைக்கான 7 பொன்விதிகள் (Stock Market Tips & Golden Rules)\n\n"
            "பங்குச்சந்தையில் (Stock Market) நீண்ட காலத்தில் நஷ்டத்தை தவிர்த்து நிலையான வெற்றி பெற, "
            "தொழில்முறை முதலீட்டாளர்கள் பின்பற்றும் இந்த **7 முக்கிய விதிகளை** எப்போதும் நினைவில் வையுங்கள்:\n\n"
            "---\n\n"
            "#### 1. 🛡️ Risk Management (1-2% மூலதன விதி)\n"
            "• உங்க மொத்த முதலீட்டில் (Capital) எந்த ஒரு தனி trade-க்கும் **1% முதல் 2%-க்கு மேல் நஷ்டம் வர அனுமதிக்காதீர்கள்**.\n"
            "• உங்க Stop-loss தூரத்தை வைத்து வாங்கும் shares எண்ணிக்கையை (position sizing) கணக்கிடுங்கள், பேராசையால் அதிக shares வாங்காதீர்கள்.\n\n"
            "#### 2. 🛑 எப்போதும் Stop-Loss உடன் வர்த்தகம் செய்யுங்கள்\n"
            "• Order போடுவதற்கு முன்பே **Stop-loss எங்கே வைக்க வேண்டும்** என்பதை திட்டமிடுங்கள்.\n"
            "• விலை குறையும் போது பயந்துபோய் Stop-loss-ஐ தள்ளி வைக்காதீர்கள். சிறிய நஷ்டம் உங்களை சந்தையில் உயிருடன் வைக்கும்; பெரிய நஷ்டம் முதலீட்டை அழித்துவிடும்.\n\n"
            "#### 3. 📈 Trend-ஐ எதிர்த்து நிற்காதீர்கள் (\"Trend is Your Friend\")\n"
            "• 50 EMA & 200 EMA-க்கு மேல் பயணிக்கும் uptrend பங்குகளிலேயே அதிக வாய்ப்புகளை தேடுங்கள்.\n"
            "• \"விலை 40% இறங்கிடுச்சு, இப்போ cheap-ஆ இருக்கு\" என்று கீழே சரியும் பங்குகளை (falling knife) அவசரப்பட்டு வாங்காதீர்கள். Reversal உறுதியாகும் வரை பொறுமை காக்கவும்.\n\n"
            "#### 4. ⚖️ Risk-to-Reward Ratio (குறைந்தது 1:2)\n"
            "• நீங்கள் எடுக்கும் ஒவ்வொரு ₹1 நஷ்ட அபாயத்திற்கும் குறைந்தது **₹2 லாபம் கிடைக்க வாய்ப்புள்ள trades-ஐ மட்டுமே** தேர்ந்தெடுக்கவும்.\n"
            "• 1:2 ratio இருந்தால் 50% முறை தவறு செய்தாலும் உங்கள் மொத்த கணக்கில் நல்ல லாபமே நிற்கும்!\n\n"
            "#### 5. 🧩 Diversification (துறைசார் பரவலாக்கம்)\n"
            "• மொத்த முதலீட்டையும் ஒரே பங்கில் அல்லது ஒரே sector-ல் போடாதீர்கள்.\n"
            "• **70/30 பார்முலா:** 70% பணத்தை Nifty 50 தரமான பெரிய நிறுவனங்களிலும், 30% தொகையை swing/momentum trading-லும் பிரித்து வைக்கவும்.\n\n"
            "#### 6. 🧘 FOMO-வை தவிருங்கள் (உச்சத்தில் வாங்காதீர்கள்)\n"
            "• ஒரு பங்கு ஏற்கனவே 2-3 நாட்களில் 15% ஏறிவிட்டால், அவசரப்பட்டு துரத்தி வாங்காதீர்கள் (No FOMO). Support-க்கு pullback வரும் வரை காத்திருங்கள்.\n"
            "• ஒரு trade நஷ்டமானால் உடனே கோபத்தில் அடுத்த trade எடுக்காதீர்கள் (Revenge trading வேண்டாம்).\n\n"
            "#### 7. 📖 Trading Journal பராமரியுங்கள்\n"
            "• ஒவ்வொரு trade-ன் Entry, Exit, காரணம் மற்றும் செய்த தவறுகளை டைரியில் எழுதி வையுங்கள். உங்கள் தவறுகளே சிறந்த ஆசான்.\n\n"
            "---\n"
            "| முக்கிய விதி | செய்ய வேண்டியது | பயன் |\n"
            "| :--- | :--- | :--- |\n"
            "| **Capital Risk** | Trade-க்கு 1-2% நஷ்ட வரம்பு | முழு மூலதனம் அழியாமல் காக்கும் |\n"
            "| **Stop-Loss** | Entry போடும்போதே நிர்ணயிக்கவும் | உணர்ச்சிவசப்பட்டு முடிவெடுப்பதை தடுக்கும் |\n"
            "| **Risk / Reward** | குறைந்தது 1:2 விகிதம் | நீண்டகால நிலையான லாபம் |\n"
            "| **Psychology** | உச்சத்தில் துரத்தி வாங்காதீர்கள் | அதிக விலையில் சிக்குவதை தடுக்கும் |\n\n"
            "---\n"
            "⚠️ *முக்கிய குறிப்பு: இது கல்வி மற்றும் விழிப்புணர்வுக்கான தகவல் மட்டுமே. தனிப்பட்ட நிதி ஆலோசனை (Financial Advice) அல்ல.*"
        )
    elif lang == "ta":
        return (
            "### 💡 பங்குச்சந்தை முதலீடு & வர்த்தகத்திற்கான 7 பொன்விதிகள் (Stock Market Tips)\n\n"
            "பங்குச்சந்தையில் மூலதனத்தை பாதுகாத்து நிலையான லாபம் ஈட்ட அனுபவமிக்க முதலீட்டாளர்கள் பின்பற்றும் **7 அத்தியாவசிய விதிகள்** இதோ:\n\n"
            "---\n\n"
            "#### 1. 🛡️ மூலதனப் பாதுகாப்பு (1-2% இடர் விதி)\n"
            "• எந்தவொரு தனிப்பட்ட வர்த்தகத்திலும் உங்கள் மொத்த தொகையில் **1% முதல் 2%-க்கு மேல் இழப்பை அனுமதிக்காதீர்கள்**.\n"
            "• பங்குகளை வாங்கும் அளவை (Position Size) உங்கள் நஷ்ட வரம்பை அடிப்படையாகக் கொண்டு தீர்மானியுங்கள்.\n\n"
            "#### 2. 🛑 நஷ்டத் தடுப்பு வரம்பு (Stop-Loss) கட்டாயம்\n"
            "• வர்த்தகத்தில் இறங்குவதற்கு முன்பே Stop-Loss விலையை நிர்ணயித்து கணினியில் பதிவு செய்யுங்கள்.\n"
            "• விலை சரியும்போது நஷ்டத் தடுப்பு வரம்பை தள்ளி வைக்காதீர்கள்.\n\n"
            "#### 3. 📈 சந்தைப் போக்கின்படி வர்த்தகம் (Trend Following)\n"
            "• சந்தையின் போக்கிற்கு எதிராக வர்த்தகம் செய்யாதீர்கள். 50 மற்றும் 200 நாள் நகரும் சராசரிகளுக்கு (EMA) மேலே உள்ள பங்குகளை தேர்ந்தெடுக்கவும்.\n"
            "• வேகமாக சரியும் பங்குகளை \"மலிவாக உள்ளது\" என்ற ஒரே காரணத்திற்காக முன்கூட்டியே வாங்காதீர்கள்.\n\n"
            "#### 4. ⚖️ இடர் - வருவாய் விகிதம் (குறைந்தது 1:2)\n"
            "• நீங்கள் ஏற்கும் ஒவ்வொரு ₹1 இழப்பு அபாயத்திற்கும் ₹2 அல்லது அதற்கு மேற்பட்ட லாப வாய்ப்புள்ள அமைப்புகளில் மட்டுமே வர்த்தகம் செய்யுங்கள்.\n\n"
            "#### 5. 🧩 முதலீட்டுப் பரவலாக்கம் (Diversification)\n"
            "• அனைத்து மூலதனத்தையும் ஒரே பங்கில் அல்லது ஒரே துறையில் குவிக்காதீர்கள்; வெவ்வேறு துறைகளில் பிரித்து முதலீடு செய்யவும்.\n\n"
            "#### 6. 🧘 உணர்ச்சிகளைக் கட்டுப்படுத்துதல் (FOMO தவிர்த்தல்)\n"
            "• மிக வேகமாக உயர்ந்த பங்குகளை உச்சத்தில் அவசரமாக துரத்தி வாங்காதீர்கள்; விலை நிலைபெறும் வரை காத்திருங்கள்.\n"
            "• நஷ்டத்திற்குப் பிறகு பழிவாங்கும் நோக்கில் அவசரமாக வர்த்தகம் செய்வதை (Revenge Trading) தவிர்க்கவும்.\n\n"
            "#### 7. 📖 வர்த்தகக் குறிப்பேடு (Trading Journal)\n"
            "• ஒவ்வொரு வர்த்தகத்தின் முடிவுகள், நுழைவு, வெளியேறுதல் மற்றும் காரணங்களை குறித்து வைத்து வாரந்தோறும் ஆய்வு செய்யுங்கள்.\n\n"
            "---\n"
            "⚠️ *பொறுப்புத் துறப்பு: இது கல்வி மற்றும் விழிப்புணர்வு நோக்கங்களுக்கான தகவல்கள் மட்டுமே. முதலீட்டு முடிவுகளுக்கு முன் தகுதியான நிதி ஆலோசகரை அணுகவும்.*"
        )
    elif lang in ["hi", "hinglish"]:
        return (
            "### 💡 शेयर बाजार के 7 स्वर्णिम नियम और टिप्स (Stock Market Tips & Golden Rules)\n\n"
            "शेयर बाजार में पूंजी सुरक्षित रखते हुए अनुशासित और सफल निवेशक बनने के लिए ये **7 गोल्डन रूल्स** हमेशा याद रखें:\n\n"
            "---\n\n"
            "#### 1. 🛡️ रिस्क मैनेजमेंट (1-2% कैपिटल नियम)\n"
            "• किसी भी एक ट्रेड में अपनी कुल ट्रेडिंग पूंजी का **1% से 2% से अधिक जोखिम न लें**।\n"
            "• अपनी पोजीशन का साइज हमेशा स्टॉप-लॉस की दूरी देखकर तय करें, लालच में आकर ओवर-ट्रेडिंग न करें।\n\n"
            "#### 2. 🛑 हमेशा Stop-Loss लगाएं (नो एक्सेप्शन)\n"
            "• ट्रेड में एंट्री लेने से पहले ही स्टॉप-लॉस तय करें।\n"
            "• ट्रेड गलत जाने पर स्टॉप-लॉस को कभी पीछे न हटाएं। छोटे नुकसान स्वीकार करना ही बड़ी पूंजी को बचाता है।\n\n"
            "#### 3. 📈 ट्रेंड के साथ ट्रेड करें (\"Trend is Your Friend\")\n"
            "• 50 EMA और 200 EMA के ऊपर मजबूत ट्रेंड वाले शेयरों में खरीदारी के मौके ढूंढें।\n"
            "• गिरते हुए शेयर को केवल \"सस्ता\" समझकर बॉटम पर पकड़ने की कोशिश न करें (Catching a falling knife से बचें)।\n\n"
            "#### 4. ⚖️ रिस्क-रिवॉर्ड रेश्यो (कम से कम 1:2)\n"
            "• हमेशा ऐसे सेटअप चुनें जहाँ संभावित मुनाफा (Reward) आपके नुकसान (Risk) से कम से कम **2 गुना** हो।\n"
            "• 1:2 R:R होने पर अगर आप 50% ट्रेड्स में भी गलत होते हैं, तब भी आपका कुल खाता मुनाफे में रहेगा!\n\n"
            "#### 5. 🧩 पोर्टफोलियो डाइवर्सिफिकेशन\n"
            "• सारा पैसा एक ही शेयर या एक ही सेक्टर (जैसे केवल आईटी या पेनी स्टॉक्स) में न लगाएं।\n"
            "• 70% पूंजी मजबूत ब्लू-चिप कंपनियों में और 30% स्विंग/मोमेंटम ट्रेड्स में बांटें।\n\n"
            "#### 6. 🧘 FOMO (छूट जाने का डर) से बचें\n"
            "• जो शेयर 2-3 दिनों में 15% भाग चुका हो, उसे ऊपर के स्तरों पर न खरीदें। रिट्रेसमेंट या सपोर्ट पर आने का इंतजार करें।\n"
            "• नुकसान के तुरंत बाद गुस्से या बदले की भावना में ट्रेड (Revenge Trading) न करें।\n\n"
            "#### 7. 📖 ट्रेडिंग जर्नल बनाएं\n"
            "• अपने हर ट्रेड की एंट्री, एग्जिट, कारण और सीखी गई बातें लिखें और नियमित रूप से उसकी समीक्षा करें।\n\n"
            "---\n"
            "| नियम | क्या करें | फायदा |\n"
            "| :--- | :--- | :--- |\n"
            "| **Capital Risk** | प्रति ट्रेड 1-2% का रिस्क | पूंजी कभी खत्म नहीं होगी |\n"
            "| **Stop-Loss** | एंट्री के समय ही लगाएं | भावनाओं में गलत फैसले नहीं होंगे |\n"
            "| **Risk / Reward** | कम से कम 1:2 अनुपात | दीर्घकालिक निरंतर लाभ |\n"
            "| **Psychology** | टॉप पर चेज़ न करें | ऊंचे दामों पर फंसने से बचाव |\n\n"
            "---\n"
            "⚠️ *अस्वीकरण: यह केवल शैक्षणिक और वित्तीय जागरूकता के लिए है, व्यक्तिगत निवेश सलाह नहीं।*"
        )
    else:
        # Default English
        return (
            "### 💡 Institutional Stock Market Rules & Trading Tips\n\n"
            "Here are the **7 Golden Rules of Stock Market Success** followed by professional fund managers and disciplined traders:\n\n"
            "---\n\n"
            "#### 1. 🛡️ Master Capital Risk Management (The 1-2% Rule)\n"
            "• **Never risk more than 1% to 2%** of your total portfolio on any single trade.\n"
            "• Calculate your position sizing based on your stop-loss distance, never on gut feeling or optimism.\n"
            "• *Example:* With a ₹1,00,000 account, your maximum loss per trade if stopped out must not exceed ₹1,000 to ₹2,000.\n\n"
            "#### 2. 🛑 Always Use a Defined Stop-Loss (Non-Negotiable)\n"
            "• Place your hard stop-loss order in the system **simultaneously with your entry**.\n"
            "• **Never widen or remove a stop-loss** when the market moves against you. Small, controlled losses keep you in the game; unmanaged drawdowns ruin accounts.\n\n"
            "#### 3. 📈 Trade in the Direction of the Trend (\"Trend is Your Friend\")\n"
            "• Focus your long ideas on stocks trading **above their 50-day and 200-day EMAs** with rising volume.\n"
            "• Avoid \"catching falling knives\" simply because a stock looks cheap after a 40% fall — a cheap stock can easily drop another 50% until technical accumulation confirms a bottom.\n\n"
            "#### 4. ⚖️ Demand an Asymmetric Risk-to-Reward Ratio (Min 1:2)\n"
            "• Only execute setups where the realistic technical target offers at least **twice the distance** of your stop-loss.\n"
            "• With a 1:2 Risk-to-Reward ratio, you only need a **35% to 40% win rate** to remain consistently profitable over time.\n\n"
            "#### 5. 🧩 Diversification & The 70/30 Core-Satellite Strategy\n"
            "• Never concentrate your entire capital into a single stock or a single sector (e.g. only IT or only small-caps).\n"
            "• **70% Core:** Quality large-cap market leaders with clean balance sheets and consistent earnings growth.\n"
            "• **30% Satellite:** Tactical swing setups and high-momentum leaders managed with trailing stop-losses.\n\n"
            "#### 6. 🧘 Conquer Emotional Psychology & Avoid FOMO\n"
            "• Never chase a stock that has already surged 10% to 20% in recent sessions. The highest probability entry is always on an orderly pullback into key support.\n"
            "• Never engage in **revenge trading** after a loss. When emotional or shaken, close the terminal.\n\n"
            "#### 7. 📖 Maintain a Disciplined Trading Journal\n"
            "• Record every trade: entry price, stop-loss, target, technical catalyst, and emotional state. Review it weekly to eliminate recurring mistakes.\n\n"
            "---\n\n"
            "| Principle | Execution Blueprint | Strategic Benefit |\n"
            "| :--- | :--- | :--- |\n"
            "| **Capital Preservation** | Cap risk at 1-2% per setup | Prevents catastrophic drawdown |\n"
            "| **Stop-Loss Discipline** | Pre-set before trade execution | Eliminates emotional hesitation |\n"
            "| **Risk / Reward Ratio** | Target at least 1:2 or 1:3 | Mathematical positive expectancy |\n"
            "| **Trend Alignment** | Long above 50/200 EMA | Trades with institutional flow |\n"
            "| **Psychology** | Never chase extended candles | Avoids buying at local tops |\n\n"
            "---\n"
            "⚠️ *Disclaimer: Educational market guidance and quantitative risk principles. Always conduct independent research or consult a SEBI-registered financial advisor before investing.*"
        )


def format_market_overview_response(data: Dict[str, Any], lang: str) -> str:
    """Format market overview response in target language."""
    mood = data["overall_sentiment"]
    summary = data["sentiment_summary"]
    indices = data["indices"]

    if lang == "tanglish":
        lines = [
            f"**இன்னைக்கு Market Mood: {mood}**",
            f"{summary}\n",
            "**முக்கியமான Indices நிலவரம்:**"
        ]
        for idx in indices:
            icon = "🟢" if idx["change"] >= 0 else "🔴"
            lines.append(f"- **{idx['name']}**: {idx['currency_symbol']}{idx['current_price']:,.2f} ({idx['change_formatted']}) {icon} | Sentiment: {idx['sentiment']}")
        lines.append(f"\n*Market Status: {indices[0]['region']} market hours apply. Real-time updates active.*")
        return "\n".join(lines)

    elif lang == "ta":
        lines = [
            f"**இன்றைய சந்தை நிலவரம்: {mood}**",
            f"{summary}\n",
            "**முக்கிய குறியீடுகள் (Indices):**"
        ]
        for idx in indices:
            icon = "🟢" if idx["change"] >= 0 else "🔴"
            lines.append(f"- **{idx['name']}**: {idx['currency_symbol']}{idx['current_price']:,.2f} ({idx['change_formatted']}) {icon}")
        lines.append("\n*சந்தை தரவுகள் உடனுக்குடன் புதுப்பிக்கப்படுகின்றன.*")
        return "\n".join(lines)

    elif lang in ["hi", "hinglish"]:
        lines = [
            f"**आज का Market Sentiment: {mood}**",
            f"{summary}\n",
            "**प्रमुख Indices का हाल:**"
        ]
        for idx in indices:
            icon = "🟢" if idx["change"] >= 0 else "🔴"
            lines.append(f"- **{idx['name']}**: {idx['currency_symbol']}{idx['current_price']:,.2f} ({idx['change_formatted']}) {icon}")
        lines.append("\n*डेटा नवीनतम ट्रेडिंग सत्र के अनुसार है।*")
        return "\n".join(lines)

    else:
        # English
        lines = [
            f"### 🌐 Market Overview: {mood}",
            f"{summary}\n",
            "| Index | Last Price | Daily Change | Sentiment | 20D Volatility |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]
        for idx in indices:
            icon = "🟢" if idx["change"] >= 0 else "🔴"
            lines.append(f"| **{idx['name']}** | {idx['currency_symbol']}{idx['current_price']:,.2f} | {idx['change_formatted']} {icon} | {idx['sentiment']} | {idx['volatility_20d']:.1f}% |")
        lines.append("\n*Values reflect the latest available exchange trading data.*")
        return "\n".join(lines)


def format_stock_analysis_response(analysis: Dict[str, Any], intent: str, lang: str) -> str:
    """
    Format complete stock analysis response in the appropriate language and depth.
    """
    q = analysis["quote"]
    ind = analysis["indicators"]["latest"]
    sr = analysis["support_resistance"]
    st = analysis["statistics"]
    rk = analysis["risk"]
    pr = analysis["prediction"]
    sc = analysis["scenarios"]
    sg = analysis["strategy"]

    sym = q["symbol"]
    name = q["name"]
    curr = format_currency(q["current_price"], q["currency_symbol"])
    chg = format_percent(q["change_percent"])
    rsi = ind["rsi_14"]
    trend = ind["trend_bias"]
    risk = rk["risk_level"]
    target_5d = format_currency(pr["forecasts"]["5_day"]["target_price"], q["currency_symbol"])
    pred_dir = pr["direction"]
    conf = pr["confidence_score_pct"]
    sup = format_currency(sr["nearest_support"], q["currency_symbol"])
    res = format_currency(sr["nearest_resistance"], q["currency_symbol"])

    # 1. SPECIALIZED TARGETED RESPONSES FOR SPECIFIC INTENTS
    if intent == "STOCK_TIPS":
        return format_stock_tips_response(lang, analysis=analysis)

    if intent == "WHY_MOVE":
        if lang == "tanglish":
            return (
                f"**{name} ({sym}) சமீபத்திய விலை மாற்றத்திற்கான முக்கிய காரணங்கள்:**\n\n"
                f"• **Current Price:** {curr} ({chg})\n"
                f"• **RSI (Momentum):** {rsi:.1f} ({ind['rsi_signal']}) - {ind['rsi_desc']}\n"
                f"• **Moving Average Position:** Price தற்போது {ind['ma_summary']}.\n"
                f"• **Volume Activity:** Volume ratio {ind['volume_ratio']}x (average volume-ஐ விட {'அதிகம்' if ind['volume_ratio'] > 1.2 else 'சராசரி'})\n"
                f"• **Support & Resistance:** முக்கிய support {sup} மற்றும் resistance {res}.\n\n"
                f"**சுருக்கம்:** விலை இயக்கம் broad market sentiment மற்றும் technical indicator pullbacks ஆகியவற்றால் பாதிக்கப்படுகிறது."
            )
        elif lang == "ta":
            return (
                f"**{name} ({sym}) விலை மாற்றத்திற்கான காரணங்கள்:**\n\n"
                f"• **தற்போதைய விலை:** {curr} ({chg})\n"
                f"• **RSI அளவு:** {rsi:.1f} ({ind['rsi_signal']})\n"
                f"• **சந்தை போக்கு (Trend):** {trend}\n"
                f"• **ஆதரவு (Support):** {sup} | **தடைநிலை (Resistance):** {res}\n\n"
                f"விலை 20-நாள் மற்றும் 50-நாள் சராசரியுடன் தொடர்புடைய நகர்வுகளைக் காட்டுகிறது."
            )
        else:
            return (
                f"### Analysis: Why is {name} ({sym}) moving?\n\n"
                f"• **Current Price:** {curr} ({chg})\n"
                f"• **Momentum Driver:** RSI is currently at {rsi:.1f} ({ind['rsi_signal']}). {ind['rsi_desc']}\n"
                f"• **Moving Average Alignment:** Price is trading {ind['ma_summary']}.\n"
                f"• **Volume Profile:** Current volume is {ind['volume_ratio']:.1f}x the 20-day average, signaling {'elevated institutional turnover' if ind['volume_ratio'] > 1.5 else 'normal trading activity'}.\n"
                f"• **Key Levels:** Nearest support lies at {sup}, while primary resistance caps upside at {res}."
            )

    if intent == "STOCK_DIRECTION":
        if lang == "tanglish":
            return (
                f"**{name} ({sym}) Directional Outlook: {pred_dir} ({trend})**\n\n"
                f"• **Current Price:** {curr} ({chg})\n"
                f"• **Short-Term Bias:** {trend}\n"
                f"• **5-Day ML Target:** {target_5d} ({pr['forecasts']['5_day']['predicted_return_pct']:+.2f}%) [Calibrated Confidence: {conf}%]\n"
                f"• **Key Support:** {sup} | **Key Resistance:** {res}\n\n"
                f"Price {res}-க்கு மேல sustain ஆனா மேல போக நல்ல chance இருக்கு. ஆனால் {sup}-க்கு கீழே போனா short-term consolidation அல்லது pullback வரலாம்."
            )
        else:
            return (
                f"### Directional Outlook for {name} ({sym}): {pred_dir} ({trend})\n\n"
                f"• **Current Price:** {curr} ({chg})\n"
                f"• **Trend Structure:** {trend} (Price is {ind['ma_summary']})\n"
                f"• **5-Day ML Projected Target:** {target_5d} ({pr['forecasts']['5_day']['predicted_return_pct']:+.2f}%)\n"
                f"• **Model Confidence:** {conf}% (derived from walk-forward directional validation)\n"
                f"• **Support / Resistance:** Support at {sup}, Resistance at {res}.\n\n"
                f"**Assessment:** {sc['bullish']['condition']} for upside continuation; failure at {sup} invalidates the setup."
            )

    if intent == "BUY_SELL_QUERY":
        if lang == "tanglish":
            return (
                f"**{name} ({sym}) முதலீடு / வாங்குதல் குறித்த Technical Setup:**\n\n"
                f"• **Current Price:** {curr}\n"
                f"• **Model Bias:** {sg['overall_stance']}\n"
                f"• **Suggested Entry Zone:** {sg['entry_zone']}\n"
                f"• **Target Zone:** {sg['target_zone']}\n"
                f"• **Invalidation / Stop-loss Concept:** {format_currency(sg['invalidation_level'], q['currency_symbol'])}\n"
                f"• **Risk Level:** {risk} ({rk['risk_score']}/100)\n\n"
                f"⚠️ *முக்கிய குறிப்பு: இது கல்வி சார்ந்த Technical Analysis மட்டுமே. தனிப்பட்ட நிதி ஆலோசனை (Financial Advice) அல்ல.*"
            )
        else:
            return (
                f"### Strategy & Scenario Framework for {name} ({sym})\n\n"
                f"• **Current Price:** {curr} ({chg})\n"
                f"• **Structural Bias:** **{sg['overall_stance']}**\n"
                f"• **Potential Entry Zone:** {sg['entry_zone']}\n"
                f"• **Primary Target Range:** {sg['target_zone']}\n"
                f"• **Invalidation / Stop-Loss Concept:** {format_currency(sg['invalidation_level'], q['currency_symbol'])}\n"
                f"• **Risk-to-Reward Estimate:** {sg['risk_reward_ratio']}\n"
                f"• **Risk Level:** {risk} ({rk['summary']})\n\n"
                f"⚠️ *Disclaimer: {sg['disclaimer']}*"
            )

    # 2. DEFAULT BEGINNER-FRIENDLY STOCK ANALYSIS (Concise & simple by default)
    if intent != "STOCK_ANALYSIS_DETAILED":
        if "bull" in trend.lower():
            trend_badge = "Bullish"
            trend_icon = "🟢"
            exp_en = "Buyers are actively driving the price upwards and it is holding above key moving averages."
            exp_tang = "பங்கில் buyers அதிகமா இருக்காங்க, விலை மேல்நோக்கி நகர்ந்து வருது."
            exp_ta = "வாங்குபவர்களின் ஆதிக்கம் அதிகமாக உள்ளது, பங்கு விலை உயர்ந்து வருகிறது."
            exp_hi = "बाजार में खरीदार सक्रिय हैं और शेयर की कीमत ऊपर की ओर बढ़ रही है।"
        elif "bear" in trend.lower():
            trend_badge = "Bearish"
            trend_icon = "🔴"
            exp_en = "Selling pressure has been outweighing buyers, pushing prices lower in recent sessions."
            exp_tang = "விற்பனையாளர்கள் அழுத்தம் அதிகமா இருக்கு, சமீபத்திய நாட்களில் விலை கீழ்நோக்கி போகுது."
            exp_ta = "விற்பனை அழுத்தம் காரணமாக பங்கு விலை கீழ்நோக்கி நகர்கிறது."
            exp_hi = "बिकवाली का दबाव बना हुआ है और शेयर हाल के दिनों में नीचे आ रहा है।"
        else:
            trend_badge = "Neutral"
            trend_icon = "⚪"
            exp_en = "Price is moving sideways in a steady range without a clear breakout yet."
            exp_tang = "தெளிவான ஏற்ற இறக்கம் இல்லாம ஒரு குறிப்பிட்ட ரேஞ்சுக்குள்ளேயே சுத்திட்டு இருக்கு."
            exp_ta = "குறிப்பிட்ட வரம்பிற்குள் விலை வர்த்தகமாகி வருகிறது, பெரிய மாற்றம் இன்னும் ஏற்படவில்லை."
            exp_hi = "शेयर एक दायरे में घूम रहा है, अभी कोई स्पष्ट दिशा तय नहीं हुई है।"

        risk_exp_en = "Gentle swings and steady historical movement." if risk == "Low" else "Moderate price swings typical of large-cap companies." if risk == "Medium" else "Higher volatility with wider daily price fluctuations."
        risk_exp_tang = "குறைவான ஏற்ற இறக்கம், நிலையான இயக்கம்." if risk == "Low" else "மிதமான ஏற்ற இறக்கம்." if risk == "Medium" else "அதிக ஏற்ற இறக்கம், கூடுதல் கவனம் தேவை."
        risk_exp_ta = "குறைந்த ஏற்ற இறக்கம்." if risk == "Low" else "மிதமான ஏற்ற இறக்கம்." if risk == "Medium" else "அதிக ஏற்ற இறக்கம், எச்சரிக்கை தேவை."
        risk_exp_hi = "कम उतार-चढ़ाव और स्थिर चाल।" if risk == "Low" else "मध्यम उतार-चढ़ाव।" if risk == "Medium" else "अधिक उतार-चढ़ाव, सतर्कता आवश्यक।"

        if lang == "tanglish":
            return (
                f"### 📊 {name} ({sym}) எளிய பார்வை\n\n"
                f"• **Current Price:** **{curr}** ({chg})\n"
                f"• **Trend:** {trend_icon} **{trend_badge}** — {exp_tang}\n"
                f"• **Key Levels (முக்கிய நிலைகள்):**\n"
                f"  - **Support (Floor):** **{sup}** *(விலை இறங்கினால் இந்த இடத்தில் தாங்கி நிற்க வாய்ப்புள்ளது)*\n"
                f"  - **Resistance (Ceiling):** **{res}** *(விலை ஏறும்போது இந்த இடத்தில் தற்காலிக தடை வரலாம்)*\n"
                f"• **Risk Level:** **{risk}** ({risk_exp_tang})\n\n"
                f"**எளிய சுருக்கம் (Summary):**\n"
                f"{name} பங்கு தற்போது {trend_badge.lower()} போக்கில் வர்த்தகமாகிறது. "
                f"பங்கு விலை {sup} support-க்கு மேல இருக்கும் வரை நிலைத்தன்மை இருக்கும். "
                f"RSI momentum அளவு {rsi:.1f}-ல் உள்ளது.\n\n"
                f"💡 *Technical indicators (RSI, Moving Averages) மற்றும் AI கணிப்புகளை விரிவாக பார்க்க விரும்பினால் 'Explain in detail' என்று கேட்கலாம்!*\n\n"
                f"---\n"
                f"⚠️ *முக்கிய குறிப்பு: இது கல்வி சார்ந்த தகவல்களுக்கு மட்டுமே. தனிப்பட்ட நிதி ஆலோசனை (Financial Advice) அல்ல. முதலீடு செய்வதற்கு முன் உங்கள் சொந்த ஆய்வை மேற்கொள்ளவும்.*"
            )
        elif lang == "ta":
            return (
                f"### 📊 {name} ({sym}) எளிய ஆய்வு\n\n"
                f"• **தற்போதைய விலை:** **{curr}** ({chg})\n"
                f"• **சந்தை போக்கு (Trend):** {trend_icon} **{trend_badge}** — {exp_ta}\n"
                f"• **முக்கிய நிலைகள் (Key Levels):**\n"
                f"  - **ஆதரவு நிலை (Support):** **{sup}** *(விலை இறங்கினால் தாங்கும் தளம்)*\n"
                f"  - **தடை நிலை (Resistance):** **{res}** *(விலை உயரும் போது விற்பனை அழுத்தம் ஏற்படும் கூரை)*\n"
                f"• **இடர் அளவு (Risk Level):** **{risk}** ({risk_exp_ta})\n\n"
                f"**சுருக்கம்:**\n"
                f"{name} பங்கு தற்போது {trend_badge} போக்கில் வர்த்தகமாகிறது. முக்கிய ஆதரவு நிலை {sup} ஆகும்.\n\n"
                f"💡 *விரிவான குறிகாட்டிகள் மற்றும் AI கணிப்புகளை அறிய 'விரிவான விளக்கம்' (more details) என கேட்கலாம்!*\n\n"
                f"---\n"
                f"⚠️ *மறுப்பு: இது கல்வி மற்றும் தகவல் நோக்கங்களுக்காக மட்டுமே, நிதி ஆலோசனை அல்ல. முதலீடு செய்வதற்கு முன் உங்கள் சொந்த ஆய்வை மேற்கொள்ளவும்.*"
            )
        elif lang in ["hi", "hinglish"]:
            return (
                f"### 📊 {name} ({sym}) का संक्षिप्त विवरण\n\n"
                f"• **करंट प्राइस (Current Price):** **{curr}** ({chg})\n"
                f"• **ट्रेंड (Trend):** {trend_icon} **{trend_badge}** — {exp_hi}\n"
                f"• **की लेवल्स (Key Levels):**\n"
                f"  - **सपोर्ट (Support):** **{sup}** *(जहाँ से गिरता भाव संभल सकता है)*\n"
                f"  - **रेजिस्टेंस (Resistance):** **{res}** *(जहाँ बढ़ते भाव में रुकावट आ सकती है)*\n"
                f"• **रिस्क लेवल (Risk Level):** **{risk}** ({risk_exp_hi})\n\n"
                f"**सरल सारांश (Summary for Beginners):**\n"
                f"{name} का शेयर अभी {trend_badge} स्थिति में है। जब तक शेयर {sup} के ऊपर बना हुआ है, तब तक स्थिरता रहने की संभावना है।\n\n"
                f"💡 *और गहराई से इंडिकेटर्स और भविष्य के अनुमान समझने के लिए 'more details' लिखकर पूछें!*\n\n"
                f"---\n"
                f"⚠️ *अस्वीकरण: यह केवल शैक्षणिक और सूचनात्मक उद्देश्यों के लिए है, वित्तीय सलाह नहीं। निवेश करने से पहले अपना शोध स्वयं करें।*"
            )
        else:
            return (
                f"### 📊 {name} ({sym}) Overview\n\n"
                f"• **Current Price:** **{curr}** ({chg})\n"
                f"• **Trend:** {trend_icon} **{trend_badge}** — {exp_en}\n"
                f"• **Key Levels:**\n"
                f"  - **Support (Floor):** **{sup}** *(Where buyers typically step in to prevent further drops)*\n"
                f"  - **Resistance (Ceiling):** **{res}** *(Where selling pressure often slows further gains)*\n"
                f"• **Risk Level:** **{risk}** ({risk_exp_en})\n\n"
                f"**Summary for Beginners:**\n"
                f"{name} is currently showing a {trend_badge.lower()} pattern. As long as it holds above its {sup} support level, the baseline remains stable. Its momentum gauge (RSI) is currently at {rsi:.1f}.\n\n"
                f"💡 *Want deeper details with technical indicators, multi-day forecasts, and scenarios? Just ask: 'Explain {sym} in detail'!*"
                f"\n\n---\n"
                f"⚠️ *Disclaimer: This analysis is for educational and informational purposes only and does not constitute financial advice. Always do your own research before investing.*"
            )

    # 3. FULL COMPREHENSIVE MULTILINGUAL ANALYSIS (When requested in detail)
    if lang == "tanglish":
        return f"""**{name} ({sym}) முழுமையான ஆய்வு அறிக்கை (Complete Analysis)**

**1. விரைவு பதில் (Quick Summary):**
{name} தற்போது short-term **{trend}** momentum காட்டுகிறது.

• **Current Price:** {curr} ({chg})
• **52-Week Range:** {format_currency(q['52_week_low'], q['currency_symbol'])} - {format_currency(q['52_week_high'], q['currency_symbol'])}
• **RSI (14):** {rsi:.1f} ({ind['rsi_signal']})
• **Trend:** {trend}
• **Risk Rating:** {risk} (Score: {rk['risk_score']}/100)

---

**2. தொழில்நுட்ப குறிகாட்டிகள் (Technical Indicators):**
• **Moving Averages:** Price தற்போது {ind['ma_summary']}.
• **RSI:** {ind['rsi_desc']}
• **MACD:** {ind['macd_desc']}
• **Bollinger Bands:** Upper band {format_currency(ind['bollinger_upper'], q['currency_symbol'])}, Lower band {format_currency(ind['bollinger_lower'], q['currency_symbol'])}.

---

**3. முக்கிய நிலைகள் (Support & Resistance):**
• **Primary Support:** {sup} (விலை இறங்கினால் தாங்கும் பகுதி)
• **Primary Resistance:** {res} (விலை உயர தடையாக இருக்கும் பகுதி)
• **Breakout Zone:** {sr['breakout_zone']}

---

**4. இடர் ஆய்வு (Risk Analysis):**
• **Risk Level:** {risk}
• **காரணம்:** {rk['explanation']}
• **Max Drawdown:** {st['max_drawdown_pct']:.1f}%

---

**5. AI / ML விலை கணிப்பு (Model Prediction):**
• **திசை (Direction):** {pred_dir}
• **Next Session (1D):** {format_currency(pr['forecasts']['1_day']['target_price'], q['currency_symbol'])} ({pr['forecasts']['1_day']['predicted_return_pct']:+.2f}%)
• **5-Day Target:** {target_5d} ({pr['forecasts']['5_day']['predicted_return_pct']:+.2f}%)
• **1-Month Target:** {format_currency(pr['forecasts']['21_day']['target_price'], q['currency_symbol'])} ({pr['forecasts']['21_day']['predicted_return_pct']:+.2f}%)
• **Calibrated Confidence:** {conf}% (Historical walk-forward testing அடிப்படையில் கணக்கிடப்பட்டது).

---

**6. சந்தை சூழ்நிலைகள் (Market Scenarios):**
• 🟢 **Bullish Scenario:** {sc['bullish']['condition']}, இலக்கு: {sc['bullish']['target_zone']}
• ⚪ **Neutral Scenario:** {sc['neutral']['condition']} ({sc['neutral']['action']})
• 🔴 **Bearish Scenario:** {sc['bearish']['condition']}, ஆபத்து நிலை: {sc['bearish']['target_zone']}

---

**7. முடிவுரை (Conclusion):**
{name} பங்கு தற்போது {trend.lower()} நிலையில் உள்ளது. RSI மற்றும் support நிலைகளை கவனித்து முடிவெடுப்பது நல்லது."""

    elif lang == "ta":
        return f"""**{name} ({sym}) விரிவான பங்கு ஆய்வு**

**1. முக்கிய விவரங்கள்:**
• **தற்போதைய விலை:** {curr} ({chg})
• **RSI குறியீடு:** {rsi:.1f} ({ind['rsi_signal']})
• **சந்தை போக்கு:** {trend}
• **இடர் நிலை (Risk):** {risk}

**2. ஆதரவு & தடைநிலைகள்:**
• **ஆதரவு (Support):** {sup}
• **தடைநிலை (Resistance):** {res}

**3. AI மாதிரி கணிப்பு (ML Forecast):**
• **எதிர்பார்க்கப்படும் திசை:** {pred_dir}
• **5-நாள் இலக்கு:** {target_5d} ({pr['forecasts']['5_day']['predicted_return_pct']:+.2f}%)
• **நம்பகத்தன்மை (Confidence):** {conf}%

**4. சூழ்நிலைகள் (Scenarios):**
• **ஏற்ற நிலை:** {sc['bullish']['condition']}
• **இறக்க நிலை:** {sc['bearish']['condition']}

*குறிப்பு: இந்த தகவல் மாதிரி அடிப்படையிலானது, உறுதிசெய்யப்பட்ட நிதி ஆலோசனை அல்ல.*"""

    elif lang in ["hi", "hinglish"]:
        return f"""**{name} ({sym}) का संपूर्ण विश्लेषण**

**1. वर्तमान स्थिति (Current Status):**
• **Current Price:** {curr} ({chg})
• **RSI (14):** {rsi:.1f} ({ind['rsi_signal']})
• **Trend:** {trend}
• **Risk Level:** {risk} (Score {rk['risk_score']}/100)

**2. सपोर्ट और रेजिस्टेंस (Key Levels):**
• **Support:** {sup}
• **Resistance:** {res}

**3. AI / ML प्रेडिक्शन:**
• **दिशा (Direction):** {pred_dir}
• **5-Day Projected Price:** {target_5d} ({pr['forecasts']['5_day']['predicted_return_pct']:+.2f}%)
• **Calibrated Confidence:** {conf}%

**4. मार्केट परिदृश्य (Scenarios):**
• **Bullish:** {sc['bullish']['condition']} (Target: {sc['bullish']['target_zone']})
• **Bearish:** {sc['bearish']['condition']}

*चेतावनी: यह केवल शैक्षणिक उद्देश्य के लिए है, व्यक्तिगत वित्तीय सलाह नहीं है।*"""

    else:
        # Standard Professional English Response
        return f"""### 📊 Analysis for {name} ({sym})

#### 1. Quick Summary
**{name}** is currently demonstrating a **{trend}** technical structure trading at **{curr}** ({chg}).

| Metric | Value | Reference / Status |
| :--- | :--- | :--- |
| **Current Price** | {curr} | Last available trade |
| **Daily Change** | {chg} | Intraday performance |
| **52-Week Range** | {format_currency(q['52_week_low'], q['currency_symbol'])} - {format_currency(q['52_week_high'], q['currency_symbol'])} | Annual boundaries |
| **RSI (14)** | {rsi:.1f} | {ind['rsi_signal']} |
| **Primary Trend** | {trend} | Price is {ind['ma_summary']} |
| **Risk Rating** | **{risk}** | Score: {rk['risk_score']}/100 |

---

#### 2. Technical Indicators
- **Moving Averages:** Price is currently {ind['ma_summary']}.
- **RSI (14):** {ind['rsi_desc']}
- **MACD:** {ind['macd_desc']}
- **Bollinger Bands:** Upper band at {format_currency(ind['bollinger_upper'], q['currency_symbol'])}, Lower band at {format_currency(ind['bollinger_lower'], q['currency_symbol'])} (Bandwidth: {ind['bollinger_bandwidth_pct']:.1f}%).
- **Average True Range (ATR):** {format_currency(ind['atr_14'], q['currency_symbol'])} ({ind['atr_percent']:.1f}% daily volatility).

---

#### 3. Support & Resistance Levels
- **Nearest Support:** **{sup}** (Secondary: {format_currency(sr['secondary_support'], q['currency_symbol'])})
- **Nearest Resistance:** **{res}** (Secondary: {format_currency(sr['secondary_resistance'], q['currency_symbol'])})
- **Breakout Trigger:** {sr['breakout_zone']}
- **Breakdown Trigger:** {sr['breakdown_zone']}

---

#### 4. Multi-Factor Risk Assessment
- **Risk Level:** **{risk}**
- **Evaluation:** {rk['explanation']}
- **Historical Max Drawdown:** {st['max_drawdown_pct']:.1f}%
- **Market Beta:** {st['beta']:.2f}

---

#### 5. AI / ML Prediction & Horizon Forecasts
- **Model Direction:** **{pred_dir}** ({pr['trend_label']})
- **Calibrated Confidence:** **{conf}%** (*derived from TimeSeriesSplit out-of-fold directional accuracy*)
- **1-Day Forecast:** {format_currency(pr['forecasts']['1_day']['target_price'], q['currency_symbol'])} ({pr['forecasts']['1_day']['predicted_return_pct']:+.2f}%)
- **5-Day Forecast:** **{target_5d}** ({pr['forecasts']['5_day']['predicted_return_pct']:+.2f}%)
- **21-Day Forecast:** {format_currency(pr['forecasts']['21_day']['target_price'], q['currency_symbol'])} ({pr['forecasts']['21_day']['predicted_return_pct']:+.2f}%)

*Uncertainty note: Model projections represent statistical distribution cones and are subject to real-time market shifts.*

---

#### 6. Actionable Market Scenarios
- 🟢 **Bullish Scenario:** {sc['bullish']['condition']}, with potential upside into {sc['bullish']['target_zone']}.
- ⚪ **Neutral Scenario:** {sc['neutral']['condition']}. {sc['neutral']['action']}.
- 🔴 **Bearish Scenario:** {sc['bearish']['condition']}, increasing downside risk toward {sc['bearish']['target_zone']}.

---

#### 7. Educational Setup & Conclusion
- **Model Stance:** **{sg['overall_stance']}**
- **Entry Zone Concept:** {sg['entry_zone']}
- **Invalidation Level:** {format_currency(sg['invalidation_level'], q['currency_symbol'])}
- **Risk/Reward Profile:** {sg['risk_reward_ratio']}

*Disclaimer: {sg['disclaimer']}*"""


def format_comparison_response(comp: Dict[str, Any], lang: str) -> str:
    """Format side-by-side stock comparison in requested language."""
    a = comp["stock_a"]
    b = comp["stock_b"]

    if lang == "tanglish":
        return f"""**{a['name']} ({a['symbol']}) vs {b['name']} ({b['symbol']}) ஒப்பீடு (Comparison):**

| Metric | {a['symbol']} | {b['symbol']} |
| :--- | :--- | :--- |
| **Current Price** | {a['currency_symbol']}{a['price']:,.2f} | {b['currency_symbol']}{b['price']:,.2f} |
| **Today's Change** | {a['change_pct']:+.2f}% | {b['change_pct']:+.2f}% |
| **1-Year Return** | {a['return_1y']:+.2f}% | {b['return_1y']:+.2f}% |
| **Volatility (Annual)**| {a['volatility']:.1f}% | {b['volatility']:.1f}% |
| **Max Drawdown** | {a['max_drawdown']:.1f}% | {b['max_drawdown']:.1f}% |
| **Sharpe Ratio** | {a['sharpe']:.2f} | {b['sharpe']:.2f} |
| **RSI (14)** | {a['rsi']:.1f} | {b['rsi']:.1f} |
| **Trend** | {a['trend']} | {b['trend']} |
| **Risk Level** | {a['risk_level']} | {b['risk_level']} |
| **Market Cap** | {a['market_cap']} | {b['market_cap']} |

**முடிவுரை (Summary):**
இரு பங்குகளையும் ஒப்பிடும் போது, {'1-year return-ல் ' + a['symbol'] if a['return_1y'] > b['return_1y'] else '1-year return-ல் ' + b['symbol']} முன்னிலையில் உள்ளது. இடர் மேலாண்மையில் (lower volatility) {' ' + a['symbol'] if a['volatility'] < b['volatility'] else ' ' + b['symbol']} அதிக நிலைத்தன்மை காட்டுகிறது."""

    else:
        return f"""### ⚖️ Stock Comparison: {a['name']} ({a['symbol']}) vs {b['name']} ({b['symbol']})

| Performance & Risk Metric | {a['symbol']} | {b['symbol']} | Leader |
| :--- | :--- | :--- | :--- |
| **Current Price** | {a['currency_symbol']}{a['price']:,.2f} | {b['currency_symbol']}{b['price']:,.2f} | - |
| **Daily Change** | {a['change_pct']:+.2f}% | {b['change_pct']:+.2f}% | {a['symbol'] if a['change_pct'] > b['change_pct'] else b['symbol']} |
| **1-Year Return** | {a['return_1y']:+.2f}% | {b['return_1y']:+.2f}% | {a['symbol'] if a['return_1y'] > b['return_1y'] else b['symbol']} |
| **Annualized Volatility** | {a['volatility']:.1f}% | {b['volatility']:.1f}% | {a['symbol'] if a['volatility'] < b['volatility'] else b['symbol']} (Lower risk) |
| **Max Drawdown** | {a['max_drawdown']:.1f}% | {b['max_drawdown']:.1f}% | {a['symbol'] if a['max_drawdown'] > b['max_drawdown'] else b['symbol']} |
| **Sharpe Ratio** | {a['sharpe']:.2f} | {b['sharpe']:.2f} | {a['symbol'] if a['sharpe'] > b['sharpe'] else b['symbol']} |
| **RSI (14)** | {a['rsi']:.1f} | {b['rsi']:.1f} | - |
| **Technical Trend** | {a['trend']} | {b['trend']} | - |
| **Risk Category** | {a['risk_level']} | {b['risk_level']} | - |
| **Market Capitalization** | {a['market_cap']} | {b['market_cap']} | - |

**Key Takeaways:**
- **Momentum & Returns:** {'**' + a['symbol'] + '** has outperformed over the past 12 months with ' + f'{a["return_1y"]:+.2f}%' if a['return_1y'] > b['return_1y'] else '**' + b['symbol'] + '** has outperformed over the past 12 months with ' + f'{b["return_1y"]:+.2f}%'}.
- **Risk-Adjusted Performance:** {'**' + a['symbol'] + '** provides superior risk-adjusted returns (Sharpe ' + f'{a["sharpe"]:.2f})' if a['sharpe'] > b['sharpe'] else '**' + b['symbol'] + '** provides superior risk-adjusted returns (Sharpe ' + f'{b["sharpe"]:.2f})'}.
- **Volatility Profile:** {'**' + a['symbol'] + '** trades with lower volatility (' + f'{a["volatility"]:.1f}%)' if a['volatility'] < b['volatility'] else '**' + b['symbol'] + '** trades with lower volatility (' + f'{b["volatility"]:.1f}%)'}."""
