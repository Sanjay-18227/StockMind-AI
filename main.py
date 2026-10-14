"""
StockMind AI — FastAPI Main Application Server
Serves static frontend assets, handles conversational AI queries,
provides live market overviews, and streams full quantitative stock analyses.
"""

import os
import sys
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai.language import detect_language
from ai.intent import classify_intent
from ai.assistant import (
    format_market_overview_response,
    format_stock_analysis_response,
    format_comparison_response,
    generate_comparison_analysis,
    format_conversational_response
)
from data.global_market_data import get_market_overview
from data.market_data import resolve_ticker
from data.companies import get_all_companies, search_companies, get_categories, get_company_by_symbol
from model.live_signal import run_complete_stock_analysis

app = FastAPI(
    title="StockMind AI",
    description="Quantitative Financial Assistant & ML Prediction Platform",
    version="1.0.0"
)

# Enable CORS for local dev / flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    query: str = Field(..., description="User question or query text")
    active_symbol: Optional[str] = Field("TCS.NS", description="Currently focused ticker symbol")
    timeframe: Optional[str] = Field("1y", description="Requested historical timeframe (1d, 5d, 1mo, 1y, etc.)")


@app.get("/")
async def serve_index():
    """Serve the main single-page application."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "StockMind AI API is active. index.html not found."}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "StockMind AI"}


@app.get("/api/market-overview")
async def market_overview():
    """Fetch broad market pulse across domestic (NIFTY, SENSEX) and global indices."""
    try:
        overview = get_market_overview()
        return JSONResponse(content=overview)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch market overview: {str(e)}")
@app.get("/api/companies")
async def get_companies():
    """Return all indexed companies and assets."""
    return JSONResponse(content={"companies": get_all_companies()})


@app.get("/api/companies/search")
async def search_company_list(q: str = Query("", description="Search query")):
    """Instant search across company catalog."""
    return JSONResponse(content={"results": search_companies(q)})


@app.get("/api/companies/categories")
async def get_company_categories():
    """Grouped companies by sector/market category."""
    return JSONResponse(content={"categories": get_categories()})



@app.get("/api/stock/{symbol}")
async def get_stock_data(symbol: str, timeframe: str = Query("1y", pattern="^(1d|5d|1mo|3mo|6mo|1y|5y|max)$")):
    """
    Fetch complete quantitative analysis, indicators, and ML forecast for a single stock.
    Used for timeframe switcher and direct symbol inspection.
    """
    try:
        ticker = resolve_ticker(symbol)
        analysis = run_complete_stock_analysis(ticker, period=timeframe)
        return JSONResponse(content={
            "quote": analysis["quote"],
            "chart_payload": analysis["chart_payload"],
            "dashboard_cards": analysis["dashboard_cards"],
            "analysis": analysis
        })
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing {symbol}: {str(e)}")


@app.post("/api/chat")
async def process_chat(req: ChatRequest):
    """
    Main Conversational Assistant Endpoint:
    Automatically detects user language (English, Tamil, Tanglish, Hindi),
    parses intents & tickers, and returns a tailored markdown narrative
    coupled with structured visualization payloads.
    """
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # 1. Language Detection
    lang = detect_language(query)

    # 2. Intent Classification & Entity Extraction
    active_sym = req.active_symbol or "TCS.NS"
    parsed = classify_intent(query, active_symbol=active_sym)
    intent = parsed["intent"]
    primary_sym = parsed.get("primary_symbol") or active_sym
    secondary_sym = parsed.get("secondary_symbol")
    tf = parsed.get("timeframe") or req.timeframe or "1y"

    # 3. Handle Greetings & General Conversational Queries
    if intent in ["GENERAL_GREETING", "GENERAL_HOW_ARE_YOU", "GENERAL_CAPABILITIES", "GENERAL_OFF_TOPIC", "GENERAL_CONVERSATION"] and not parsed.get("symbols"):
        msg = format_conversational_response(intent, lang)
        return JSONResponse(content={
            "text_response": msg,
            "stock_analysis": None,
            "comparison": None,
            "market_overview": None,
            "intent": intent,
            "language": lang
        })

    # 4. Handle Market Overview Intent
    if intent == "MARKET_OVERVIEW":
        try:
            overview = get_market_overview()
            text_response = format_market_overview_response(overview, lang)
            return JSONResponse(content={
                "text_response": text_response,
                "stock_analysis": None,
                "comparison": None,
                "market_overview": overview,
                "intent": intent,
                "language": lang
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Market overview unavailable: {str(e)}")

    # 5. Handle Stock Comparison Intent
    if intent == "STOCK_COMPARISON":
        try:
            if not secondary_sym:
                # Default comparison pair if user only provided one symbol
                secondary_sym = "INFY.NS" if "TCS" in primary_sym else "TCS.NS"

            comp_data = generate_comparison_analysis(primary_sym, secondary_sym, timeframe=tf)
            text_response = format_comparison_response(comp_data, lang)
            return JSONResponse(content={
                "text_response": text_response,
                "comparison": comp_data,
                "stock_analysis": None,
                "market_overview": None,
                "intent": intent,
                "language": lang
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

    # 6. Handle Single Stock Analysis (All stock-focused intents)
    try:
        resolved = resolve_ticker(primary_sym)
        analysis = run_complete_stock_analysis(resolved, period=tf)
        text_response = format_stock_analysis_response(analysis, intent, lang)

        return JSONResponse(content={
            "text_response": text_response,
            "stock_analysis": analysis,
            "comparison": None,
            "market_overview": None,
            "intent": intent,
            "language": lang
        })
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to process query for '{primary_sym}'. Error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
