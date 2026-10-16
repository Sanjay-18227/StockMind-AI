"""
StockMind AI — Browser-Based Web Application (Gradio Interface)
Provides a ChatGPT/Claude-inspired conversational interface coupled with
real-time quantitative analytics, multi-horizon ML predictions, interactive
Plotly technical charts, and multilingual natural language understanding.
"""

import os
import sys
import socket
import time
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
    format_currency_conversion_response,
    format_why_explanation_response,
    format_deep_technical_response,
    format_how_it_works_response,
    format_risk_explanation_response,
    format_support_resistance_response,
    format_prediction_response
)
from data.global_market_data import get_market_overview
from data.market_data import resolve_ticker
from data.companies import get_all_companies
from model.live_signal import run_complete_stock_analysis
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

# Custom High-End CSS for Institutional Dark Theme + Responsive Navigation
CUSTOM_CSS = """
/* StockMind AI Custom Theme Enhancements */
body, .gradio-container {
    background-color: #0B0F19 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: #F8FAFC !important;
}

/* Sticky Top Navigation Bar (Always Visible across desktop, tablet, mobile) */
.sticky-nav-bar {
    position: sticky !important;
    top: 0 !important;
    z-index: 1000 !important;
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 8px 16px !important;
    margin-bottom: 14px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
}

.nav-back-btn {
    background: linear-gradient(135deg, #1E293B 0%, #334155 100%) !important;
    border: 1px solid #475569 !important;
    color: #F8FAFC !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    min-height: 36px !important;
}
.nav-back-btn:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    border-color: #3B82F6 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}

.nav-refresh-btn {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    color: #94A3B8 !important;
    border-radius: 8px !important;
    padding: 6px 12px !important;
    font-size: 13px !important;
    cursor: pointer !important;
    min-height: 36px !important;
}
.nav-refresh-btn:hover {
    color: #FFFFFF !important;
    border-color: #475569 !important;
    background: #334155 !important;
}

.view-badge {
    font-size: 13px !important;
    color: #38BDF8 !important;
    font-weight: 600 !important;
    margin: 0 !important;
}

.status-badge {
    font-size: 12px !important;
    color: #10B981 !important;
    font-weight: 600 !important;
    margin: 0 !important;
    text-align: right !important;
}

/* Header container */
.header-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 12px;
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
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.main-title {
    font-size: 24px;
    font-weight: 800;
    color: #FFFFFF;
    margin: 2px 0 6px 0;
    letter-spacing: -0.02em;
}

.sub-title {
    font-size: 13px;
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
    padding: 6px 12px !important;
    transition: all 0.2s ease !important;
}
.suggestion-pill:hover {
    background: #2563EB !important;
    border-color: #3B82F6 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

/* Contextual Follow-up Action Buttons Strip */
.followup-strip {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 6px !important;
    padding: 6px 0 !important;
    margin-bottom: 4px !important;
}

.followup-btn {
    background: rgba(30, 41, 59, 0.9) !important;
    border: 1px solid #334155 !important;
    color: #E2E8F0 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    padding: 4px 10px !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
}
.followup-btn:hover {
    background: #2563EB !important;
    border-color: #3B82F6 !important;
    color: #FFFFFF !important;
}

/* Chat container */
.chat-wrapper {
    border-radius: 14px;
    overflow: hidden;
}

/* Primary Button */
.primary-btn {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    cursor: pointer !important;
}
.primary-btn:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
}

/* Secondary Deep Technical View Container */
.deep-tech-panel {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
    padding: 20px !important;
    margin-top: 10px !important;
}

/* Mobile responsive adjustments */
@media (max-width: 768px) {
    .main-title { font-size: 20px !important; }
    .sticky-nav-bar { padding: 6px 12px !important; }
    .header-box { padding: 14px !important; }
    .followup-strip { gap: 4px !important; }
    .followup-btn { font-size: 10px !important; padding: 4px 8px !important; }
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


def get_default_session_state(default_symbol: str = "TCS.NS", initial_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generates clean session state structure."""
    return {
        "active_symbol": default_symbol,
        "previous_symbol": None,
        "comparison_symbol": None,
        "timeframe": "1y",
        "last_analysis": initial_analysis,
        "last_comparison": None,
        "last_market_overview": None,
        "is_processing": False,
        "last_sig": None,
        "last_time": 0.0,
        "current_view": "main",
        "view_history": ["main"],
        "processed_request_ids": set()
    }


def initial_stock_state(default_symbol: str = "TCS.NS") -> Tuple[Any, Any, Any, Any, str, str, str, str, Dict[str, Any]]:
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
        deep_tech_md = format_deep_technical_response(analysis, "en")
        session_data = get_default_session_state(default_symbol=resolved, initial_analysis=analysis)

        return fig_candle, fig_pred, fig_osc, fig_comp, cards_html, strategy_md, comparison_md, deep_tech_md, session_data
    except Exception as e:
        empty_fig = create_empty_figure("Enter a stock query to display charts.")
        cards_html = build_cards_html(None)
        strategy_md = build_strategy_markdown(None)
        comparison_md = build_comparison_markdown(None)
        deep_tech_md = "Select or analyze a stock to view deep technical metrics."
        session_data = get_default_session_state(default_symbol=default_symbol, initial_analysis=None)
        return empty_fig, empty_fig, empty_fig, empty_fig, cards_html, strategy_md, comparison_md, deep_tech_md, session_data


def handle_back_navigation(session_data: Dict[str, Any]):
    """
    Dedicated Back Navigation Handler:
    - Restores the previous view.
    - NEVER calls the LLM or stock analysis.
    - NEVER runs prediction or regenerates charts.
    - NEVER submits the textbox or repeats answers.
    - Completely decouples navigation from AI execution.
    """
    if not session_data or not isinstance(session_data, dict):
        session_data = get_default_session_state()

    history = session_data.get("view_history", ["main"])
    if len(history) > 1:
        history.pop()
        target_view = history[-1]
    else:
        target_view = "main"

    session_data["current_view"] = target_view
    session_data["view_history"] = history

    is_main = (target_view == "main")
    is_deep = (target_view == "deep_technical")
    active_sym = session_data.get("active_symbol", "TCS.NS")
    badge_text = "📍 **Active View:** Main Dashboard" if is_main else f"📍 **Active View:** Deep Technical ({active_sym})"

    return (
        gr.update(visible=is_main),
        gr.update(visible=is_deep),
        badge_text,
        session_data
    )


def handle_ui_refresh(session_data: Dict[str, Any]):
    """
    Safely refreshes/resets the UI state without re-running any prompt.
    """
    active_sym = session_data.get("active_symbol", "TCS.NS") if isinstance(session_data, dict) else "TCS.NS"
    last_analysis = session_data.get("last_analysis") if isinstance(session_data, dict) else None
    new_session = get_default_session_state(default_symbol=active_sym, initial_analysis=last_analysis)
    return (
        "",  # clear input textbox
        "📍 **Active View:** Main Dashboard",
        gr.update(visible=True),   # main_view visible
        gr.update(visible=False),  # deep_technical_view hidden
        new_session
    )


def handle_chat_and_analysis(
    user_message: str,
    chat_history: List[Dict[str, str]],
    session_data: Dict[str, Any],
    current_fig_candle: Any,
    current_fig_pred: Any,
    current_fig_osc: Any,
    current_fig_comp: Any,
    current_cards_html: str,
    current_strategy_md: str,
    current_comp_md: str,
    current_deep_tech_md: str
):
    """
    Main Centralized Conversational Assistant & Visual Engine Handler:
    1. Validates message and protects against double-submission / duplicate execution.
    2. Detects per-message language and script/style (English, Tamil, Tanglish, Hindi, Hinglish).
    3. Resolves conversation context (pronouns 'it', active stock, comparisons).
    4. Reuses cached market data / analysis for follow-ups (Why, Deep Technical, Risk, Prediction).
    5. Appends exactly ONE turn to history and renders clean UI state.
    """
    # 0. Session initialization & validation
    if not session_data or not isinstance(session_data, dict):
        session_data = get_default_session_state()

    query = (user_message or "").strip()
    history = list(chat_history) if chat_history else []

    # Current view states for safe return
    cur_view = session_data.get("current_view", "main")
    is_main_view = (cur_view == "main")
    is_deep_view = (cur_view == "deep_technical")
    view_badge_text = "📍 **Active View:** Main Dashboard" if is_main_view else f"📍 **Active View:** Deep Technical ({session_data.get('active_symbol', 'TCS.NS')})"

    if not query:
        return (
            history,
            "",
            session_data,
            current_cards_html,
            current_fig_candle,
            current_fig_pred,
            current_fig_osc,
            current_fig_comp,
            current_strategy_md,
            current_comp_md,
            current_deep_tech_md,
            gr.update(visible=is_main_view),
            gr.update(visible=is_deep_view),
            view_badge_text
        )

    # In-Flight Duplicate Request Guard (Prevents double clicks, simultaneous Enter+Send, rapid tap)
    if session_data.get("is_processing", False):
        print(f"[StockMind] Duplicate request dropped (already processing): '{query}'")
        return (
            history,
            "",
            session_data,
            current_cards_html,
            current_fig_candle,
            current_fig_pred,
            current_fig_osc,
            current_fig_comp,
            current_strategy_md,
            current_comp_md,
            current_deep_tech_md,
            gr.update(visible=is_main_view),
            gr.update(visible=is_deep_view),
            view_badge_text
        )

    # Rapid Duplicate Submission Guard (Within duplicate window with identical content)
    now = time.time()
    active_sym = session_data.get("active_symbol") or "TCS.NS"
    query_sig = f"{query.lower()}_{active_sym}"
    last_completed = session_data.get("last_completed_time", 0.0)
    last_started = session_data.get("last_time", 0.0)
    if session_data.get("last_sig") == query_sig and ((now - last_completed) < 3.0 or (now - last_started) < 6.0):
        print(f"[StockMind] Rapid duplicate query suppressed: '{query}'")
        return (
            history,
            "",
            session_data,
            current_cards_html,
            current_fig_candle,
            current_fig_pred,
            current_fig_osc,
            current_fig_comp,
            current_strategy_md,
            current_comp_md,
            current_deep_tech_md,
            gr.update(visible=is_main_view),
            gr.update(visible=is_deep_view),
            view_badge_text
        )

    # Set in-flight processing locks
    session_data["is_processing"] = True
    session_data["last_sig"] = query_sig
    session_data["last_time"] = now

    try:
        # 1. Detect language & style of THIS specific message
        lang = detect_language(query)

        # 2. Context-aware intent classification
        parsed = classify_intent(query, active_symbol=active_sym)
        intent = parsed.get("intent", "STOCK_ANALYSIS")
        primary_sym = parsed.get("primary_symbol") or active_sym
        secondary_sym = parsed.get("secondary_symbol")
        tf = parsed.get("timeframe") or session_data.get("timeframe", "1y")

        # Defaults for UI outputs
        new_cards_html = current_cards_html
        new_fig_candle = current_fig_candle
        new_fig_pred = current_fig_pred
        new_fig_osc = current_fig_osc
        new_fig_comp = current_fig_comp
        new_strategy_md = current_strategy_md
        new_comp_md = current_comp_md
        new_deep_tech_md = current_deep_tech_md
        assistant_reply = ""

        # 3. Handle Conversational & Greeting queries
        if intent in ["GENERAL_GREETING", "GENERAL_HOW_ARE_YOU", "GENERAL_CAPABILITIES", "GENERAL_OFF_TOPIC", "GENERAL_CONVERSATION"] and not parsed.get("symbols"):
            assistant_reply = format_conversational_response(intent, lang)

        # 4. Handle Market Overview
        elif intent == "MARKET_OVERVIEW":
            overview = get_market_overview()
            session_data["last_market_overview"] = overview
            assistant_reply = format_market_overview_response(overview, lang)

        # 5. Handle Stock Comparison
        elif intent == "STOCK_COMPARISON":
            if not secondary_sym:
                secondary_sym = "INFY.NS" if "TCS" in primary_sym else "TCS.NS"

            comp_data = generate_comparison_analysis(primary_sym, secondary_sym, timeframe=tf)
            session_data["last_comparison"] = comp_data
            assistant_reply = format_comparison_response(comp_data, lang)
            new_fig_comp = create_comparison_figure(comp_data)
            new_comp_md = build_comparison_markdown(comp_data)

        # 6. Targeted Contextual Follow-up Intents (Reuses cached analysis if available)
        elif intent in ["WHY_EXPLANATION", "DEEP_TECHNICAL", "HOW_IT_WORKS", "RISK_QUERY", "SUPPORT_RESISTANCE", "PREDICTION_QUERY", "LANGUAGE_SWITCH"]:
            # Check if existing cached analysis is available for this symbol
            cached_analysis = session_data.get("last_analysis")
            if cached_analysis and cached_analysis.get("quote", {}).get("symbol") == primary_sym:
                analysis = cached_analysis
            else:
                resolved = resolve_ticker(primary_sym)
                analysis = run_complete_stock_analysis(resolved, period=tf)
                session_data["last_analysis"] = analysis
                session_data["active_symbol"] = resolved

            # Generate targeted response without repeating whole analysis
            if intent == "WHY_EXPLANATION":
                assistant_reply = format_why_explanation_response(analysis, lang)
            elif intent == "DEEP_TECHNICAL":
                assistant_reply = format_deep_technical_response(analysis, lang)
                new_deep_tech_md = format_deep_technical_response(analysis, "en")
                # Transition view history to deep technical
                if session_data.get("current_view") != "deep_technical":
                    session_data["view_history"].append("deep_technical")
                    session_data["current_view"] = "deep_technical"
                    is_main_view = False
                    is_deep_view = True
                    view_badge_text = f"📍 **Active View:** Deep Technical ({analysis['quote']['symbol']})"
            elif intent == "HOW_IT_WORKS":
                assistant_reply = format_how_it_works_response(analysis, lang)
            elif intent == "RISK_QUERY":
                assistant_reply = format_risk_explanation_response(analysis, lang)
            elif intent == "SUPPORT_RESISTANCE":
                assistant_reply = format_support_resistance_response(analysis, lang)
            elif intent == "PREDICTION_QUERY":
                assistant_reply = format_prediction_response(analysis, lang)
            elif intent == "LANGUAGE_SWITCH":
                # Re-render analysis overview in the requested language
                assistant_reply = format_stock_analysis_response(analysis, "STOCK_ANALYSIS", lang)

        # 7. Currency Conversion
        elif intent == "CURRENCY_CONVERSION":
            resolved = resolve_ticker(primary_sym)
            analysis = run_complete_stock_analysis(resolved, period=tf)
            session_data["last_analysis"] = analysis
            session_data["active_symbol"] = resolved
            assistant_reply = format_currency_conversion_response(analysis, lang=lang)

            q = analysis["quote"]
            sym_name = q.get("name", resolved)
            curr = q.get("currency_symbol", "₹")
            new_cards_html = build_cards_html(analysis)
            new_fig_candle = create_candlestick_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
            new_fig_pred = create_prediction_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
            new_fig_osc = create_oscillators_figure(analysis["chart_payload"], symbol_name=sym_name)
            new_strategy_md = build_strategy_markdown(analysis)
            new_deep_tech_md = format_deep_technical_response(analysis, "en")

        # 8. Stock Tips
        elif intent == "STOCK_TIPS":
            if not parsed.get("symbols") and not parsed.get("primary_symbol"):
                assistant_reply = format_stock_tips_response(lang=lang)
            else:
                try:
                    resolved = resolve_ticker(primary_sym)
                    analysis = run_complete_stock_analysis(resolved, period=tf)
                    session_data["last_analysis"] = analysis
                    session_data["active_symbol"] = resolved
                    assistant_reply = format_stock_tips_response(lang=lang, analysis=analysis)
                    q = analysis["quote"]
                    sym_name = q.get("name", resolved)
                    curr = q.get("currency_symbol", "₹")
                    new_cards_html = build_cards_html(analysis)
                    new_fig_candle = create_candlestick_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
                    new_fig_pred = create_prediction_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
                    new_fig_osc = create_oscillators_figure(analysis["chart_payload"], symbol_name=sym_name)
                    new_strategy_md = build_strategy_markdown(analysis)
                    new_deep_tech_md = format_deep_technical_response(analysis, "en")
                except Exception:
                    assistant_reply = format_stock_tips_response(lang=lang)

        # 9. Standard Stock Analysis (Single stock query, prediction, casual questions, simple overview)
        else:
            resolved = resolve_ticker(primary_sym)
            analysis = run_complete_stock_analysis(resolved, period=tf)
            session_data["last_analysis"] = analysis
            session_data["active_symbol"] = resolved
            assistant_reply = format_stock_analysis_response(analysis, intent, lang)

            # Update charts and dashboard cards
            q = analysis["quote"]
            sym_name = q.get("name", resolved)
            curr = q.get("currency_symbol", "₹")
            new_cards_html = build_cards_html(analysis)
            new_fig_candle = create_candlestick_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
            new_fig_pred = create_prediction_figure(analysis["chart_payload"], symbol_name=sym_name, currency_symbol=curr)
            new_fig_osc = create_oscillators_figure(analysis["chart_payload"], symbol_name=sym_name)
            new_strategy_md = build_strategy_markdown(analysis)
            new_deep_tech_md = format_deep_technical_response(analysis, "en")

        # Append turn to history: EXACTLY ONE USER MESSAGE AND ONE ASSISTANT REPLY
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": assistant_reply})

        return (
            history,
            "",
            session_data,
            new_cards_html,
            new_fig_candle,
            new_fig_pred,
            new_fig_osc,
            new_fig_comp,
            new_strategy_md,
            new_comp_md,
            new_deep_tech_md,
            gr.update(visible=is_main_view),
            gr.update(visible=is_deep_view),
            view_badge_text
        )

    except Exception as e:
        # Technical debug in terminal
        print(f"[StockMind Error] Failed processing query '{query}':", file=sys.stderr)
        traceback.print_exc()

        # User-friendly message in UI without crashing or dumping traceback
        clean_err = str(e)
        if "No data found" in clean_err or "Invalid ticker" in clean_err:
            friendly_msg = f"⚠️ Could not find market data for **'{query}'**. Please check if the ticker symbol or company name is correct (e.g. *TCS*, *Reliance*, *Infosys*, *Apple*, *Tesla*)."
        elif "rate limit" in clean_err.lower():
            friendly_msg = "⚠️ Market data rate limit temporarily reached. Please wait a few seconds and try again."
        else:
            friendly_msg = f"⚠️ Market data couldn't be loaded right now. Please try again or verify the symbol '{query}'."

        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": friendly_msg})

        return (
            history,
            "",
            session_data,
            current_cards_html,
            current_fig_candle,
            current_fig_pred,
            current_fig_osc,
            current_fig_comp,
            current_strategy_md,
            current_comp_md,
            current_deep_tech_md,
            gr.update(visible=is_main_view),
            gr.update(visible=is_deep_view),
            view_badge_text
        )

    finally:
        # Release in-flight lock safely
        session_data["is_processing"] = False
        session_data["last_completed_time"] = time.time()


def build_app() -> gr.Blocks:
    """Builds and wires the complete StockMind AI Gradio application."""
    (
        initial_candle,
        initial_pred,
        initial_osc,
        initial_comp,
        initial_cards,
        initial_strat,
        initial_comp_md,
        initial_deep_tech,
        initial_session
    ) = initial_stock_state("TCS.NS")

    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
    )

    with gr.Blocks(title="StockMind AI - Financial Intelligence & ML Predictions") as demo:
        # Unified Conversational and UI Session State
        session_state = gr.State(value=initial_session)

        # 1. Sticky Navigation Bar (Always visible on desktop, tablet, and mobile)
        with gr.Row(elem_classes=["sticky-nav-bar"]):
            with gr.Row():
                back_btn = gr.Button("⬅️ Back", elem_classes=["nav-back-btn"], size="sm")
                refresh_btn = gr.Button("🔄 Refresh", elem_classes=["nav-refresh-btn"], size="sm")
            with gr.Row():
                view_badge = gr.Markdown("📍 **Active View:** Main Dashboard", elem_classes=["view-badge"])
                status_indicator = gr.Markdown("🟢 **Live Market Engine Active**", elem_classes=["status-badge"])

        # 2. Header & Branding Box
        with gr.Row():
            with gr.Column(elem_classes=["header-box"]):
                gr.HTML("""
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                    <div>
                        <div class="brand-badge">⚡ Real-time Analytics &bull; Calibrated ML Trajectory &bull; Multilingual</div>
                        <h1 class="main-title">How can I help you?</h1>
                        <p class="sub-title">Analyze stocks, understand markets, compare companies, or just ask in English, Tamil, Tanglish, or Hindi.</p>
                    </div>
                </div>
                """)

        # 3. Quick Action Suggestion Prompts
        with gr.Row():
            pill_tcs = gr.Button("📈 Analyze TCS", elem_classes=["suggestion-pill"], size="sm")
            pill_comp = gr.Button("⚔️ Compare TCS and Infosys", elem_classes=["suggestion-pill"], size="sm")
            pill_market = gr.Button("🌐 Market Pulse (Nifty / Global)", elem_classes=["suggestion-pill"], size="sm")
            pill_apple = gr.Button("🔮 Apple Stock Prediction", elem_classes=["suggestion-pill"], size="sm")
            pill_tanglish = gr.Button("🗣️ Reliance stock epdi iruku?", elem_classes=["suggestion-pill"], size="sm")
            pill_tips = gr.Button("💡 Trading Rules & Tips", elem_classes=["suggestion-pill"], size="sm")

        # 4. PRIMARY VIEW CONTAINER: Main 2-Column Dashboard & Chat
        with gr.Column(visible=True) as main_view_container:
            with gr.Row():
                # LEFT COLUMN: Conversational AI Assistant
                with gr.Column(scale=5, elem_classes=["chat-wrapper"]):
                    chatbot = gr.Chatbot(
                        label="Conversational AI Assistant",
                        height=540,
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

                    # Dynamic Contextual Follow-up Actions Strip
                    with gr.Row(elem_classes=["followup-strip"]):
                        pill_why = gr.Button("❓ Why?", elem_classes=["followup-btn"], size="sm")
                        pill_deep = gr.Button("📊 Deep Technical", elem_classes=["followup-btn"], size="sm")
                        pill_risk = gr.Button("🛡️ Risk", elem_classes=["followup-btn"], size="sm")
                        pill_pred = gr.Button("🔮 Prediction", elem_classes=["followup-btn"], size="sm")
                        pill_sr = gr.Button("🎯 Support & Resistance", elem_classes=["followup-btn"], size="sm")
                        pill_how = gr.Button("⚙️ How It Works", elem_classes=["followup-btn"], size="sm")

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

        # 5. SECONDARY VIEW CONTAINER: Dedicated Deep Technical Terminal View
        with gr.Column(visible=False, elem_classes=["deep-tech-panel"]) as deep_technical_view_container:
            with gr.Row():
                back_from_deep_btn = gr.Button("⬅️ Back to Main Dashboard", elem_classes=["nav-back-btn"], size="sm")
            deep_tech_markdown_output = gr.Markdown(value=initial_deep_tech)

        # Wire Submit & Action Pipeline
        all_inputs = [
            msg_input,
            chatbot,
            session_state,
            candlestick_plot,
            prediction_plot,
            oscillators_plot,
            comparison_plot,
            stat_cards_output,
            strategy_md_output,
            comparison_md_output,
            deep_tech_markdown_output
        ]

        all_outputs = [
            chatbot,
            msg_input,
            session_state,
            stat_cards_output,
            candlestick_plot,
            prediction_plot,
            oscillators_plot,
            comparison_plot,
            strategy_md_output,
            comparison_md_output,
            deep_tech_markdown_output,
            main_view_container,
            deep_technical_view_container,
            view_badge
        ]

        chat_args = dict(
            fn=handle_chat_and_analysis,
            inputs=all_inputs,
            outputs=all_outputs
        )

        # Primary user submit triggers (Send button & Enter key)
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

        # Navigation Handlers (Back & Refresh) — ZERO AI CALLS
        nav_back_args = dict(
            fn=handle_back_navigation,
            inputs=[session_state],
            outputs=[main_view_container, deep_technical_view_container, view_badge, session_state]
        )
        back_btn.click(**nav_back_args)
        back_from_deep_btn.click(**nav_back_args)

        refresh_btn.click(
            fn=handle_ui_refresh,
            inputs=[session_state],
            outputs=[msg_input, view_badge, main_view_container, deep_technical_view_container, session_state]
        )

        # Helper function for quick pill actions (Zero .then() chaining to prevent duplicate callbacks)
        def trigger_query(text: str):
            def handler(h, s, fc, fp, fo, fcomp, sc, sm, cm, dt):
                return handle_chat_and_analysis(text, h, s, fc, fp, fo, fcomp, sc, sm, cm, dt)
            return handler

        pill_tcs.click(
            fn=trigger_query("Analyze TCS"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_comp.click(
            fn=trigger_query("Compare TCS and Infosys"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_market.click(
            fn=trigger_query("How is the stock market today?"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_apple.click(
            fn=trigger_query("Apple stock prediction"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_tanglish.click(
            fn=trigger_query("Reliance stock epdi iruku?"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_tips.click(
            fn=trigger_query("Give me stock market tips"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )

        # Follow-up actions strip buttons
        pill_why.click(
            fn=trigger_query("Why?"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_deep.click(
            fn=trigger_query("Deep Technical"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_risk.click(
            fn=trigger_query("Why is it risky?"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_pred.click(
            fn=trigger_query("Just prediction"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_sr.click(
            fn=trigger_query("Support level?"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )
        pill_how.click(
            fn=trigger_query("How it works"),
            inputs=all_inputs[1:],
            outputs=all_outputs
        )

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
