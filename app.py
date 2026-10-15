"""
StockMind AI — Browser-Based Web Application (Gradio Interface)
Provides a ChatGPT/Claude-inspired conversational interface coupled with
real-time quantitative analytics, multi-horizon ML predictions, interactive
Plotly technical charts, and multilingual natural language understanding.
"""

import os
import sys
import socket
import traceback
from typing import Dict, Any, List, Tuple, Optional

# Ensure workspace root is in sys.path
WORKSPACE_ROOT = os.path.dirname(os.path.abspath(__file__))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

# Fix Windows console UTF-8 output if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Safe .env loader (0 external dependencies)
def load_dotenv_safely(env_path: str = os.path.join(WORKSPACE_ROOT, ".env")):
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

load_dotenv_safely()

import gradio as gr
import plotly.graph_objects as go

# Connect directly to existing backend modules
from ai.language import detect_language
from ai.intent import classify_intent
from ai.assistant import (
    format_market_overview_response,
    format_stock_analysis_response,
    format_comparison_response,
    generate_comparison_analysis,
    format_conversational_response,
    format_stock_tips_response,
    format_currency_conversion_response
)
from data.global_market_data import get_market_overview
from data.market_data import resolve_ticker
from data.companies import get_all_companies
from model.live_signal import run_complete_stock_analysis
from main import app  # Expose FastAPI app instance for 'uvicorn app:app' compatibility
from ui.plot_charts import (
    create_candlestick_figure,
    create_prediction_figure,
    create_oscillators_figure,
    create_comparison_figure,
    create_empty_figure,
    build_cards_html,
    build_strategy_markdown,
    build_comparison_markdown
)

# Custom High-End CSS for Institutional Dark Theme
CUSTOM_CSS = """
/* StockMind AI Custom Theme Enhancements */
body, .gradio-container {
    background-color: #0B0F19 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: #F8FAFC !important;
}

/* Header container */
.header-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
}

.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(37, 99, 235, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #60A5FA;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 9999px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.main-title {
    font-size: 26px;
    font-weight: 800;
    color: #FFFFFF;
    margin: 4px 0 6px 0;
    letter-spacing: -0.02em;
}

.sub-title {
    font-size: 14px;
    color: #94A3B8;
    margin: 0;
    line-height: 1.5;
}

/* Suggestion Pills */
.suggestion-pill {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    color: #CBD5E1 !important;
    border-radius: 9999px !important;
    font-size: 12px !important;
    padding: 6px 14px !important;
    transition: all 0.2s ease !important;
}
.suggestion-pill:hover {
    background: #2563EB !important;
    border-color: #3B82F6 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

/* Chat container */
.chat-wrapper {
    border-radius: 14px;
    overflow: hidden;
}

/* Buttons */
.primary-btn {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
}
.primary-btn:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
}

/* Tab borders and styling */
.tab-nav {
    border-bottom: 1px solid #334155 !important;
}
"""

def find_available_port(preferred_port: int = 7860, host: str = "127.0.0.1", max_tries: int = 30) -> int:
    """Finds an open port starting from preferred_port without crashing."""
    for p in range(preferred_port, preferred_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, p))
                return p
        except OSError:
            continue
    return preferred_port


def initial_stock_state(default_symbol: str = "TCS.NS") -> Tuple[Any, Any, Any, Any, str, str]:
    """Pre-generates initial graphs and cards for instant fast startup."""
    try:
        resolved = resolve_ticker(default_symbol)
        analysis = run_complete_stock_analysis(resolved, period="1y")
        q = analysis["quote"]
        sym_name = q.get("name", default_symbol)
        curr = q.get("currency_symbol", "₹")

        fig_candle = create_candlestick_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
        fig_pred = create_prediction_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
        fig_osc = create_oscillators_figure(analysis["chart_payload"], symbol_name=sym_name)
        fig_comp = create_empty_figure("Ask 'Compare TCS and Infosys' to display head-to-head comparison graph.")
        cards_html = build_cards_html(analysis)
        strategy_md = build_strategy_markdown(analysis)
        comparison_md = build_comparison_markdown(None)
        return fig_candle, fig_pred, fig_osc, fig_comp, cards_html, strategy_md, comparison_md
    except Exception as e:
        empty_fig = create_empty_figure("Enter a stock query to display charts.")
        cards_html = build_cards_html(None)
        strategy_md = build_strategy_markdown(None)
        comparison_md = build_comparison_markdown(None)
        return empty_fig, empty_fig, empty_fig, empty_fig, cards_html, strategy_md, comparison_md


def handle_chat_and_analysis(
    user_message: str,
    chat_history: List[Dict[str, str]],
    active_symbol_state: str,
    current_fig_candle: Any,
    current_fig_pred: Any,
    current_fig_osc: Any,
    current_fig_comp: Any,
    current_cards_html: str,
    current_strategy_md: str,
    current_comp_md: str
):
    """
    Main Conversational Assistant & Quantitative Visual Engine Handler:
    1. Validates input
    2. Detects language (English, Tamil, Tanglish, Hindi)
    3. Classifies intent & extracts ticker entities
    4. Connects to existing backend modules
    5. Returns conversational narrative + updates all interactive graphs & dashboard cards
    """
    query = (user_message or "").strip()
    if not query:
        return (
            chat_history,
            "",
            active_symbol_state,
            current_cards_html,
            current_fig_candle,
            current_fig_pred,
            current_fig_osc,
            current_fig_comp,
            current_strategy_md,
            current_comp_md
        )

    # Initialize chat history as list
    history = list(chat_history) if chat_history else []

    try:
        # 1. Detect language
        lang = detect_language(query)

        # 2. Intent classification & entity extraction
        active_sym = active_symbol_state or "TCS.NS"
        parsed = classify_intent(query, active_symbol=active_sym)
        intent = parsed.get("intent", "STOCK_ANALYSIS")
        primary_sym = parsed.get("primary_symbol") or active_sym
        secondary_sym = parsed.get("secondary_symbol")
        tf = parsed.get("timeframe") or "1y"

        # Defaults for UI outputs if not modified by this query
        new_active_sym = active_sym
        new_cards_html = current_cards_html
        new_fig_candle = current_fig_candle
        new_fig_pred = current_fig_pred
        new_fig_osc = current_fig_osc
        new_fig_comp = current_fig_comp
        new_strategy_md = current_strategy_md
        new_comp_md = current_comp_md
        assistant_reply = ""

        # 3. Conversational / Greetings / General Intent
        if intent in ["GENERAL_GREETING", "GENERAL_HOW_ARE_YOU", "GENERAL_CAPABILITIES", "GENERAL_OFF_TOPIC", "GENERAL_CONVERSATION"] and not parsed.get("symbols"):
            assistant_reply = format_conversational_response(intent, lang)

        # 4. Currency Conversion Intent (e.g. Dollar to Indian Rupees / Foreign stock in INR)
        elif intent == "CURRENCY_CONVERSION":
            resolved = resolve_ticker(primary_sym)
            analysis = run_complete_stock_analysis(resolved, period=tf)
            assistant_reply = format_currency_conversion_response(analysis, lang=lang)

            # Update active stock & visuals
            new_active_sym = resolved
            q = analysis["quote"]
            sym_name = q.get("name", resolved)
            curr = q.get("currency_symbol", "₹")
            new_cards_html = build_cards_html(analysis)
            new_fig_candle = create_candlestick_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
            new_fig_pred = create_prediction_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
            new_fig_osc = create_oscillators_figure(analysis["chart_payload"], symbol_name=sym_name)
            new_strategy_md = build_strategy_markdown(analysis)

        # 5. Stock Tips Intent
        elif intent == "STOCK_TIPS":
            if not parsed.get("primary_symbol"):
                assistant_reply = format_stock_tips_response(lang=lang)
            else:
                try:
                    resolved = resolve_ticker(primary_sym)
                    analysis = run_complete_stock_analysis(resolved, period=tf)
                    assistant_reply = format_stock_tips_response(lang=lang, analysis=analysis)
                    # Update active stock & visuals
                    new_active_sym = resolved
                    q = analysis["quote"]
                    sym_name = q.get("name", resolved)
                    curr = q.get("currency_symbol", "₹")
                    new_cards_html = build_cards_html(analysis)
                    new_fig_candle = create_candlestick_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
                    new_fig_pred = create_prediction_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
                    new_fig_osc = create_oscillators_figure(analysis["chart_payload"], symbol_name=sym_name)
                    new_strategy_md = build_strategy_markdown(analysis)
                except Exception:
                    assistant_reply = format_stock_tips_response(lang=lang)

        # 5. Market Overview Intent
        elif intent == "MARKET_OVERVIEW":
            overview = get_market_overview()
            assistant_reply = format_market_overview_response(overview, lang)

        # 6. Stock Comparison Intent
        elif intent == "STOCK_COMPARISON":
            if not secondary_sym:
                secondary_sym = "INFY.NS" if "TCS" in primary_sym else "TCS.NS"

            comp_data = generate_comparison_analysis(primary_sym, secondary_sym, timeframe=tf)
            assistant_reply = format_comparison_response(comp_data, lang)
            new_fig_comp = create_comparison_figure(comp_data)
            new_comp_md = build_comparison_markdown(comp_data)

        # 7. Single Stock Analysis (All stock queries: prediction, direction, fundamentals, why move, etc.)
        else:
            resolved = resolve_ticker(primary_sym)
            analysis = run_complete_stock_analysis(resolved, period=tf)
            assistant_reply = format_stock_analysis_response(analysis, intent, lang)

            # Update charts and cards
            new_active_sym = resolved
            q = analysis["quote"]
            sym_name = q.get("name", resolved)
            curr = q.get("currency_symbol", "₹")

            new_cards_html = build_cards_html(analysis)
            new_fig_candle = create_candlestick_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
            new_fig_pred = create_prediction_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
            new_fig_osc = create_oscillators_figure(analysis["chart_payload"], symbol_name=sym_name)
            new_strategy_md = build_strategy_markdown(analysis)

        # Append turn to history
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": assistant_reply})

        return (
            history,
            "",
            new_active_sym,
            new_cards_html,
            new_fig_candle,
            new_fig_pred,
            new_fig_osc,
            new_fig_comp,
            new_strategy_md,
            new_comp_md
        )

    except Exception as e:
        # Technical debug in terminal
        print(f"[StockMind Error] Failed processing query '{query}':", file=sys.stderr)
        traceback.print_exc()

        # User-friendly message in UI
        clean_err = str(e)
        if "No data found" in clean_err or "Invalid ticker" in clean_err:
            friendly_msg = f"⚠️ Could not find market data for **'{query}'**. Please check if the ticker symbol or company name is correct (e.g. *TCS*, *Reliance*, *Infosys*, *Apple*, *Tesla*)."
        elif "rate limit" in clean_err.lower():
            friendly_msg = "⚠️ Market data rate limit temporarily reached. Please wait a few seconds and try again."
        else:
            friendly_msg = f"⚠️ Unable to analyze **'{query}'**: {clean_err}. Please verify the symbol or try another query."

        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": friendly_msg})

        return (
            history,
            "",
            active_symbol_state,
            current_cards_html,
            current_fig_candle,
            current_fig_pred,
            current_fig_osc,
            current_fig_comp,
            current_strategy_md,
            current_comp_md
        )


def build_app() -> gr.Blocks:
    """Builds and wires the complete StockMind AI Gradio application."""
    initial_candle, initial_pred, initial_osc, initial_comp, initial_cards, initial_strat, initial_comp_md = initial_stock_state("TCS.NS")

    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
    )

    with gr.Blocks(title="StockMind AI - Financial Intelligence & ML Predictions") as demo:
        # Active Symbol State
        active_symbol_state = gr.State("TCS.NS")

        # Header & Branding
        with gr.Row():
            with gr.Column(elem_classes=["header-box"]):
                gr.HTML("""
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                    <div>
                        <div class="brand-badge">⚡ Real-time Analytics &bull; Calibrated ML Trajectory &bull; Multilingual</div>
                        <h1 class="main-title">How can I help you?</h1>
                        <p class="sub-title">Analyze stocks, understand markets, compare companies, or just ask in English, Tamil, Tanglish, or Hindi.</p>
                    </div>
                    <div style="text-align: right; background: rgba(15, 23, 42, 0.6); padding: 8px 16px; border-radius: 10px; border: 1px solid #334155;">
                        <span style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 600;">System Status</span>
                        <div style="font-size: 13px; font-weight: 700; color: #10B981; display: flex; align-items: center; justify-content: flex-end; gap: 6px;">
                            <span style="width: 8px; height: 8px; background: #10B981; border-radius: 50%; display: inline-block;"></span>
                            Live Engine Active
                        </div>
                    </div>
                </div>
                """)

        # Suggestion Prompts / Quick Action Pills
        with gr.Row():
            pill_tcs = gr.Button("📈 Analyze TCS", elem_classes=["suggestion-pill"], size="sm")
            pill_comp = gr.Button("⚔️ Compare TCS and Infosys", elem_classes=["suggestion-pill"], size="sm")
            pill_market = gr.Button("🌐 Market Pulse (Nifty / Global)", elem_classes=["suggestion-pill"], size="sm")
            pill_apple = gr.Button("🔮 Apple Stock Prediction", elem_classes=["suggestion-pill"], size="sm")
            pill_tanglish = gr.Button("🗣️ Reliance stock epdi iruku?", elem_classes=["suggestion-pill"], size="sm")
            pill_tips = gr.Button("💡 Trading Rules & Tips", elem_classes=["suggestion-pill"], size="sm")

        # Main Workspace: 2-Column Responsive Layout
        with gr.Row():
            # LEFT COLUMN: Conversational AI Assistant
            with gr.Column(scale=5, elem_classes=["chat-wrapper"]):
                chatbot = gr.Chatbot(
                    label="Conversational AI Assistant",
                    height=560,
                    show_label=False,
                    avatar_images=(None, "https://api.iconify.design/lucide:bot.svg?color=%233b82f6"),
                    value=[{
                        "role": "assistant",
                        "content": (
                            "**Welcome to StockMind AI! 👋📈**\n\n"
                            "I'm your intelligent quantitative market assistant. I can analyze financial trends, "
                            "generate machine learning forecasts, calculate support & resistance, compare companies, "
                            "and explain technical indicators in plain language.\n\n"
                            "*Try asking:* `'Analyze TCS'`, `'Compare TCS and Infosys'`, `'How is the stock market today?'`, "
                            "or in Tanglish `'TCS stock ippo epdi iruku?'`."
                        )
                    }]
                )

                # Input Controls
                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="Ask about any stock, trend, comparison, or prediction (e.g. 'Analyze TCS', 'Reliance epdi iruku?')...",
                        label="Your Query",
                        show_label=False,
                        lines=2,
                        max_lines=4,
                        scale=9,
                        autofocus=True
                    )
                    send_btn = gr.Button("Send 🚀", elem_classes=["primary-btn"], scale=2)

                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear Conversation", size="sm")
                    disclaimer_text = gr.Markdown(
                        "<div style='font-size: 11px; color: #94A3B8; text-align: right; padding-top: 4px;'>"
                        "⚠️ <em>Educational & Research Tool. Non-guaranteed algorithmic forecasts. Not financial advice.</em>"
                        "</div>"
                    )

            # RIGHT COLUMN: Quantitative Visual Terminal & Dashboard
            with gr.Column(scale=7):
                # 9 Dashboard Stat Cards
                stat_cards_output = gr.HTML(value=initial_cards)

                # Interactive Visualization Tabs
                with gr.Tabs():
                    with gr.Tab("🕯️ Technical & Overlays", id="tab_candle"):
                        candlestick_plot = gr.Plot(value=initial_candle, label="Price & Overlays", show_label=False)

                    with gr.Tab("🔮 AI Forecast Cone", id="tab_pred"):
                        prediction_plot = gr.Plot(value=initial_pred, label="ML Trajectory", show_label=False)

                    with gr.Tab("📊 Momentum (RSI & MACD)", id="tab_osc"):
                        oscillators_plot = gr.Plot(value=initial_osc, label="Oscillators", show_label=False)

                    with gr.Tab("⚔️ Stock Comparison", id="tab_comp"):
                        comparison_plot = gr.Plot(value=initial_comp, label="Comparison Chart", show_label=False)
                        comparison_md_output = gr.Markdown(value=initial_comp_md)

                    with gr.Tab("📋 Scenarios & Strategy", id="tab_strat"):
                        strategy_md_output = gr.Markdown(value=initial_strat)

        # Wire Submit Actions
        all_outputs = [
            chatbot,
            msg_input,
            active_symbol_state,
            stat_cards_output,
            candlestick_plot,
            prediction_plot,
            oscillators_plot,
            comparison_plot,
            strategy_md_output,
            comparison_md_output
        ]

        chat_args = dict(
            fn=handle_chat_and_analysis,
            inputs=[
                msg_input,
                chatbot,
                active_symbol_state,
                candlestick_plot,
                prediction_plot,
                oscillators_plot,
                comparison_plot,
                stat_cards_output,
                strategy_md_output,
                comparison_md_output
            ],
            outputs=all_outputs
        )

        # Send button & Enter key on input
        send_btn.click(**chat_args)
        msg_input.submit(**chat_args)

        # Clear conversation
        def clear_chat():
            return [
                [{
                    "role": "assistant",
                    "content": "Conversation cleared. Which stock or market topic would you like to explore next?"
                }],
                ""
            ]
        clear_btn.click(fn=clear_chat, inputs=[], outputs=[chatbot, msg_input])

        # Pill Quick Buttons
        def trigger_pill(text: str):
            return text

        pill_tcs.click(fn=lambda: "Analyze TCS", inputs=[], outputs=[msg_input]).then(**chat_args)
        pill_comp.click(fn=lambda: "Compare TCS and Infosys", inputs=[], outputs=[msg_input]).then(**chat_args)
        pill_market.click(fn=lambda: "How is the stock market today?", inputs=[], outputs=[msg_input]).then(**chat_args)
        pill_apple.click(fn=lambda: "Apple stock prediction", inputs=[], outputs=[msg_input]).then(**chat_args)
        pill_tanglish.click(fn=lambda: "Reliance stock epdi iruku?", inputs=[], outputs=[msg_input]).then(**chat_args)
        pill_tips.click(fn=lambda: "Give me stock market tips", inputs=[], outputs=[msg_input]).then(**chat_args)

    return demo


def main():
    """Main execution function for launching StockMind AI web application."""
    print("=" * 60)
    print("  StockMind AI — Financial Intelligence & Prediction Platform")
    print("=" * 60)

    # 1. Build application
    demo = build_app()

    # 2. Port conflict safety: auto-detect open port if 7860 is occupied
    host = os.environ.get("HOST", "127.0.0.1")
    requested_port = int(os.environ.get("PORT", 7860))
    port = find_available_port(preferred_port=requested_port, host=host)

    if port != requested_port:
        print(f"[StockMind Info] Port {requested_port} is busy. Automatically switched to port {port}.")

    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
    )

    favicon = os.path.join(WORKSPACE_ROOT, "static", "favicon.png")
    favicon_path = favicon if os.path.exists(favicon) else None

    # 3. Launch Gradio web server
    # Note: share=False for normal local development. Change to share=True if you need a temporary public URL.
    demo.launch(
        server_name=host,
        server_port=port,
        inbrowser=True,
        show_error=True,
        share=False,
        theme=theme,
        css=CUSTOM_CSS,
        favicon_path=favicon_path
    )


if __name__ == "__main__":
    main()
