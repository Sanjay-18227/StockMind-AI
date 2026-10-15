"""
Plotly Chart Generation for StockMind AI Gradio Interface:
Constructs high-performance interactive charts for:
1. Candlestick + Moving Averages + Bollinger Bands + Volume
2. AI ML Forecast Trajectory with Uncertainty Cone (Historical vs Predicted clearly distinguished)
3. Oscillators (RSI + MACD Subplots)
4. Normalized Stock Comparison (Base 100)
"""

from typing import Dict, Any, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Clean institutional color palette
COLORS = {
    "bg": "#0F172A",          # Deep slate background
    "surface": "#1E293B",     # Card surface
    "text": "#F8FAFC",        # Bright white text
    "text_muted": "#94A3B8",  # Slate muted
    "grid": "#334155",        # Hairline grid
    "green": "#10B981",       # Bullish emerald
    "red": "#EF4444",         # Bearish rose
    "blue": "#3B82F6",        # Primary blue
    "purple": "#8B5CF6",      # EMA purple
    "orange": "#F59E0B",      # Forecast / Warning amber
    "cyan": "#06B6D4",        # Secondary indicator
}

def create_candlestick_figure(chart_payload: Dict[str, Any], symbol_name: str = "Stock", currency_symbol: str = "₹") -> go.Figure:
    """
    Creates an interactive 2-row subplot:
    Row 1 (75% height): Candlestick, SMA 20, SMA 50, EMA 20, Bollinger Bands, Support/Resistance levels.
    Row 2 (25% height): Volume bars colored by candle direction.
    """
    dates = chart_payload.get("dates", [])
    ohlc = chart_payload.get("ohlc", {})
    volume = chart_payload.get("volume", [])
    overlays = chart_payload.get("overlays", {})
    key_levels = chart_payload.get("key_levels", {})

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.75, 0.25],
        subplot_titles=(f"{symbol_name} — Price & Technical Overlays", "Trading Volume")
    )

    if dates and ohlc.get("close"):
        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=dates,
                open=ohlc.get("open", []),
                high=ohlc.get("high", []),
                low=ohlc.get("low", []),
                close=ohlc.get("close", []),
                name="OHLC Price",
                increasing_line_color=COLORS["green"],
                decreasing_line_color=COLORS["red"],
                showlegend=True
            ),
            row=1, col=1
        )

        # Overlays: SMA 20, SMA 50, EMA 20
        if overlays.get("sma_20"):
            fig.add_trace(
                go.Scatter(
                    x=dates, y=overlays["sma_20"],
                    mode="lines", name="SMA (20)",
                    line=dict(color=COLORS["blue"], width=1.5)
                ),
                row=1, col=1
            )
        if overlays.get("sma_50"):
            fig.add_trace(
                go.Scatter(
                    x=dates, y=overlays["sma_50"],
                    mode="lines", name="SMA (50)",
                    line=dict(color=COLORS["orange"], width=1.5)
                ),
                row=1, col=1
            )
        if overlays.get("ema_20"):
            fig.add_trace(
                go.Scatter(
                    x=dates, y=overlays["ema_20"],
                    mode="lines", name="EMA (20)",
                    line=dict(color=COLORS["purple"], width=1.5, dash="dot")
                ),
                row=1, col=1
            )

        # Bollinger Bands
        if overlays.get("bb_upper") and overlays.get("bb_lower"):
            fig.add_trace(
                go.Scatter(
                    x=dates, y=overlays["bb_upper"],
                    mode="lines", name="Upper BB",
                    line=dict(color="rgba(148, 163, 184, 0.4)", width=1, dash="dash"),
                    showlegend=False
                ),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=dates, y=overlays["bb_lower"],
                    mode="lines", name="BB (20, 2)",
                    line=dict(color="rgba(148, 163, 184, 0.4)", width=1, dash="dash"),
                    fill="tonexty",
                    fillcolor="rgba(148, 163, 184, 0.05)"
                ),
                row=1, col=1
            )

        # Support & Resistance levels
        sup = key_levels.get("nearest_support")
        res = key_levels.get("nearest_resistance")
        if sup:
            fig.add_hline(
                y=sup, line=dict(color=COLORS["green"], dash="dash", width=1.2),
                annotation_text=f"Support: {currency_symbol}{sup:,.2f}",
                annotation_position="bottom right",
                annotation_font=dict(size=10, color=COLORS["green"]),
                row=1, col=1
            )
        if res:
            fig.add_hline(
                y=res, line=dict(color=COLORS["red"], dash="dash", width=1.2),
                annotation_text=f"Resistance: {currency_symbol}{res:,.2f}",
                annotation_position="top right",
                annotation_font=dict(size=10, color=COLORS["red"]),
                row=1, col=1
            )

        # Volume bars
        colors = [
            COLORS["green"] if c >= o else COLORS["red"]
            for o, c in zip(ohlc.get("open", []), ohlc.get("close", []))
        ]
        fig.add_trace(
            go.Bar(
                x=dates, y=volume,
                name="Volume",
                marker_color=colors,
                opacity=0.8,
                showlegend=False
            ),
            row=2, col=1
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["surface"],
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=COLORS["text"])
        ),
        font=dict(family="Inter, system-ui, sans-serif", color=COLORS["text"])
    )
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"], gridwidth=0.5)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"], gridwidth=0.5)
    return fig


def create_prediction_figure(chart_payload: Dict[str, Any], symbol_name: str = "Stock", currency_symbol: str = "₹") -> go.Figure:
    """
    Creates an AI Forecast Trajectory visualization:
    - Historical Close Prices (solid line)
    - Vertical dividing line indicating transition from history to future
    - AI Forecast Trajectory (dashed line)
    - Shaded Confidence Band / Uncertainty Cone (Upper & Lower bounds)
    - Clear visual distinction between historical and predicted portions.
    """
    fig = go.Figure()
    hist_dates = chart_payload.get("dates", [])
    ohlc = chart_payload.get("ohlc", {})
    hist_prices = ohlc.get("close", [])
    forecast = chart_payload.get("forecast", {})

    # Show last 40 bars of history for clean zoom
    n_show = min(len(hist_dates), 45)
    display_hist_dates = hist_dates[-n_show:] if hist_dates else []
    display_hist_prices = hist_prices[-n_show:] if hist_prices else []

    if display_hist_dates and display_hist_prices:
        # 1. Historical Prices (solid blue line)
        fig.add_trace(
            go.Scatter(
                x=display_hist_dates,
                y=display_hist_prices,
                mode="lines+markers",
                name="Historical Actual Price",
                line=dict(color=COLORS["blue"], width=2.5),
                marker=dict(size=3)
            )
        )

    # 2. Prediction Trajectory & Uncertainty Cone
    pred_dates = forecast.get("dates", [])
    pred_prices = forecast.get("prices", [])
    upper_bounds = forecast.get("upper_bounds", [])
    lower_bounds = forecast.get("lower_bounds", [])
    direction = forecast.get("direction", "SIDEWAYS")
    conf = forecast.get("confidence", 50.0)

    dir_color = COLORS["green"] if direction == "UP" else (COLORS["red"] if direction == "DOWN" else COLORS["orange"])

    if pred_dates and pred_prices:
        # Uncertainty Cone (Lower bound first, then Upper bound with fill)
        if lower_bounds and upper_bounds and len(lower_bounds) == len(pred_dates):
            fig.add_trace(
                go.Scatter(
                    x=pred_dates,
                    y=lower_bounds,
                    mode="lines",
                    name="Lower Confidence Bound (80%)",
                    line=dict(color="rgba(245, 158, 11, 0.3)", width=1, dash="dot"),
                    showlegend=False
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=pred_dates,
                    y=upper_bounds,
                    mode="lines",
                    name=f"Forecast Uncertainty Cone ({conf:.0f}% Conf.)",
                    line=dict(color="rgba(245, 158, 11, 0.3)", width=1, dash="dot"),
                    fill="tonexty",
                    fillcolor="rgba(245, 158, 11, 0.12)"
                )
            )

        # Connect last historical point to first forecast point
        connect_dates = [display_hist_dates[-1]] + pred_dates if display_hist_dates else pred_dates
        connect_prices = [display_hist_prices[-1]] + pred_prices if display_hist_prices else pred_prices

        # Forecast Trajectory (dashed vibrant line)
        fig.add_trace(
            go.Scatter(
                x=connect_dates,
                y=connect_prices,
                mode="lines+markers",
                name=f"AI Forecast ({direction})",
                line=dict(color=dir_color, width=2.5, dash="dash"),
                marker=dict(size=5, symbol="diamond")
            )
        )

        # Transition vertical line
        if display_hist_dates:
            fig.add_vline(
                x=display_hist_dates[-1],
                line=dict(color=COLORS["text_muted"], width=1.5, dash="dashdot"),
                annotation_text="Today / Forecast Start",
                annotation_position="top left",
                annotation_font=dict(size=10, color=COLORS["text_muted"])
            )

    fig.update_layout(
        title=dict(
            text=f"{symbol_name} — AI Machine Learning Forecast & Confidence Cone",
            font=dict(size=15, color=COLORS["text"])
        ),
        template="plotly_dark",
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["surface"],
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=COLORS["text"])
        ),
        font=dict(family="Inter, system-ui, sans-serif", color=COLORS["text"]),
        annotations=[
            dict(
                text="⚠️ Algorithmic Projection — Educational Use Only (Non-Guaranteed)",
                xref="paper", yref="paper",
                x=0.5, y=-0.12,
                showarrow=False,
                font=dict(size=10, color=COLORS["text_muted"])
            )
        ]
    )
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"], gridwidth=0.5)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"], gridwidth=0.5)
    return fig


def create_oscillators_figure(chart_payload: Dict[str, Any], symbol_name: str = "Stock") -> go.Figure:
    """
    Creates an interactive 2-row subplot for technical oscillators:
    Row 1: RSI (14) with 70/30 boundary thresholds and neutral zone shading
    Row 2: MACD line, Signal line, and MACD Histogram bars
    """
    dates = chart_payload.get("dates", [])
    oscillators = chart_payload.get("oscillators", {})

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.5, 0.5],
        subplot_titles=(f"{symbol_name} — Relative Strength Index (RSI 14)", "MACD (12, 26, 9) & Momentum Histogram")
    )

    if dates and oscillators:
        # 1. RSI
        rsi = oscillators.get("rsi", [])
        if rsi:
            fig.add_trace(
                go.Scatter(
                    x=dates, y=rsi,
                    mode="lines", name="RSI (14)",
                    line=dict(color=COLORS["purple"], width=2)
                ),
                row=1, col=1
            )
            # Overbought (70) and Oversold (30) lines
            fig.add_hline(
                y=70, line=dict(color=COLORS["red"], dash="dash", width=1),
                annotation_text="Overbought (70)", annotation_position="top right",
                annotation_font=dict(size=9, color=COLORS["red"]),
                row=1, col=1
            )
            fig.add_hline(
                y=30, line=dict(color=COLORS["green"], dash="dash", width=1),
                annotation_text="Oversold (30)", annotation_position="bottom right",
                annotation_font=dict(size=9, color=COLORS["green"]),
                row=1, col=1
            )

        # 2. MACD
        macd = oscillators.get("macd", [])
        signal = oscillators.get("macd_signal", [])
        hist = oscillators.get("macd_hist", [])

        if macd and signal:
            fig.add_trace(
                go.Scatter(
                    x=dates, y=macd,
                    mode="lines", name="MACD",
                    line=dict(color=COLORS["blue"], width=1.5)
                ),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=dates, y=signal,
                    mode="lines", name="Signal",
                    line=dict(color=COLORS["orange"], width=1.5, dash="dot")
                ),
                row=2, col=1
            )
        if hist:
            hist_colors = [COLORS["green"] if h >= 0 else COLORS["red"] for h in hist]
            fig.add_trace(
                go.Bar(
                    x=dates, y=hist,
                    name="MACD Hist",
                    marker_color=hist_colors,
                    opacity=0.7,
                    showlegend=False
                ),
                row=2, col=1
            )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["surface"],
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=COLORS["text"])
        ),
        font=dict(family="Inter, system-ui, sans-serif", color=COLORS["text"])
    )
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"], gridwidth=0.5)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"], gridwidth=0.5)
    return fig


def create_comparison_figure(comparison_dict: Dict[str, Any]) -> go.Figure:
    """
    Creates a Normalized Returns chart (Base 100) comparing two assets over time.
    """
    fig = go.Figure()
    stock_a = comparison_dict.get("stock_a", {})
    stock_b = comparison_dict.get("stock_b", {})
    chart_data = comparison_dict.get("chart_data", {})
    dates = chart_data.get("dates", [])
    norm_a = chart_data.get("normalized_a", [])
    norm_b = chart_data.get("normalized_b", [])

    sym_a = stock_a.get("name") or stock_a.get("symbol", "Asset A")
    sym_b = stock_b.get("name") or stock_b.get("symbol", "Asset B")

    if dates and norm_a and norm_b:
        fig.add_trace(
            go.Scatter(
                x=dates, y=norm_a,
                mode="lines", name=f"{sym_a} (Base 100)",
                line=dict(color=COLORS["blue"], width=2.2)
            )
        )
        fig.add_trace(
            go.Scatter(
                x=dates, y=norm_b,
                mode="lines", name=f"{sym_b} (Base 100)",
                line=dict(color=COLORS["orange"], width=2.2)
            )
        )
        # 100 Baseline
        fig.add_hline(
            y=100, line=dict(color="rgba(148, 163, 184, 0.5)", dash="dash", width=1),
            annotation_text="Base 100", annotation_position="top left",
            annotation_font=dict(size=9, color=COLORS["text_muted"])
        )

    fig.update_layout(
        title=dict(
            text=f"Head-to-Head Performance: {sym_a} vs {sym_b}",
            font=dict(size=15, color=COLORS["text"])
        ),
        template="plotly_dark",
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["surface"],
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color=COLORS["text"])
        ),
        font=dict(family="Inter, system-ui, sans-serif", color=COLORS["text"])
    )
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["grid"], gridwidth=0.5)
    fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid"], gridwidth=0.5)
    return fig


def create_empty_figure(message: str = "Select or query a stock to display technical charts.") -> go.Figure:
    """Returns a placeholder figure with a clean message."""
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLORS["bg"],
        plot_bgcolor=COLORS["surface"],
        annotations=[
            dict(
                text=message,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14, color=COLORS["text_muted"])
            )
        ]
    )
    return fig


def build_cards_html(analysis: Optional[Dict[str, Any]] = None) -> str:
    """
    Renders the 9 dashboard cards as a clean modern responsive grid.
    """
    if not analysis or "dashboard_cards" not in analysis:
        return """
        <div style="padding: 16px; text-align: center; color: #94A3B8; background: #1E293B; border-radius: 12px; border: 1px solid #334155;">
            💡 <em>Enter a stock symbol or ask a question in chat to load quantitative metrics.</em>
        </div>
        """

    cards = analysis.get("dashboard_cards", [])
    q = analysis.get("quote", {})
    ticker = q.get("symbol", "")
    name = q.get("name", "")

    tone_map = {
        "positive": ("#10B981", "rgba(16, 185, 129, 0.12)"),
        "green": ("#10B981", "rgba(16, 185, 129, 0.12)"),
        "negative": ("#EF4444", "rgba(239, 68, 68, 0.12)"),
        "red": ("#EF4444", "rgba(239, 68, 68, 0.12)"),
        "neutral": ("#94A3B8", "rgba(148, 163, 184, 0.12)"),
        "gray": ("#94A3B8", "rgba(148, 163, 184, 0.12)"),
        "warning": ("#F59E0B", "rgba(245, 158, 11, 0.12)"),
        "amber": ("#F59E0B", "rgba(245, 158, 11, 0.12)")
    }

    html = ['<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 8px;">']

    for c in cards:
        color, bg = tone_map.get(c.get("tone", "neutral"), ("#3B82F6", "rgba(59, 130, 246, 0.12)"))
        title = c.get("title", "")
        val = c.get("value", "")
        sub = c.get("subtext", "")
        badge = c.get("badge", "")

        html.append(f"""
        <div style="background: #1E293B; border: 1px solid #334155; border-radius: 10px; padding: 10px 12px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-size: 11px; font-weight: 500; color: #94A3B8;">{title}</span>
                <span style="font-size: 9px; font-weight: 600; padding: 2px 6px; border-radius: 4px; background: {bg}; color: {color};">{badge}</span>
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #F8FAFC; margin: 2px 0;">{val}</div>
            <div style="font-size: 10px; color: {color}; font-weight: 500;">{sub}</div>
        </div>
        """)

    html.append("</div>")
    return "".join(html)


def build_strategy_markdown(analysis: Optional[Dict[str, Any]] = None) -> str:
    """
    Renders structured Market Scenarios & Actionable Strategy setup.
    """
    if not analysis:
        return "💡 *No active stock selected. Query a stock to display educational trading scenarios.*"

    st = analysis.get("strategy", {})
    sc = analysis.get("scenarios", {})
    q = analysis.get("quote", {})
    curr = q.get("currency_symbol", "₹")

    bull = sc.get("bullish", {})
    base = sc.get("base", {})
    bear = sc.get("bearish", {})

    return f"""
### 📋 Tactical Setup & Market Scenarios for {q.get('name', '')} ({q.get('symbol', '')})

**Strategic Bias:** `{st.get('bias', 'Neutral')}` &nbsp;|&nbsp; **Risk/Reward Ratio:** `{st.get('risk_reward_ratio', 1.0):.2f}`

* **Target Resistance:** `{curr}{st.get('resistance_target', 0):,.2f}`
* **Target Support:** `{curr}{st.get('support_target', 0):,.2f}`
* **Model Invalidation Floor:** `{curr}{st.get('invalidation_level', 0):,.2f}`

#### 🎯 Scenario Probability Matrix
* 🟢 **Bullish Case ({bull.get('probability', 0)}% Prob):** Target `{curr}{bull.get('target', 0):,.2f}` — *{bull.get('catalyst', '')}*
* 🟡 **Base Case ({base.get('probability', 0)}% Prob):** Target `{curr}{base.get('target', 0):,.2f}` — *{base.get('catalyst', '')}*
* 🔴 **Bearish Case ({bear.get('probability', 0)}% Prob):** Target `{curr}{bear.get('target', 0):,.2f}` — *{bear.get('catalyst', '')}*

> **Technical Reasoning:** {st.get('bias_reasoning', '')}
> 
> 🎓 **Educational Takeaway:** {st.get('educational_takeaway', '')}
"""


def build_comparison_markdown(comparison: Optional[Dict[str, Any]] = None) -> str:
    """
    Renders side-by-side comparison metrics in Markdown.
    """
    if not comparison:
        return "💡 *Ask something like 'Compare TCS and Infosys' to display head-to-head comparison metrics.*"

    sa = comparison.get("stock_a", {})
    sb = comparison.get("stock_b", {})
    corr = comparison.get("correlation", 0.0)

    cur_a = sa.get("currency_symbol", "₹")
    cur_b = sb.get("currency_symbol", "₹")

    return f"""
### ⚔️ Head-to-Head Quantitative Comparison: {sa.get('name')} vs {sb.get('name')}

| Metric | {sa.get('name')} ({sa.get('symbol')}) | {sb.get('name')} ({sb.get('symbol')}) |
| :--- | :--- | :--- |
| **Current Price** | `{cur_a}{sa.get('price', 0):,.2f}` ({sa.get('change_pct', 0):+.2f}%) | `{cur_b}{sb.get('price', 0):,.2f}` ({sb.get('change_pct', 0):+.2f}%) |
| **1-Year Return** | `{sa.get('return_1y', 0):+.2f}%` | `{sb.get('return_1y', 0):+.2f}%` |
| **Annualized Volatility** | `{sa.get('volatility', 0):.2f}%` | `{sb.get('volatility', 0):.2f}%` |
| **Max Drawdown** | `{sa.get('max_drawdown', 0):.2f}%` | `{sb.get('max_drawdown', 0):.2f}%` |
| **Sharpe Ratio** | `{sa.get('sharpe', 0):.2f}` | `{sb.get('sharpe', 0):.2f}` |
| **RSI (14) Momentum** | `{sa.get('rsi', 0):.1f}` | `{sb.get('rsi', 0):.1f}` |
| **Trend Bias** | `{sa.get('trend')}` | `{sb.get('trend')}` |
| **Risk Rating** | `{sa.get('risk_level')}` | `{sb.get('risk_level')}` |
| **Market Capitalization** | `{sa.get('market_cap')}` | `{sb.get('market_cap')}` |

**Benchmark Correlation:** `{corr:.2f}` (Statistically aligns with broad index move)
"""
