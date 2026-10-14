"""
Market Data Engine: Fetches real-time, delayed, and historical stock data.
Provides robust ticker resolution for Indian (NSE/BSE) and global markets.
"""

import yfinance as yf
import pandas as pd
import requests
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from utils.helpers import cache, safe_float, get_market_status
from data.companies import build_catalog_alias_map, search_companies, get_company_by_symbol

# Curated alias map for comprehensive coverage across Indian (NSE/BSE), US/Global markets, and Multilingual queries
COMMON_ALIASES = {
    # --- NIFTY 50 & MAJOR INDIAN BLUECHIPS ---
    "tcs": "TCS.NS",
    "tata consultancy services": "TCS.NS",
    "tata consultancy": "TCS.NS",
    "reliance": "RELIANCE.NS",
    "reliance industries": "RELIANCE.NS",
    "ril": "RELIANCE.NS",
    "infosys": "INFY.NS",
    "infy": "INFY.NS",
    "hdfc": "HDFCBANK.NS",
    "hdfc bank": "HDFCBANK.NS",
    "hdfcbank": "HDFCBANK.NS",
    "icici": "ICICIBANK.NS",
    "icici bank": "ICICIBANK.NS",
    "icicibank": "ICICIBANK.NS",
    "sbi": "SBIN.NS",
    "state bank of india": "SBIN.NS",
    "state bank": "SBIN.NS",
    "sbin": "SBIN.NS",
    "itc": "ITC.NS",
    "itc ltd": "ITC.NS",
    "tata motors": "TATAMOTORS.NS",
    "tatamotors": "TATAMOTORS.NS",
    "tata steel": "TATASTEEL.NS",
    "tatasteel": "TATASTEEL.NS",
    "titan": "TITAN.NS",
    "titan company": "TITAN.NS",
    "l&t": "LT.NS",
    "lt": "LT.NS",
    "larson & toubro": "LT.NS",
    "larsen and toubro": "LT.NS",
    "larsen & toubro": "LT.NS",
    "bharti airtel": "BHARTIARTL.NS",
    "airtel": "BHARTIARTL.NS",
    "bharti": "BHARTIARTL.NS",
    "bhartiartl": "BHARTIARTL.NS",
    "wipro": "WIPRO.NS",
    "hcl tech": "HCLTECH.NS",
    "hcl": "HCLTECH.NS",
    "hcl technologies": "HCLTECH.NS",
    "hcltech": "HCLTECH.NS",
    "maruti": "MARUTI.NS",
    "maruti suzuki": "MARUTI.NS",
    "asian paints": "ASIANPAINT.NS",
    "asian paint": "ASIANPAINT.NS",
    "asianpaint": "ASIANPAINT.NS",
    "bajaj finance": "BAJFINANCE.NS",
    "bajfinance": "BAJFINANCE.NS",
    "sun pharma": "SUNPHARMA.NS",
    "sunpharma": "SUNPHARMA.NS",
    "kotak": "KOTAKBANK.NS",
    "kotak bank": "KOTAKBANK.NS",
    "kotak mahindra": "KOTAKBANK.NS",
    "kotak mahindra bank": "KOTAKBANK.NS",
    "kotakbank": "KOTAKBANK.NS",
    "axis bank": "AXISBANK.NS",
    "axis": "AXISBANK.NS",
    "axisbank": "AXISBANK.NS",
    "m&m": "M&M.NS",
    "mahindra": "M&M.NS",
    "mahindra & mahindra": "M&M.NS",
    "mahindra and mahindra": "M&M.NS",
    "hindustan unilever": "HINDUNILVR.NS",
    "hul": "HINDUNILVR.NS",
    "unilever": "HINDUNILVR.NS",
    "hindunilvr": "HINDUNILVR.NS",
    "ntpc": "NTPC.NS",
    "power grid": "POWERGRID.NS",
    "powergrid": "POWERGRID.NS",
    "coal india": "COALINDIA.NS",
    "coalindia": "COALINDIA.NS",
    "ultratech": "ULTRACEMCO.NS",
    "ultratech cement": "ULTRACEMCO.NS",
    "ultracemco": "ULTRACEMCO.NS",
    "bajaj finserv": "BAJAJFINSV.NS",
    "bajajfinsv": "BAJAJFINSV.NS",
    "adani enterprises": "ADANIENT.NS",
    "adanient": "ADANIENT.NS",
    "adani ports": "ADANIPORTS.NS",
    "adani port": "ADANIPORTS.NS",
    "adanimports": "ADANIPORTS.NS",
    "ongc": "ONGC.NS",
    "oil and natural gas": "ONGC.NS",
    "bel": "BEL.NS",
    "bharat electronics": "BEL.NS",
    "trent": "TRENT.NS",
    "zudio": "TRENT.NS",
    "westside": "TRENT.NS",
    "grasim": "GRASIM.NS",
    "hindalco": "HINDALCO.NS",
    "jsw steel": "JSWSTEEL.NS",
    "jswsteel": "JSWSTEEL.NS",
    "tech mahindra": "TECHM.NS",
    "techm": "TECHM.NS",
    "nestle": "NESTLEIND.NS",
    "nestle india": "NESTLEIND.NS",
    "nestleind": "NESTLEIND.NS",
    "cipla": "CIPLA.NS",
    "dr reddy": "DRREDDY.NS",
    "dr reddy's": "DRREDDY.NS",
    "drreddy": "DRREDDY.NS",
    "apollo hospitals": "APOLLOHOSP.NS",
    "apollo hospital": "APOLLOHOSP.NS",
    "apollohosp": "APOLLOHOSP.NS",
    "tata consumer": "TATACONSUM.NS",
    "tataconsum": "TATACONSUM.NS",
    "shriram finance": "SHRIRAMFIN.NS",
    "shriramfin": "SHRIRAMFIN.NS",
    "hero motocorp": "HEROMOTOCO.NS",
    "hero": "HEROMOTOCO.NS",
    "heromotoco": "HEROMOTOCO.NS",
    "bpcl": "BPCL.NS",
    "bharat petroleum": "BPCL.NS",
    "eicher motors": "EICHERMOT.NS",
    "eicher": "EICHERMOT.NS",
    "royal enfield": "EICHERMOT.NS",
    "eichermot": "EICHERMOT.NS",
    "divis": "DIVISLAB.NS",
    "divi's": "DIVISLAB.NS",
    "divislab": "DIVISLAB.NS",
    "indusind": "INDUSINDBK.NS",
    "indusind bank": "INDUSINDBK.NS",
    "indusindbk": "INDUSINDBK.NS",
    "ltimindtree": "LTIM.NS",
    "ltim": "LTIM.NS",
    "mindtree": "LTIM.NS",
    "bajaj auto": "BAJAJ-AUTO.NS",
    "bajaj-auto": "BAJAJ-AUTO.NS",
    "britannia": "BRITANNIA.NS",

    # --- POPULAR GROWTH, MIDCAP, PSUs & NEW-AGE INDIAN STOCKS ---
    "zomato": "ZOMATO.NS",
    "blinkit": "ZOMATO.NS",
    "swiggy": "SWIGGY.NS",
    "instamart": "SWIGGY.NS",
    "jio": "JIOFIN.NS",
    "jio financial": "JIOFIN.NS",
    "jiofin": "JIOFIN.NS",
    "paytm": "PAYTM.NS",
    "one97": "PAYTM.NS",
    "nykaa": "NYKAA.NS",
    "policybazaar": "POLICYBZR.NS",
    "pb fintech": "POLICYBZR.NS",
    "delhivery": "DELHIVERY.NS",
    "ola electric": "OLAELEC.NS",
    "ola": "OLAELEC.NS",
    "hal": "HAL.NS",
    "hindustan aeronautics": "HAL.NS",
    "bhel": "BHEL.NS",
    "rvnl": "RVNL.NS",
    "rail vikas": "RVNL.NS",
    "rail vikas nigam": "RVNL.NS",
    "irfc": "IRFC.NS",
    "indian railway finance": "IRFC.NS",
    "irctc": "IRCTC.NS",
    "suzlon": "SUZLON.NS",
    "suzlon energy": "SUZLON.NS",
    "tata power": "TATAPOWER.NS",
    "tatapower": "TATAPOWER.NS",
    "adani power": "ADANIPOWER.NS",
    "adanipower": "ADANIPOWER.NS",
    "adani green": "ADANIGREEN.NS",
    "adanigreen": "ADANIGREEN.NS",
    "adani total gas": "ATGL.NS",
    "atgl": "ATGL.NS",
    "adani wilmar": "AWL.NS",
    "awl": "AWL.NS",
    "vedanta": "VEDL.NS",
    "vedl": "VEDL.NS",
    "dmart": "DMART.NS",
    "d-mart": "DMART.NS",
    "avenue supermarts": "DMART.NS",
    "indigo": "INDIGO.NS",
    "interglobe aviation": "INDIGO.NS",
    "polycab": "POLYCAB.NS",
    "havells": "HAVELLS.NS",
    "dixon": "DIXON.NS",
    "dixon technologies": "DIXON.NS",
    "dlf": "DLF.NS",
    "godrej properties": "GODREJPROP.NS",
    "godrejprop": "GODREJPROP.NS",
    "cdsl": "CDSL.NS",
    "bse": "BSE.NS",
    "bse limited": "BSE.NS",
    "angel one": "ANGELONE.NS",
    "angelone": "ANGELONE.NS",
    "mcx": "MCX.NS",
    "bank of baroda": "BANKBARODA.NS",
    "bob": "BANKBARODA.NS",
    "bankbaroda": "BANKBARODA.NS",
    "pnb": "PNB.NS",
    "punjab national bank": "PNB.NS",
    "canara bank": "CANBK.NS",
    "canbk": "CANBK.NS",
    "idfc first": "IDFCFIRSTB.NS",
    "idfc first bank": "IDFCFIRSTB.NS",
    "idfc": "IDFCFIRSTB.NS",
    "idfcbank": "IDFCFIRSTB.NS",
    "federal bank": "FEDERALBNK.NS",
    "federalbnk": "FEDERALBNK.NS",
    "yes bank": "YESBANK.NS",
    "yesbank": "YESBANK.NS",
    "ireda": "IREDA.NS",
    "nhpc": "NHPC.NS",
    "mazagon dock": "MAZDOCK.NS",
    "mazdock": "MAZDOCK.NS",
    "cochin shipyard": "COCHINSHIP.NS",
    "cochinship": "COCHINSHIP.NS",
    "gail": "GAIL.NS",
    "indian oil": "IOC.NS",
    "ioc": "IOC.NS",
    "hpcl": "HPCL.NS",
    "oil india": "OIL.NS",
    "pidilite": "PIDILITIND.NS",
    "fevicol": "PIDILITIND.NS",
    "pidilitind": "PIDILITIND.NS",
    "berger paints": "BERGEPAINT.NS",
    "berger": "BERGEPAINT.NS",
    "siemens": "SIEMENS.NS",
    "abb": "ABB.NS",
    "cg power": "CGPOWER.NS",
    "cummins": "CUMMINSIND.NS",
    "persistent": "PERSISTENT.NS",
    "persistent systems": "PERSISTENT.NS",
    "coforge": "COFORGE.NS",
    "mphasis": "MPHASIS.NS",
    "tata elxsi": "TATAELXSI.NS",
    "tataelxsi": "TATAELXSI.NS",
    "kpit": "KPITTECH.NS",
    "kpit tech": "KPITTECH.NS",
    "varun beverages": "VBL.NS",
    "vbl": "VBL.NS",
    "dabur": "DABUR.NS",
    "marico": "MARICO.NS",
    "parachute": "MARICO.NS",
    "godrej consumer": "GODREJCP.NS",
    "godrejcp": "GODREJCP.NS",
    "colgate": "COLPAL.NS",
    "colpal": "COLPAL.NS",
    "ambuja": "AMBUJACEM.NS",
    "ambuja cement": "AMBUJACEM.NS",
    "acc": "ACC.NS",
    "shree cement": "SHREECEM.NS",
    "lupin": "LUPIN.NS",
    "torrent pharma": "TORNTPHARM.NS",
    "aurobindo": "AUROPHARMA.NS",
    "biocon": "BIOCON.NS",
    "zydus": "ZYDUSLIFE.NS",
    "mankind": "MANKIND.NS",
    "mankind pharma": "MANKIND.NS",
    "max healthcare": "MAXHEALTH.NS",
    "lic": "LICI.NS",
    "lici": "LICI.NS",
    "sbi life": "SBILIFE.NS",
    "sbilife": "SBILIFE.NS",
    "hdfc life": "HDFCLIFE.NS",
    "hdfclife": "HDFCLIFE.NS",
    "muthoot": "MUTHOOTFIN.NS",
    "muthoot finance": "MUTHOOTFIN.NS",
    "rec": "REC.NS",
    "pfc": "PFC.NS",
    "power finance": "PFC.NS",
    "cholamandalam": "CHOLAFIN.NS",
    "chola": "CHOLAFIN.NS",
    "kalyan jewellers": "KALYANKJIL.NS",
    "kalyan": "KALYANKJIL.NS",
    "page industries": "PAGEIND.NS",
    "jockey": "PAGEIND.NS",
    "lodha": "LODHA.NS",
    "oberoi realty": "OBEROIRLTY.NS",
    "prestige": "PRESTIGE.NS",
    "tvs motor": "TVSMOTOR.NS",
    "tvs": "TVSMOTOR.NS",
    "ashok leyland": "ASHOKLEY.NS",
    "bharat forge": "BHARATFORG.NS",
    "motherson": "MOTHERSON.NS",
    "jindal steel": "JINDALSTEL.NS",
    "sail": "SAIL.NS",
    "nmdc": "NMDC.NS",
    "national aluminium": "NATIONALUM.NS",
    "voltas": "VOLTAS.NS",
    "blue star": "BLUESTARCO.NS",

    # --- MAJOR INDICES & COMMODITIES ---
    "nifty": "^NSEI",
    "nifty 50": "^NSEI",
    "nifty50": "^NSEI",
    "sensex": "^BSESN",
    "bse sensex": "^BSESN",
    "nifty bank": "^NSEBANK",
    "bank nifty": "^NSEBANK",
    "banknifty": "^NSEBANK",
    "nifty it": "^CNXIT",
    "nifty auto": "^CNXAUTO",
    "nifty pharma": "^CNXPHARMA",
    "nifty fmcg": "^CNXFMCG",
    "nifty metal": "^CNXMETAL",
    "gold": "GC=F",
    "silver": "SI=F",
    "crude oil": "CL=F",
    "crude": "CL=F",
    "oil": "CL=F",
    "bitcoin": "BTC-USD",
    "btc": "BTC-USD",
    "ethereum": "ETH-USD",
    "eth": "ETH-USD",

    # --- US & GLOBAL TECH / MEGA-CAP GIANTS ---
    "apple": "AAPL",
    "aapl": "AAPL",
    "iphone": "AAPL",
    "microsoft": "MSFT",
    "msft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "googl": "GOOGL",
    "goog": "GOOGL",
    "amazon": "AMZN",
    "amzn": "AMZN",
    "tesla": "TSLA",
    "tsla": "TSLA",
    "nvidia": "NVDA",
    "nvda": "NVDA",
    "meta": "META",
    "facebook": "META",
    "instagram": "META",
    "netflix": "NFLX",
    "nflx": "NFLX",
    "amd": "AMD",
    "intel": "INTC",
    "intc": "INTC",
    "qualcomm": "QCOM",
    "qcom": "QCOM",
    "broadcom": "AVGO",
    "avgo": "AVGO",
    "micron": "MU",
    "tsmc": "TSM",
    "tsm": "TSM",
    "asml": "ASML",
    "arm": "ARM",
    "berkshire": "BRK-B",
    "berkshire hathaway": "BRK-B",
    "jpmorgan": "JPM",
    "jpm": "JPM",
    "bank of america": "BAC",
    "bofa": "BAC",
    "bac": "BAC",
    "visa": "V",
    "mastercard": "MA",
    "walmart": "WMT",
    "wmt": "WMT",
    "costco": "COST",
    "coca cola": "KO",
    "coke": "KO",
    "pepsi": "PEP",
    "pepsico": "PEP",
    "mcdonalds": "MCD",
    "mcdonald's": "MCD",
    "nike": "NKE",
    "disney": "DIS",
    "boeing": "BA",
    "eli lilly": "LLY",
    "novo nordisk": "NVO",
    "pfizer": "PFE",
    "johnson & johnson": "JNJ",
    "exxon": "XOM",
    "exxonmobil": "XOM",
    "chevron": "CVX",
    "toyota": "TM",
    "alibaba": "BABA",
    "sony": "SONY",
    "palantir": "PLTR",
    "pltr": "PLTR",
    "uber": "UBER",
    "coinbase": "COIN",
    "snowflake": "SNOW",
    "salesforce": "CRM",
    "s&p 500": "^GSPC",
    "sp500": "^GSPC",
    "s&p": "^GSPC",
    "nasdaq": "^IXIC",
    "dow": "^DJI",
    "dow jones": "^DJI",

    # --- TAMIL SCRIPT ALIASES ---
    "டிசிஎஸ்": "TCS.NS",
    "டாடா மோட்டார்ஸ்": "TATAMOTORS.NS",
    "டாடா ஸ்டீல்": "TATASTEEL.NS",
    "டாடா பவர்": "TATAPOWER.NS",
    "ரிலையன்ஸ்": "RELIANCE.NS",
    "ரிலையன்ஸ் இண்டஸ்ட்ரீஸ்": "RELIANCE.NS" ,
    "இன்போசிஸ்": "INFY.NS",
    "ஹெச்டிஎஃப்சி": "HDFCBANK.NS",
    "ஹெச்டிஎஃப்சி வங்கி": "HDFCBANK.NS",
    "ஐசிஐசிஐ": "ICICIBANK.NS",
    "ஸ்டேட் பாங்க்": "SBIN.NS",
    "எஸ்பிஐ": "SBIN.NS",
    "ஐடிசி": "ITC.NS",
    "ஏர்டெல்": "BHARTIARTL.NS",
    "விப்ரோ": "WIPRO.NS",
    "அடானி": "ADANIENT.NS",
    "அதானி": "ADANIENT.NS",
    "சோமேட்டோ": "ZOMATO.NS",
    "ஜோமேட்டோ": "ZOMATO.NS",
    "ஜியோ": "JIOFIN.NS",
    "பேடிஎம்": "PAYTM.NS",
    "ஸ்விக்கி": "SWIGGY.NS",
    "டைட்டன்": "TITAN.NS",
    "மாருதி": "MARUTI.NS",
    "நிப்டி": "^NSEI",
    "சென்செக்ஸ்": "^BSESN",
    "தங்கம்": "GC=F",
    "வெள்ளி": "SI=F",
    "ஆப்பிள்": "AAPL",
    "டெஸ்லா": "TSLA",
    "கூகிள்": "GOOGL",
    "மைக்ரோசாப்ட்": "MSFT",
    "என்விடியா": "NVDA",
    "அமேசான்": "AMZN",

    # --- HINDI SCRIPT ALIASES ---
    "टीसीएस": "TCS.NS",
    "टाटा मोटर्स": "TATAMOTORS.NS",
    "टाटा स्टील": "TATASTEEL.NS",
    "टाटा पावर": "TATAPOWER.NS",
    "रिलायंस": "RELIANCE.NS",
    "इंफोसिस": "INFY.NS",
    "एचडीएफसी": "HDFCBANK.NS",
    "आईसीआईसीआई": "ICICIBANK.NS",
    "एसबीआई": "SBIN.NS",
    "आईटीसी": "ITC.NS",
    "एयरटेल": "BHARTIARTL.NS",
    "विप्रो": "WIPRO.NS",
    "अडानी": "ADANIENT.NS",
    "जोमैटो": "ZOMATO.NS",
    "जियो": "JIOFIN.NS",
    "पेटीएम": "PAYTM.NS",
    "स्विगी": "SWIGGY.NS",
    "टाइटन": "TITAN.NS",
    "मारुति": "MARUTI.NS",
    "निफ्टी": "^NSEI",
    "सेंसेक्स": "^BSESN",
    "सोना": "GC=F",
    "चांदी": "SI=F",
    "एप्पल": "AAPL",
    "टेस्ला": "TSLA",
    "गूगल": "GOOGL",
    "माइक्रोसॉफ्ट": "MSFT",
    "एनवीडिया": "NVDA",
    "अमेज़न": "AMZN"
}

# Merge dynamically with comprehensive company catalog aliases
try:
    COMMON_ALIASES.update(build_catalog_alias_map())
except Exception:
    pass

def resolve_ticker(query: str) -> str:
    """
    Resolve natural language query or symbol to an exchange ticker symbol.
    Prefers NSE (.NS) for ambiguous Indian tickers, NASDAQ/NYSE for US.
    """
    cleaned = query.strip().lower()
    
    # 1. Direct alias match
    if cleaned in COMMON_ALIASES:
        return COMMON_ALIASES[cleaned]
    
    # 2. Check without punctuation
    no_punct = cleaned.replace(".", "").replace(",", "").replace("-", " ")
    if no_punct in COMMON_ALIASES:
        return COMMON_ALIASES[no_punct]
        
    # 3. If user already provided ticker with exchange/type suffix (e.g., TCS.NS, RELIANCE.BO, GC=F, ^NSEI)
    raw_upper = query.strip().upper()
    if "." in raw_upper or raw_upper.startswith("^") or "=" in raw_upper or ("-" in raw_upper and not raw_upper.startswith("-")):
        return raw_upper
        
    # 4. Check if raw uppercase exists in aliases
    if raw_upper.lower() in COMMON_ALIASES:
        return COMMON_ALIASES[raw_upper.lower()]

    # 5. Check catalog search
    catalog_matches = search_companies(query, limit=3)
    if catalog_matches:
        for cm in catalog_matches:
            if query.lower() in cm["name"].lower() or query.lower() in cm["ticker"].lower() or query.lower() in [a.lower() for a in cm.get("aliases", [])]:
                return cm["symbol"]

    # 6. If it's a known US tech/bluechip ticker
    US_TICKERS = {
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "NFLX",
        "AMD", "INTC", "QCOM", "AVGO", "MU", "TSM", "ASML", "ARM", "JPM", "BAC",
        "V", "MA", "WMT", "COST", "KO", "PEP", "MCD", "NKE", "DIS", "BA", "LLY",
        "NVO", "PFE", "JNJ", "XOM", "CVX", "BABA", "TM", "SONY", "PLTR", "UBER", "COIN",
        "CRM", "ORCL", "ADBE", "CSCO", "IBM", "SPOT", "ABNB", "PYPL", "SHOP", "SMCI", "MSTR"
    }
    if raw_upper in US_TICKERS:
        return raw_upper

    # 7. Check if catalog exact ticker match
    for cm in catalog_matches:
        if cm["ticker"].upper() == raw_upper:
            return cm["symbol"]

    # 8. Try online search lookup with Yahoo Finance quote endpoint
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={requests.utils.quote(query)}&quotesCount=5"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=3)
        if r.status_code == 200:
            data = r.json()
            quotes = data.get("quotes", [])
            if quotes:
                # Prioritize equity quotes
                for q in quotes:
                    sym = q.get("symbol", "")
                    if sym and not sym.startswith("="):
                        return sym
    except Exception:
        pass

    # 9. Default fallback: If uppercase and no dot, add .NS if it looks like an Indian ticker
    if raw_upper.isalpha() and len(raw_upper) >= 2:
        return f"{raw_upper}.NS"

    return raw_upper


def get_stock_quote(symbol: str) -> Dict[str, Any]:
    """
    Fetch comprehensive current/latest quote information for a given symbol.
    """
    cache_key = f"quote_{symbol.upper()}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    ticker = yf.Ticker(symbol)
    
    # Attempt fast_info first (faster & reliable)
    fi = getattr(ticker, "fast_info", None)
    current_price = 0.0
    prev_close = 0.0
    day_high = 0.0
    day_low = 0.0
    day_open = 0.0
    market_cap = 0.0
    fifty_two_high = 0.0
    fifty_two_low = 0.0
    volume = 0.0
    currency = "INR" if (".NS" in symbol.upper() or ".BO" in symbol.upper() or "^NSE" in symbol.upper() or "^BSE" in symbol.upper()) else "USD"
    
    if fi:
        try:
            current_price = safe_float(fi.last_price)
            prev_close = safe_float(fi.previous_close)
            day_high = safe_float(fi.day_high)
            day_low = safe_float(fi.day_low)
            day_open = safe_float(fi.open)
            market_cap = safe_float(fi.market_cap)
            fifty_two_high = safe_float(fi.year_high)
            fifty_two_low = safe_float(fi.year_low)
            volume = safe_float(fi.last_volume)
            currency = str(getattr(fi, "currency", currency))
        except Exception:
            pass

    # Fallback to history if current_price is 0
    df = ticker.history(period="5d")
    if current_price == 0.0 and not df.empty:
        current_price = safe_float(df["Close"].iloc[-1])
        prev_close = safe_float(df["Close"].iloc[-2]) if len(df) > 1 else current_price
        day_high = safe_float(df["High"].iloc[-1])
        day_low = safe_float(df["Low"].iloc[-1])
        day_open = safe_float(df["Open"].iloc[-1])
        volume = safe_float(df["Volume"].iloc[-1])
        
    if df.empty and current_price == 0.0:
        raise ValueError(f"No market data available for symbol '{symbol}'. Please check the ticker.")

    # Calculate change and percentage change
    if prev_close > 0:
        change = current_price - prev_close
        change_pct = (change / prev_close) * 100
    else:
        change = 0.0
        change_pct = 0.0

    # Fetch company info metadata if available
    name = symbol.upper()
    exchange = "NSE" if ".NS" in symbol.upper() else ("BSE" if ".BO" in symbol.upper() else "US")
    sector = "N/A"
    industry = "N/A"
    summary = ""
    pe_ratio = 0.0
    
    try:
        info = ticker.info
        if info:
            name = info.get("shortName") or info.get("longName") or symbol.upper()
            exchange = info.get("exchange", exchange)
            sector = info.get("sector", "N/A")
            industry = info.get("industry", "N/A")
            summary = info.get("longBusinessSummary", "")
            pe_ratio = safe_float(info.get("trailingPE", 0.0))
            if fifty_two_high == 0.0:
                fifty_two_high = safe_float(info.get("fiftyTwoWeekHigh", 0.0))
            if fifty_two_low == 0.0:
                fifty_two_low = safe_float(info.get("fiftyTwoWeekLow", 0.0))
            if market_cap == 0.0:
                market_cap = safe_float(info.get("marketCap", 0.0))
    except Exception:
        pass

    # Market status
    status_info = get_market_status(symbol)
    
    # Calculate 10-day average volume
    avg_vol = 0.0
    if not df.empty:
        avg_vol = safe_float(df["Volume"].mean())

    last_date_str = str(df.index[-1].strftime("%Y-%m-%d %H:%M:%S")) if not df.empty else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    quote_data = {
        "symbol": symbol.upper(),
        "name": name,
        "exchange": exchange,
        "currency": currency,
        "currency_symbol": "₹" if currency == "INR" else ("$" if currency == "USD" else currency),
        "current_price": round(current_price, 2),
        "prev_close": round(prev_close, 2),
        "open": round(day_open, 2),
        "day_high": round(day_high, 2),
        "day_low": round(day_low, 2),
        "change": round(change, 2),
        "change_percent": round(change_pct, 2),
        "52_week_high": round(fifty_two_high, 2),
        "52_week_low": round(fifty_two_low, 2),
        "volume": int(volume),
        "avg_volume": int(avg_vol),
        "market_cap": market_cap,
        "pe_ratio": round(pe_ratio, 2) if pe_ratio > 0 else "N/A",
        "sector": sector,
        "industry": industry,
        "summary": summary[:300] + "..." if len(summary) > 300 else summary,
        "last_updated": last_date_str,
        "market_status": status_info["status"],
        "market_status_detail": status_info["detail"],
        "is_market_open": status_info["is_open"],
        "local_time": status_info["local_time"]
    }
    
    # Cache for 60 seconds
    cache.set(cache_key, quote_data, ttl=60)
    return quote_data


def get_historical_data(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical OHLCV data for analysis and charts.
    Returns sanitized DataFrame with Open, High, Low, Close, Volume.
    """
    cache_key = f"hist_{symbol.upper()}_{period}_{interval}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    
    if df.empty:
        # Fallback for Indian stocks if queried without .NS
        if not symbol.endswith(".NS") and not symbol.endswith(".BO") and not symbol.startswith("^"):
            ticker = yf.Ticker(f"{symbol}.NS")
            df = ticker.history(period=period, interval=interval)
            
    if df.empty:
        raise ValueError(f"No historical price data found for {symbol} ({period}).")

    # Clean DataFrame: handle timezone, NaN values
    df.index = pd.to_datetime(df.index)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    # Ensure required columns exist
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' missing from price data.")

    # Drop any zero/NaN rows
    df = df[df["Close"] > 0].copy()
    df.ffill(inplace=True)
    df.bfill(inplace=True)

    # Cache for 10 minutes
    cache.set(cache_key, df, ttl=600)
    return df
