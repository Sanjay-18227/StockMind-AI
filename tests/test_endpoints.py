"""
Comprehensive Integration & Verification Tests for StockMind AI
Tests all API endpoints, multilingual intent routing, and quantitative pipelines.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath("."))

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from main import health_check, market_overview, get_stock_data, process_chat, ChatRequest

async def run_tests():
    print("=" * 60)
    print("StockMind AI - Comprehensive System Verification")
    print("=" * 60)

    # 1. Health check
    print("\n[1] Testing /api/health ...")
    h = await health_check()
    print("    Result:", h)
    assert h["status"] == "ok"
    print("    PASSED")

    # 2. General greeting
    print("\n[2] Testing General Multilingual Chat Greeting ...")
    chat_req = ChatRequest(query="Hello there", active_symbol="TCS.NS")
    res = await process_chat(chat_req)
    data = res.body.decode("utf-8")
    assert "StockMind AI" in data
    print("    Greeting Response length:", len(data), "bytes")
    print("    PASSED")

    # 3. Market overview endpoint & chat
    print("\n[3] Testing Market Overview ...")
    mo = await market_overview()
    assert mo.status_code == 200
    print("    Market overview status: 200 OK")

    chat_req = ChatRequest(query="How is the stock market today?", active_symbol="TCS.NS")
    res = await process_chat(chat_req)
    assert res.status_code == 200
    print("    Market overview chat: 200 OK")
    print("    PASSED")

    # 4. Stock Analysis (English)
    print("\n[4] Testing Stock Analysis Query (English: 'Analyze TCS') ...")
    chat_req = ChatRequest(query="Analyze TCS", active_symbol="TCS.NS")
    res = await process_chat(chat_req)
    assert res.status_code == 200
    print("    TCS analysis response status: 200 OK")
    print("    PASSED")

    # 5. Tanglish Stock Query
    print("\n[5] Testing Tanglish Stock Query ('TCS stock ippo epdi iruku?') ...")
    chat_req = ChatRequest(query="TCS stock ippo epdi iruku?", active_symbol="TCS.NS")
    res = await process_chat(chat_req)
    assert res.status_code == 200
    print("    Tanglish query response status: 200 OK")
    print("    PASSED")

    # 6. Tamil Script Stock Query
    print("\n[6] Testing Tamil Script Stock Query ('இந்த stock இப்ப எப்படி இருக்கு?') ...")
    chat_req = ChatRequest(query="இந்த stock இப்ப எப்படி இருக்கு?", active_symbol="TCS.NS")
    res = await process_chat(chat_req)
    assert res.status_code == 200
    import json
    data_ta = json.loads(res.body.decode("utf-8"))
    assert data_ta["intent"] == "STOCK_ANALYSIS"
    assert data_ta["stock_analysis"] is not None
    print("    Tamil script query response status: 200 OK (STOCK_ANALYSIS with full stock_analysis payload)")
    print("    PASSED")

    # 7. Stock Comparison Query
    print("\n[7] Testing Stock Comparison ('Compare TCS and Infosys') ...")
    chat_req = ChatRequest(query="Compare TCS and Infosys", active_symbol="TCS.NS")
    res = await process_chat(chat_req)
    assert res.status_code == 200
    print("    Comparison response status: 200 OK")
    print("    PASSED")

    # 8. Single Stock Timeframe Data
    print("\n[8] Testing /api/stock/TCS.NS?timeframe=1mo ...")
    res = await get_stock_data(symbol="TCS.NS", timeframe="1mo")
    assert res.status_code == 200
    print("    Timeframe data status: 200 OK")
    print("    PASSED")

    # 9. Companies Directory & Search
    print("\n[9] Testing 650+ Companies Catalog & Search ...")
    from main import get_companies, search_company_list, get_company_categories
    import json
    res_c = await get_companies()
    companies_data = json.loads(res_c.body.decode("utf-8"))
    assert len(companies_data["companies"]) >= 600, f"Expected 600+ companies, got {len(companies_data['companies'])}"
    print(f"    Total Catalog Companies: {len(companies_data['companies'])}")

    res_s = await search_company_list(q="Premier")
    search_data = json.loads(res_s.body.decode("utf-8"))
    assert any("Premier Energies" in c["name"] for c in search_data["results"])
    print("    Search 'Premier' matched:", [c["name"] for c in search_data["results"]])

    res_cat = await get_company_categories()
    cat_data = json.loads(res_cat.body.decode("utf-8"))
    assert len(cat_data["categories"]) >= 15
    print(f"    Total Market Categories: {len(cat_data['categories'])}")
    print("    PASSED")

    # 10. Stock Market Tips Query
    print("\n[10] Testing Stock Market Tips ('Give me stock market tips') ...")
    chat_req = ChatRequest(query="Give me stock market tips", active_symbol="TCS.NS")
    res = await process_chat(chat_req)
    assert res.status_code == 200
    tips_data = json.loads(res.body.decode("utf-8"))
    assert tips_data["intent"] == "STOCK_TIPS"
    assert "Rule" in tips_data["text_response"] or "Tip" in tips_data["text_response"]
    print("    Tips response length:", len(tips_data["text_response"]))
    print("    PASSED")

    # 11. Foreign Currency to INR Conversion Query
    print("\n[11] Testing Foreign Stock to INR Conversion ('Apple stock in indian rupees') ...")
    chat_req = ChatRequest(query="Apple stock in indian rupees", active_symbol="AAPL")
    res = await process_chat(chat_req)
    assert res.status_code == 200
    conv_data = json.loads(res.body.decode("utf-8"))
    assert conv_data["intent"] == "CURRENCY_CONVERSION"
    assert "INR" in conv_data["text_response"] or "USD" in conv_data["text_response"]
    print("    Currency conversion response status: 200 OK")
    print("    PASSED")

    print("\n" + "=" * 60)
    print("ALL INTEGRATION TESTS PASSED SUCCESSFULLY! 🚀")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_tests())
