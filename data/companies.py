"""
StockMind AI — Comprehensive Global & Indian Company Catalog
Includes NIFTY 50, NIFTY Next 50, high-growth midcaps, popular smallcaps,
PSUs, defence, railway, energy, consumer tech, and US/Global mega-caps.
"""

from typing import List, Dict, Any, Optional

COMPANIES: List[Dict[str, Any]] = [
    # =========================================================================
    # NIFTY 50 & MAJOR INDIAN BLUECHIPS
    # =========================================================================
    {
        "symbol": "TCS.NS",
        "name": "Tata Consultancy Services",
        "ticker": "TCS",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Information Technology",
        "category": "NIFTY 50",
        "aliases": ["tcs", "tata consultancy services", "tata consultancy", "டிசிஎஸ்", "टीसीएस"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "RELIANCE.NS",
        "name": "Reliance Industries",
        "ticker": "RELIANCE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Energy & Conglomerate",
        "category": "NIFTY 50",
        "aliases": ["reliance", "reliance industries", "ril", "ரிலையன்ஸ்", "रिलायंस"],
        "is_popular": True,
        "emoji": "🛢️"
    },
    {
        "symbol": "INFY.NS",
        "name": "Infosys Ltd",
        "ticker": "INFY",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Information Technology",
        "category": "NIFTY 50",
        "aliases": ["infosys", "infy", "இன்போசிஸ்", "इंफोसिस"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "HDFCBANK.NS",
        "name": "HDFC Bank Ltd",
        "ticker": "HDFCBANK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Banking & Financial Services",
        "category": "NIFTY 50",
        "aliases": ["hdfc", "hdfc bank", "hdfcbank", "ஹெச்டிஎஃப்சி", "एचडीएफसी"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "ICICIBANK.NS",
        "name": "ICICI Bank Ltd",
        "ticker": "ICICIBANK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Banking & Financial Services",
        "category": "NIFTY 50",
        "aliases": ["icici", "icici bank", "icicibank", "ஐசிஐசிஐ", "आईसीआईसीआई"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "SBIN.NS",
        "name": "State Bank of India",
        "ticker": "SBIN",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Banking & Financial Services",
        "category": "NIFTY 50",
        "aliases": ["sbi", "state bank of india", "state bank", "sbin", "ஸ்டேட் பாங்க்", "एसबीआई"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "ITC.NS",
        "name": "ITC Ltd",
        "ticker": "ITC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Consumer Goods & FMCG",
        "category": "NIFTY 50",
        "aliases": ["itc", "itc ltd", "ஐடிசி", "आईटीसी"],
        "is_popular": True,
        "emoji": "🚬"
    },
    {
        "symbol": "TATAMOTORS.NS",
        "name": "Tata Motors Ltd",
        "ticker": "TATAMOTORS",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Automobile & EV",
        "category": "NIFTY 50",
        "aliases": ["tata motors", "tatamotors", "tata motor", "டாடா மோட்டார்ஸ்", "टाटा मोटर्स"],
        "is_popular": True,
        "emoji": "🚗"
    },
    {
        "symbol": "TATASTEEL.NS",
        "name": "Tata Steel Ltd",
        "ticker": "TATASTEEL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Metals & Mining",
        "category": "NIFTY 50",
        "aliases": ["tata steel", "tatasteel", "டாடா ஸ்டீல்", "टाटा स्टील"],
        "is_popular": True,
        "emoji": "🏗️"
    },
    {
        "symbol": "TITAN.NS",
        "name": "Titan Company Ltd",
        "ticker": "TITAN",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Consumer Durables & Jewellery",
        "category": "NIFTY 50",
        "aliases": ["titan", "titan company", "tanishq", "fastrack", "டைட்டன்", "टाइटन"],
        "is_popular": True,
        "emoji": "⌚"
    },
    {
        "symbol": "LT.NS",
        "name": "Larsen & Toubro Ltd",
        "ticker": "LT",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Construction & Engineering",
        "category": "NIFTY 50",
        "aliases": ["l&t", "lt", "larson & toubro", "larsen and toubro", "larsen & toubro", "larsen"],
        "is_popular": True,
        "emoji": "🏗️"
    },
    {
        "symbol": "BHARTIARTL.NS",
        "name": "Bharti Airtel Ltd",
        "ticker": "BHARTIARTL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Telecommunications",
        "category": "NIFTY 50",
        "aliases": ["bharti airtel", "airtel", "bharti", "bhartiartl", "ஏர்டெல்", "एयरटेल"],
        "is_popular": True,
        "emoji": "📶"
    },
    {
        "symbol": "WIPRO.NS",
        "name": "Wipro Ltd",
        "ticker": "WIPRO",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Information Technology",
        "category": "NIFTY 50",
        "aliases": ["wipro", "wipro ltd", "விப்ரோ", "विप्रो"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "HCLTECH.NS",
        "name": "HCL Technologies Ltd",
        "ticker": "HCLTECH",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Information Technology",
        "category": "NIFTY 50",
        "aliases": ["hcl tech", "hcl", "hcl technologies", "hcltech"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "MARUTI.NS",
        "name": "Maruti Suzuki India Ltd",
        "ticker": "MARUTI",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Automobile",
        "category": "NIFTY 50",
        "aliases": ["maruti", "maruti suzuki", "suzuki india", "மாருதி", "मारुति"],
        "is_popular": True,
        "emoji": "🚗"
    },
    {
        "symbol": "ASIANPAINT.NS",
        "name": "Asian Paints Ltd",
        "ticker": "ASIANPAINT",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Consumer Goods & Paints",
        "category": "NIFTY 50",
        "aliases": ["asian paints", "asian paint", "asianpaint"],
        "is_popular": True,
        "emoji": "🎨"
    },
    {
        "symbol": "BAJFINANCE.NS",
        "name": "Bajaj Finance Ltd",
        "ticker": "BAJFINANCE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "NBFC & Financial Services",
        "category": "NIFTY 50",
        "aliases": ["bajaj finance", "bajfinance", "bajaj finserv nbfc"],
        "is_popular": True,
        "emoji": "💳"
    },
    {
        "symbol": "SUNPHARMA.NS",
        "name": "Sun Pharmaceutical Industries",
        "ticker": "SUNPHARMA",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Pharmaceuticals & Healthcare",
        "category": "NIFTY 50",
        "aliases": ["sun pharma", "sunpharma", "sun pharmaceutical"],
        "is_popular": True,
        "emoji": "💊"
    },
    {
        "symbol": "KOTAKBANK.NS",
        "name": "Kotak Mahindra Bank Ltd",
        "ticker": "KOTAKBANK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Banking & Financial Services",
        "category": "NIFTY 50",
        "aliases": ["kotak", "kotak bank", "kotak mahindra", "kotak mahindra bank", "kotakbank"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "AXISBANK.NS",
        "name": "Axis Bank Ltd",
        "ticker": "AXISBANK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Banking & Financial Services",
        "category": "NIFTY 50",
        "aliases": ["axis bank", "axis", "axisbank"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "M&M.NS",
        "name": "Mahindra & Mahindra Ltd",
        "ticker": "M&M",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Automobile & EV",
        "category": "NIFTY 50",
        "aliases": ["m&m", "mahindra", "mahindra & mahindra", "mahindra and mahindra"],
        "is_popular": True,
        "emoji": "🚜"
    },
    {
        "symbol": "HINDUNILVR.NS",
        "name": "Hindustan Unilever Ltd",
        "ticker": "HINDUNILVR",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Consumer Goods & FMCG",
        "category": "NIFTY 50",
        "aliases": ["hindustan unilever", "hul", "unilever", "hindunilvr"],
        "is_popular": True,
        "emoji": "🧼"
    },
    {
        "symbol": "NTPC.NS",
        "name": "NTPC Ltd",
        "ticker": "NTPC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Power & Energy",
        "category": "NIFTY 50",
        "aliases": ["ntpc", "national thermal power"],
        "is_popular": True,
        "emoji": "⚡"
    },
    {
        "symbol": "POWERGRID.NS",
        "name": "Power Grid Corporation of India",
        "ticker": "POWERGRID",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Power Transmission",
        "category": "NIFTY 50",
        "aliases": ["power grid", "powergrid", "pgcil"],
        "is_popular": True,
        "emoji": "⚡"
    },
    {
        "symbol": "COALINDIA.NS",
        "name": "Coal India Ltd",
        "ticker": "COALINDIA",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Mining & Minerals",
        "category": "NIFTY 50",
        "aliases": ["coal india", "coalindia", "cil"],
        "is_popular": True,
        "emoji": "⛏️"
    },
    {
        "symbol": "ULTRACEMCO.NS",
        "name": "UltraTech Cement Ltd",
        "ticker": "ULTRACEMCO",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Cement & Building Materials",
        "category": "NIFTY 50",
        "aliases": ["ultratech", "ultratech cement", "ultracemco"],
        "is_popular": True,
        "emoji": "🧱"
    },
    {
        "symbol": "BAJAJFINSV.NS",
        "name": "Bajaj Finserv Ltd",
        "ticker": "BAJAJFINSV",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Financial Services",
        "category": "NIFTY 50",
        "aliases": ["bajaj finserv", "bajajfinsv"],
        "is_popular": True,
        "emoji": "💳"
    },
    {
        "symbol": "ADANIENT.NS",
        "name": "Adani Enterprises Ltd",
        "ticker": "ADANIENT",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Conglomerate & Infrastructure",
        "category": "NIFTY 50",
        "aliases": ["adani enterprises", "adanient", "adani", "அடானி", "अडानी"],
        "is_popular": True,
        "emoji": "🏗️"
    },
    {
        "symbol": "ADANIPORTS.NS",
        "name": "Adani Ports & SEZ Ltd",
        "ticker": "ADANIPORTS",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Ports & Logistics",
        "category": "NIFTY 50",
        "aliases": ["adani ports", "adani port", "adanimports", "apsez"],
        "is_popular": True,
        "emoji": "🚢"
    },
    {
        "symbol": "ONGC.NS",
        "name": "Oil & Natural Gas Corporation",
        "ticker": "ONGC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Oil & Gas Exploration",
        "category": "NIFTY 50",
        "aliases": ["ongc", "oil and natural gas", "oil and natural gas corporation"],
        "is_popular": True,
        "emoji": "🛢️"
    },
    {
        "symbol": "BEL.NS",
        "name": "Bharat Electronics Ltd",
        "ticker": "BEL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Defence & Electronics",
        "category": "NIFTY 50",
        "aliases": ["bel", "bharat electronics", "bharat electronics ltd"],
        "is_popular": True,
        "emoji": "🛡️"
    },
    {
        "symbol": "TRENT.NS",
        "name": "Trent Ltd (Westside & Zudio)",
        "ticker": "TRENT",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Retail & Fashion",
        "category": "NIFTY 50",
        "aliases": ["trent", "zudio", "westside", "trent retail"],
        "is_popular": True,
        "emoji": "👗"
    },
    {
        "symbol": "GRASIM.NS",
        "name": "Grasim Industries Ltd",
        "ticker": "GRASIM",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Diversified & Chemicals",
        "category": "NIFTY 50",
        "aliases": ["grasim", "grasim industries", "birla opus"],
        "is_popular": False,
        "emoji": "🏭"
    },
    {
        "symbol": "HINDALCO.NS",
        "name": "Hindalco Industries Ltd",
        "ticker": "HINDALCO",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Metals & Aluminium",
        "category": "NIFTY 50",
        "aliases": ["hindalco", "hindalco industries", "novelis"],
        "is_popular": True,
        "emoji": "🥈"
    },
    {
        "symbol": "JSWSTEEL.NS",
        "name": "JSW Steel Ltd",
        "ticker": "JSWSTEEL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Metals & Mining",
        "category": "NIFTY 50",
        "aliases": ["jsw steel", "jswsteel", "jsw"],
        "is_popular": True,
        "emoji": "🏗️"
    },
    {
        "symbol": "TECHM.NS",
        "name": "Tech Mahindra Ltd",
        "ticker": "TECHM",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Information Technology",
        "category": "NIFTY 50",
        "aliases": ["tech mahindra", "techm", "techmahindra"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "NESTLEIND.NS",
        "name": "Nestle India Ltd",
        "ticker": "NESTLEIND",
        "exchange": "NSE",
        "country": "IN",
        "sector": "FMCG & Food Products",
        "category": "NIFTY 50",
        "aliases": ["nestle", "nestle india", "nestleind", "maggi"],
        "is_popular": True,
        "emoji": "🍜"
    },
    {
        "symbol": "CIPLA.NS",
        "name": "Cipla Ltd",
        "ticker": "CIPLA",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Pharmaceuticals",
        "category": "NIFTY 50",
        "aliases": ["cipla", "cipla ltd"],
        "is_popular": True,
        "emoji": "💊"
    },
    {
        "symbol": "DRREDDY.NS",
        "name": "Dr. Reddy's Laboratories",
        "ticker": "DRREDDY",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Pharmaceuticals",
        "category": "NIFTY 50",
        "aliases": ["dr reddy", "dr reddy's", "drreddy", "doctor reddy"],
        "is_popular": True,
        "emoji": "💊"
    },
    {
        "symbol": "APOLLOHOSP.NS",
        "name": "Apollo Hospitals Enterprise",
        "ticker": "APOLLOHOSP",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Healthcare Services",
        "category": "NIFTY 50",
        "aliases": ["apollo hospitals", "apollo hospital", "apollohosp", "apollo 247"],
        "is_popular": True,
        "emoji": "🏥"
    },
    {
        "symbol": "TATACONSUM.NS",
        "name": "Tata Consumer Products",
        "ticker": "TATACONSUM",
        "exchange": "NSE",
        "country": "IN",
        "sector": "FMCG & Beverages",
        "category": "NIFTY 50",
        "aliases": ["tata consumer", "tataconsum", "tata tea", "tata salt", "tetley"],
        "is_popular": True,
        "emoji": "☕"
    },
    {
        "symbol": "SHRIRAMFIN.NS",
        "name": "Shriram Finance Ltd",
        "ticker": "SHRIRAMFIN",
        "exchange": "NSE",
        "country": "IN",
        "sector": "NBFC & Commercial Finance",
        "category": "NIFTY 50",
        "aliases": ["shriram finance", "shriramfin", "shriram transport"],
        "is_popular": False,
        "emoji": "🚚"
    },
    {
        "symbol": "HEROMOTOCO.NS",
        "name": "Hero MotoCorp Ltd",
        "ticker": "HEROMOTOCO",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Automobile & Two-Wheelers",
        "category": "NIFTY 50",
        "aliases": ["hero motocorp", "hero", "heromotoco", "hero honda"],
        "is_popular": True,
        "emoji": "🏍️"
    },
    {
        "symbol": "BPCL.NS",
        "name": "Bharat Petroleum Corp Ltd",
        "ticker": "BPCL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Oil Refining & Marketing",
        "category": "NIFTY 50",
        "aliases": ["bpcl", "bharat petroleum"],
        "is_popular": True,
        "emoji": "⛽"
    },
    {
        "symbol": "EICHERMOT.NS",
        "name": "Eicher Motors Ltd (Royal Enfield)",
        "ticker": "EICHERMOT",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Automobile & Two-Wheelers",
        "category": "NIFTY 50",
        "aliases": ["eicher motors", "eicher", "royal enfield", "eichermot"],
        "is_popular": True,
        "emoji": "🏍️"
    },
    {
        "symbol": "DIVISLAB.NS",
        "name": "Divi's Laboratories Ltd",
        "ticker": "DIVISLAB",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Pharmaceuticals (APIs)",
        "category": "NIFTY 50",
        "aliases": ["divis", "divi's", "divislab", "divis lab"],
        "is_popular": True,
        "emoji": "🧪"
    },
    {
        "symbol": "INDUSINDBK.NS",
        "name": "IndusInd Bank Ltd",
        "ticker": "INDUSINDBK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Banking & Financial Services",
        "category": "NIFTY 50",
        "aliases": ["indusind", "indusind bank", "indusindbk"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "LTIM.NS",
        "name": "LTIMindtree Ltd",
        "ticker": "LTIM",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Information Technology",
        "category": "NIFTY 50",
        "aliases": ["ltimindtree", "ltim", "mindtree", "l&t infotech"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "BAJAJ-AUTO.NS",
        "name": "Bajaj Auto Ltd",
        "ticker": "BAJAJ-AUTO",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Automobile & Two-Wheelers",
        "category": "NIFTY 50",
        "aliases": ["bajaj auto", "bajaj-auto", "bajaj pulsar"],
        "is_popular": True,
        "emoji": "🏍️"
    },
    {
        "symbol": "BRITANNIA.NS",
        "name": "Britannia Industries Ltd",
        "ticker": "BRITANNIA",
        "exchange": "NSE",
        "country": "IN",
        "sector": "FMCG & Bakery",
        "category": "NIFTY 50",
        "aliases": ["britannia", "britannia industries", "good day"],
        "is_popular": True,
        "emoji": "🍪"
    },

    # =========================================================================
    # HIGH-DEMAND MIDCAPS, AUTO ANCILLARY & POPULAR INDIAN GROWTH STOCKS
    # =========================================================================
    {
        "symbol": "MRF.NS",
        "name": "MRF Ltd (Madras Rubber Factory)",
        "ticker": "MRF",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Tyres & Rubber",
        "category": "Auto & EV",
        "aliases": ["mrf", "mrf tyres", "mrf tyre", "madras rubber factory"],
        "is_popular": True,
        "emoji": "🛞"
    },
    {
        "symbol": "APOLLOTYRE.NS",
        "name": "Apollo Tyres Ltd",
        "ticker": "APOLLOTYRE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Tyres & Rubber",
        "category": "Auto & EV",
        "aliases": ["apollo tyres", "apollo tyre", "apollotyre"],
        "is_popular": False,
        "emoji": "🛞"
    },
    {
        "symbol": "CEATLTD.NS",
        "name": "CEAT Ltd",
        "ticker": "CEATLTD",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Tyres & Rubber",
        "category": "Auto & EV",
        "aliases": ["ceat", "ceat tyres", "ceat ltd", "ceatltd"],
        "is_popular": False,
        "emoji": "🛞"
    },
    {
        "symbol": "BALKRISIND.NS",
        "name": "Balkrishna Industries (BKT)",
        "ticker": "BALKRISIND",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Tyres & Rubber",
        "category": "Auto & EV",
        "aliases": ["bkt", "balkrishna industries", "balkrisind"],
        "is_popular": False,
        "emoji": "🚜"
    },
    {
        "symbol": "TVSMOTOR.NS",
        "name": "TVS Motor Company",
        "ticker": "TVSMOTOR",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Automobile & Two-Wheelers",
        "category": "Auto & EV",
        "aliases": ["tvs motor", "tvs", "tvsmotor", "tvs apache"],
        "is_popular": True,
        "emoji": "🏍️"
    },
    {
        "symbol": "ASHOKLEY.NS",
        "name": "Ashok Leyland Ltd",
        "ticker": "ASHOKLEY",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Commercial Vehicles",
        "category": "Auto & EV",
        "aliases": ["ashok leyland", "ashok ley", "ashokley"],
        "is_popular": True,
        "emoji": "🚛"
    },
    {
        "symbol": "BHARATFORG.NS",
        "name": "Bharat Forge Ltd",
        "ticker": "BHARATFORG",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Forging & Auto Components",
        "category": "Auto & EV",
        "aliases": ["bharat forge", "bharatforge", "kalyani group"],
        "is_popular": True,
        "emoji": "⚙️"
    },
    {
        "symbol": "MOTHERSON.NS",
        "name": "Samvardhana Motherson International",
        "ticker": "MOTHERSON",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Auto Components",
        "category": "Auto & EV",
        "aliases": ["motherson", "motherson sumi", "samvardhana motherson"],
        "is_popular": True,
        "emoji": "🚗"
    },
    {
        "symbol": "TATATECH.NS",
        "name": "Tata Technologies Ltd",
        "ticker": "TATATECH",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Engineering & R&D Services",
        "category": "Tech & IT",
        "aliases": ["tata technologies", "tata tech", "tatatech"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "SUZLON.NS",
        "name": "Suzlon Energy Ltd",
        "ticker": "SUZLON",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Renewable Energy & Wind",
        "category": "Energy & Green",
        "aliases": ["suzlon", "suzlon energy", "wind energy"],
        "is_popular": True,
        "emoji": "💨"
    },
    {
        "symbol": "IREDA.NS",
        "name": "Indian Renewable Energy Dev Agency",
        "ticker": "IREDA",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Green Energy Financing",
        "category": "Energy & Green",
        "aliases": ["ireda", "indian renewable energy", "green finance"],
        "is_popular": True,
        "emoji": "🌱"
    },
    {
        "symbol": "TATAPOWER.NS",
        "name": "Tata Power Company",
        "ticker": "TATAPOWER",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Power Generation & EV Charging",
        "category": "Energy & Green",
        "aliases": ["tata power", "tatapower", "டாடா பவர்", "टाटा पावर"],
        "is_popular": True,
        "emoji": "⚡"
    },
    {
        "symbol": "ADANIPOWER.NS",
        "name": "Adani Power Ltd",
        "ticker": "ADANIPOWER",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Thermal Power Generation",
        "category": "Energy & Green",
        "aliases": ["adani power", "adanipower"],
        "is_popular": True,
        "emoji": "⚡"
    },
    {
        "symbol": "ADANIGREEN.NS",
        "name": "Adani Green Energy Ltd",
        "ticker": "ADANIGREEN",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Renewable Solar & Wind",
        "category": "Energy & Green",
        "aliases": ["adani green", "adanigreen"],
        "is_popular": True,
        "emoji": "🌞"
    },
    {
        "symbol": "ATGL.NS",
        "name": "Adani Total Gas Ltd",
        "ticker": "ATGL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "City Gas Distribution",
        "category": "Energy & Green",
        "aliases": ["adani total gas", "atgl", "adani gas"],
        "is_popular": False,
        "emoji": "🔥"
    },
    {
        "symbol": "AWL.NS",
        "name": "Adani Wilmar Ltd (Fortune)",
        "ticker": "AWL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Edible Oils & FMCG",
        "category": "FMCG & Retail",
        "aliases": ["adani wilmar", "awl", "fortune oil"],
        "is_popular": False,
        "emoji": "🌻"
    },

    # =========================================================================
    # NEW-AGE TECH & CONSUMER PLATFORMS
    # =========================================================================
    {
        "symbol": "ZOMATO.NS",
        "name": "Zomato Ltd (Blinkit)",
        "ticker": "ZOMATO",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Food Delivery & Quick Commerce",
        "category": "New-Age & Consumer",
        "aliases": ["zomato", "blinkit", "சோமேட்டோ", "जोमैटो"],
        "is_popular": True,
        "emoji": "🍕"
    },
    {
        "symbol": "SWIGGY.NS",
        "name": "Swiggy Ltd (Instamart)",
        "ticker": "SWIGGY",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Food Delivery & Quick Commerce",
        "category": "New-Age & Consumer",
        "aliases": ["swiggy", "instamart", "ஸ்விக்கி", "स्विगी"],
        "is_popular": True,
        "emoji": "🛵"
    },
    {
        "symbol": "JIOFIN.NS",
        "name": "Jio Financial Services",
        "ticker": "JIOFIN",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Fintech & Financial Services",
        "category": "New-Age & Consumer",
        "aliases": ["jio", "jio financial", "jiofin", "ஜியோ", "जियो"],
        "is_popular": True,
        "emoji": "📱"
    },
    {
        "symbol": "PAYTM.NS",
        "name": "One97 Communications (Paytm)",
        "ticker": "PAYTM",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Digital Payments & Fintech",
        "category": "New-Age & Consumer",
        "aliases": ["paytm", "one97", "பேடிஎம்", "पेटीएम"],
        "is_popular": True,
        "emoji": "💳"
    },
    {
        "symbol": "NYKAA.NS",
        "name": "FSN E-Commerce (Nykaa)",
        "ticker": "NYKAA",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Beauty & Fashion E-Commerce",
        "category": "New-Age & Consumer",
        "aliases": ["nykaa", "fsn e-commerce"],
        "is_popular": True,
        "emoji": "💄"
    },
    {
        "symbol": "POLICYBZR.NS",
        "name": "PB Fintech (Policybazaar)",
        "ticker": "POLICYBZR",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Insurtech & Fintech",
        "category": "New-Age & Consumer",
        "aliases": ["policybazaar", "pb fintech", "policybzr", "paisabazaar"],
        "is_popular": True,
        "emoji": "🛡️"
    },
    {
        "symbol": "DELHIVERY.NS",
        "name": "Delhivery Ltd",
        "ticker": "DELHIVERY",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Logistics & Supply Chain",
        "category": "New-Age & Consumer",
        "aliases": ["delhivery", "delhivery logistics"],
        "is_popular": False,
        "emoji": "📦"
    },
    {
        "symbol": "OLAELEC.NS",
        "name": "Ola Electric Mobility Ltd",
        "ticker": "OLAELEC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Electric Two-Wheelers",
        "category": "New-Age & Consumer",
        "aliases": ["ola electric", "ola", "olaelec", "ola scooter"],
        "is_popular": True,
        "emoji": "⚡"
    },
    {
        "symbol": "NAUKRI.NS",
        "name": "Info Edge India (Naukri.com)",
        "ticker": "NAUKRI",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Internet & Recruitment",
        "category": "New-Age & Consumer",
        "aliases": ["naukri", "info edge", "99acres", "jeevansathi"],
        "is_popular": True,
        "emoji": "💼"
    },
    {
        "symbol": "JUSTDIAL.NS",
        "name": "Just Dial Ltd",
        "ticker": "JUSTDIAL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Local Search & Internet",
        "category": "New-Age & Consumer",
        "aliases": ["just dial", "justdial"],
        "is_popular": False,
        "emoji": "📞"
    },

    # =========================================================================
    # DEFENCE, RAILWAY & PSU GIANTS
    # =========================================================================
    {
        "symbol": "HAL.NS",
        "name": "Hindustan Aeronautics Ltd",
        "ticker": "HAL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Aerospace & Defence",
        "category": "Defence & Rail",
        "aliases": ["hal", "hindustan aeronautics", "tejas aircraft"],
        "is_popular": True,
        "emoji": "✈️"
    },
    {
        "symbol": "BHEL.NS",
        "name": "Bharat Heavy Electricals Ltd",
        "ticker": "BHEL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Heavy Electrical Equipment",
        "category": "Defence & Rail",
        "aliases": ["bhel", "bharat heavy electricals"],
        "is_popular": True,
        "emoji": "⚡"
    },
    {
        "symbol": "RVNL.NS",
        "name": "Rail Vikas Nigam Ltd",
        "ticker": "RVNL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Railway Infrastructure",
        "category": "Defence & Rail",
        "aliases": ["rvnl", "rail vikas", "rail vikas nigam"],
        "is_popular": True,
        "emoji": "🚆"
    },
    {
        "symbol": "IRFC.NS",
        "name": "Indian Railway Finance Corp",
        "ticker": "IRFC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Railway Financing",
        "category": "Defence & Rail",
        "aliases": ["irfc", "indian railway finance"],
        "is_popular": True,
        "emoji": "🚂"
    },
    {
        "symbol": "IRCTC.NS",
        "name": "Indian Railway Catering & Tourism",
        "ticker": "IRCTC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Railway Ticketing & Tourism",
        "category": "Defence & Rail",
        "aliases": ["irctc", "railway ticket", "rail neer"],
        "is_popular": True,
        "emoji": "🎫"
    },
    {
        "symbol": "MAZDOCK.NS",
        "name": "Mazagon Dock Shipbuilders",
        "ticker": "MAZDOCK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Naval Defence & Warships",
        "category": "Defence & Rail",
        "aliases": ["mazagon dock", "mazdock", "mazagon"],
        "is_popular": True,
        "emoji": "⚓"
    },
    {
        "symbol": "COCHINSHIP.NS",
        "name": "Cochin Shipyard Ltd",
        "ticker": "COCHINSHIP",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Shipbuilding & Repairs",
        "category": "Defence & Rail",
        "aliases": ["cochin shipyard", "cochinship", "csl"],
        "is_popular": True,
        "emoji": "🚢"
    },
    {
        "symbol": "BDL.NS",
        "name": "Bharat Dynamics Ltd",
        "ticker": "BDL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Missiles & Defence Systems",
        "category": "Defence & Rail",
        "aliases": ["bdl", "bharat dynamics"],
        "is_popular": True,
        "emoji": "🚀"
    },
    {
        "symbol": "GRSE.NS",
        "name": "Garden Reach Shipbuilders",
        "ticker": "GRSE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Naval Vessels & Shipyard",
        "category": "Defence & Rail",
        "aliases": ["grse", "garden reach"],
        "is_popular": False,
        "emoji": "🛳️"
    },
    {
        "symbol": "TITAGARH.NS",
        "name": "Titagarh Rail Systems Ltd",
        "ticker": "TITAGARH",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Railway Wagons & Metros",
        "category": "Defence & Rail",
        "aliases": ["titagarh", "titagarh rail", "titagarh wagons"],
        "is_popular": True,
        "emoji": "🚆"
    },
    {
        "symbol": "SOLARINDS.NS",
        "name": "Solar Industries India Ltd",
        "ticker": "SOLARINDS",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Industrial Explosives & Defence",
        "category": "Defence & Rail",
        "aliases": ["solar industries", "solarinds"],
        "is_popular": False,
        "emoji": "💥"
    },

    # =========================================================================
    # BANKING & FINANCIAL SERVICES
    # =========================================================================
    {
        "symbol": "BANKBARODA.NS",
        "name": "Bank of Baroda",
        "ticker": "BANKBARODA",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Public Sector Banking",
        "category": "Banking & Finance",
        "aliases": ["bank of baroda", "bob", "bankbaroda"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "PNB.NS",
        "name": "Punjab National Bank",
        "ticker": "PNB",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Public Sector Banking",
        "category": "Banking & Finance",
        "aliases": ["pnb", "punjab national bank"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "CANBK.NS",
        "name": "Canara Bank",
        "ticker": "CANBK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Public Sector Banking",
        "category": "Banking & Finance",
        "aliases": ["canara bank", "canbk"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "IDFCFIRSTB.NS",
        "name": "IDFC First Bank Ltd",
        "ticker": "IDFCFIRSTB",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Private Sector Banking",
        "category": "Banking & Finance",
        "aliases": ["idfc first", "idfc first bank", "idfc", "idfcbank"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "FEDERALBNK.NS",
        "name": "Federal Bank Ltd",
        "ticker": "FEDERALBNK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Private Sector Banking",
        "category": "Banking & Finance",
        "aliases": ["federal bank", "federalbnk"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "YESBANK.NS",
        "name": "Yes Bank Ltd",
        "ticker": "YESBANK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Private Sector Banking",
        "category": "Banking & Finance",
        "aliases": ["yes bank", "yesbank"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "AUBANK.NS",
        "name": "AU Small Finance Bank Ltd",
        "ticker": "AUBANK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Small Finance Bank",
        "category": "Banking & Finance",
        "aliases": ["au bank", "au small finance bank", "aubank"],
        "is_popular": False,
        "emoji": "🏦"
    },
    {
        "symbol": "BANDHANBNK.NS",
        "name": "Bandhan Bank Ltd",
        "ticker": "BANDHANBNK",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Private Sector Banking",
        "category": "Banking & Finance",
        "aliases": ["bandhan bank", "bandhanbnk"],
        "is_popular": False,
        "emoji": "🏦"
    },
    {
        "symbol": "MUTHOOTFIN.NS",
        "name": "Muthoot Finance Ltd",
        "ticker": "MUTHOOTFIN",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Gold Loan NBFC",
        "category": "Banking & Finance",
        "aliases": ["muthoot", "muthoot finance", "gold loan"],
        "is_popular": True,
        "emoji": "🪙"
    },
    {
        "symbol": "REC.NS",
        "name": "REC Ltd (Rural Electrification Corp)",
        "ticker": "REC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Power Sector Financing",
        "category": "Banking & Finance",
        "aliases": ["rec", "rec ltd", "rural electrification"],
        "is_popular": True,
        "emoji": "⚡"
    },
    {
        "symbol": "PFC.NS",
        "name": "Power Finance Corporation",
        "ticker": "PFC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Power Sector Financing",
        "category": "Banking & Finance",
        "aliases": ["pfc", "power finance", "power finance corp"],
        "is_popular": True,
        "emoji": "⚡"
    },
    {
        "symbol": "CHOLAFIN.NS",
        "name": "Cholamandalam Investment & Finance",
        "ticker": "CHOLAFIN",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Vehicle & Home Finance",
        "category": "Banking & Finance",
        "aliases": ["cholamandalam", "chola", "cholafin"],
        "is_popular": True,
        "emoji": "🚛"
    },
    {
        "symbol": "CDSL.NS",
        "name": "Central Depository Services Ltd",
        "ticker": "CDSL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Market Infrastructure Depository",
        "category": "Banking & Finance",
        "aliases": ["cdsl", "central depository", "demat"],
        "is_popular": True,
        "emoji": "📜"
    },
    {
        "symbol": "BSE.NS",
        "name": "BSE Ltd (Bombay Stock Exchange)",
        "ticker": "BSE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Stock Exchange Operator",
        "category": "Banking & Finance",
        "aliases": ["bse", "bse limited", "bombay stock exchange"],
        "is_popular": True,
        "emoji": "🏛️"
    },
    {
        "symbol": "ANGELONE.NS",
        "name": "Angel One Ltd",
        "ticker": "ANGELONE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Retail Brokerage & Fintech",
        "category": "Banking & Finance",
        "aliases": ["angel one", "angelone", "angel broking"],
        "is_popular": True,
        "emoji": "📱"
    },
    {
        "symbol": "MCX.NS",
        "name": "Multi Commodity Exchange of India",
        "ticker": "MCX",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Commodity Exchange Operator",
        "category": "Banking & Finance",
        "aliases": ["mcx", "multi commodity exchange"],
        "is_popular": True,
        "emoji": "🪙"
    },
    {
        "symbol": "LICI.NS",
        "name": "Life Insurance Corporation of India",
        "ticker": "LICI",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Life Insurance",
        "category": "Banking & Finance",
        "aliases": ["lic", "lici", "life insurance corporation"],
        "is_popular": True,
        "emoji": "🛡️"
    },
    {
        "symbol": "SBILIFE.NS",
        "name": "SBI Life Insurance Co Ltd",
        "ticker": "SBILIFE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Life Insurance",
        "category": "Banking & Finance",
        "aliases": ["sbi life", "sbilife"],
        "is_popular": False,
        "emoji": "🛡️"
    },
    {
        "symbol": "HDFCLIFE.NS",
        "name": "HDFC Life Insurance Co Ltd",
        "ticker": "HDFCLIFE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Life Insurance",
        "category": "Banking & Finance",
        "aliases": ["hdfc life", "hdfclife"],
        "is_popular": False,
        "emoji": "🛡️"
    },

    # =========================================================================
    # IT, TECH & ELECTRONICS
    # =========================================================================
    {
        "symbol": "PERSISTENT.NS",
        "name": "Persistent Systems Ltd",
        "ticker": "PERSISTENT",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Digital Engineering & Cloud",
        "category": "Tech & IT",
        "aliases": ["persistent", "persistent systems"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "COFORGE.NS",
        "name": "Coforge Ltd (NIIT Tech)",
        "ticker": "COFORGE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "IT Solutions & Services",
        "category": "Tech & IT",
        "aliases": ["coforge", "niit technologies"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "MPHASIS.NS",
        "name": "Mphasis Ltd",
        "ticker": "MPHASIS",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Cloud & Cognitive Services",
        "category": "Tech & IT",
        "aliases": ["mphasis", "mphasis ltd"],
        "is_popular": False,
        "emoji": "💻"
    },
    {
        "symbol": "TATAELXSI.NS",
        "name": "Tata Elxsi Ltd",
        "ticker": "TATAELXSI",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Design & Engineering Services",
        "category": "Tech & IT",
        "aliases": ["tata elxsi", "tataelxsi"],
        "is_popular": True,
        "emoji": "🎨"
    },
    {
        "symbol": "KPITTECH.NS",
        "name": "KPIT Technologies Ltd",
        "ticker": "KPITTECH",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Automotive Software & Mobility",
        "category": "Tech & IT",
        "aliases": ["kpit", "kpit tech", "kpittech"],
        "is_popular": True,
        "emoji": "🚗"
    },
    {
        "symbol": "CYIENT.NS",
        "name": "Cyient Ltd",
        "ticker": "CYIENT",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Engineering & Technology Solutions",
        "category": "Tech & IT",
        "aliases": ["cyient", "cyient ltd"],
        "is_popular": False,
        "emoji": "📐"
    },
    {
        "symbol": "DIXON.NS",
        "name": "Dixon Technologies Ltd",
        "ticker": "DIXON",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Electronic Manufacturing Services",
        "category": "Tech & IT",
        "aliases": ["dixon", "dixon technologies", "ems"],
        "is_popular": True,
        "emoji": "📱"
    },
    {
        "symbol": "POLYCAB.NS",
        "name": "Polycab India Ltd",
        "ticker": "POLYCAB",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Wires, Cables & FMEG",
        "category": "Consumer & Industrials",
        "aliases": ["polycab", "polycab wires"],
        "is_popular": True,
        "emoji": "🔌"
    },
    {
        "symbol": "HAVELLS.NS",
        "name": "Havells India Ltd",
        "ticker": "HAVELLS",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Electrical Consumer Goods",
        "category": "Consumer & Industrials",
        "aliases": ["havells", "lloyd", "crabtree"],
        "is_popular": True,
        "emoji": "💡"
    },
    {
        "symbol": "VOLTAS.NS",
        "name": "Voltas Ltd (A Tata Enterprise)",
        "ticker": "VOLTAS",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Air Conditioners & Cooling",
        "category": "Consumer & Industrials",
        "aliases": ["voltas", "voltas ac", "voltas beko"],
        "is_popular": True,
        "emoji": "❄️"
    },
    {
        "symbol": "BLUESTARCO.NS",
        "name": "Blue Star Ltd",
        "ticker": "BLUESTARCO",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Commercial Refrigeration & AC",
        "category": "Consumer & Industrials",
        "aliases": ["blue star", "bluestarco"],
        "is_popular": False,
        "emoji": "❄️"
    },

    # =========================================================================
    # RETAIL, FMCG & CONSUMPTION
    # =========================================================================
    {
        "symbol": "DMART.NS",
        "name": "Avenue Supermarts (DMart)",
        "ticker": "DMART",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Hypermarket & Supermarkets",
        "category": "FMCG & Retail",
        "aliases": ["dmart", "d-mart", "avenue supermarts", "radhakishan damani"],
        "is_popular": True,
        "emoji": "🛒"
    },
    {
        "symbol": "VBL.NS",
        "name": "Varun Beverages Ltd (Pepsi Bottler)",
        "ticker": "VBL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Beverages & Bottling",
        "category": "FMCG & Retail",
        "aliases": ["varun beverages", "vbl", "pepsi bottler"],
        "is_popular": True,
        "emoji": "🥤"
    },
    {
        "symbol": "DABUR.NS",
        "name": "Dabur India Ltd",
        "ticker": "DABUR",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Ayurveda & Consumer Care",
        "category": "FMCG & Retail",
        "aliases": ["dabur", "dabur chyawanprash", "real juice"],
        "is_popular": True,
        "emoji": "🍯"
    },
    {
        "symbol": "MARICO.NS",
        "name": "Marico Ltd",
        "ticker": "MARICO",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Consumer Goods & Edible Oils",
        "category": "FMCG & Retail",
        "aliases": ["marico", "parachute", "saffola"],
        "is_popular": True,
        "emoji": "🥥"
    },
    {
        "symbol": "GODREJCP.NS",
        "name": "Godrej Consumer Products Ltd",
        "ticker": "GODREJCP",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Household & Personal Care",
        "category": "FMCG & Retail",
        "aliases": ["godrej consumer", "godrejcp", "goodknight", "hit"],
        "is_popular": True,
        "emoji": "🧼"
    },
    {
        "symbol": "COLPAL.NS",
        "name": "Colgate-Palmolive (India) Ltd",
        "ticker": "COLPAL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Oral Care & FMCG",
        "category": "FMCG & Retail",
        "aliases": ["colgate", "colpal", "palmolive"],
        "is_popular": True,
        "emoji": "🪥"
    },
    {
        "symbol": "PIDILITIND.NS",
        "name": "Pidilite Industries (Fevicol)",
        "ticker": "PIDILITIND",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Adhesives & Sealants",
        "category": "Consumer & Industrials",
        "aliases": ["pidilite", "fevicol", "pidilitind", "m-seal", "dr fixit"],
        "is_popular": True,
        "emoji": "🧪"
    },
    {
        "symbol": "BERGEPAINT.NS",
        "name": "Berger Paints India Ltd",
        "ticker": "BERGEPAINT",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Paints & Coatings",
        "category": "Consumer & Industrials",
        "aliases": ["berger paints", "berger", "bergepaint"],
        "is_popular": True,
        "emoji": "🎨"
    },
    {
        "symbol": "KALYANKJIL.NS",
        "name": "Kalyan Jewellers India Ltd",
        "ticker": "KALYANKJIL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Gems & Jewellery",
        "category": "FMCG & Retail",
        "aliases": ["kalyan jewellers", "kalyan", "candere"],
        "is_popular": True,
        "emoji": "💍"
    },
    {
        "symbol": "PAGEIND.NS",
        "name": "Page Industries Ltd (Jockey)",
        "ticker": "PAGEIND",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Apparel & Innerwear",
        "category": "FMCG & Retail",
        "aliases": ["page industries", "jockey", "pageind", "speedo"],
        "is_popular": True,
        "emoji": "🩲"
    },
    {
        "symbol": "INDIGO.NS",
        "name": "InterGlobe Aviation (IndiGo)",
        "ticker": "INDIGO",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Airlines & Aviation",
        "category": "FMCG & Retail",
        "aliases": ["indigo", "interglobe aviation", "indigo airlines"],
        "is_popular": True,
        "emoji": "✈️"
    },
    {
        "symbol": "DLF.NS",
        "name": "DLF Ltd",
        "ticker": "DLF",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Real Estate Development",
        "category": "Real Estate",
        "aliases": ["dlf", "dlf limited"],
        "is_popular": True,
        "emoji": "🏢"
    },
    {
        "symbol": "GODREJPROP.NS",
        "name": "Godrej Properties Ltd",
        "ticker": "GODREJPROP",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Residential Real Estate",
        "category": "Real Estate",
        "aliases": ["godrej properties", "godrejprop"],
        "is_popular": True,
        "emoji": "🏢"
    },
    {
        "symbol": "LODHA.NS",
        "name": "Macrotech Developers (Lodha)",
        "ticker": "LODHA",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Luxury & Urban Real Estate",
        "category": "Real Estate",
        "aliases": ["lodha", "macrotech developers", "macrotech"],
        "is_popular": True,
        "emoji": "🏙️"
    },

    # =========================================================================
    # HEALTHCARE & PHARMA
    # =========================================================================
    {
        "symbol": "LUPIN.NS",
        "name": "Lupin Ltd",
        "ticker": "LUPIN",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Pharmaceuticals",
        "category": "Pharma & Health",
        "aliases": ["lupin", "lupin ltd"],
        "is_popular": True,
        "emoji": "💊"
    },
    {
        "symbol": "TORNTPHARM.NS",
        "name": "Torrent Pharmaceuticals",
        "ticker": "TORNTPHARM",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Pharmaceuticals",
        "category": "Pharma & Health",
        "aliases": ["torrent pharma", "torntpharm"],
        "is_popular": True,
        "emoji": "💊"
    },
    {
        "symbol": "AUROPHARMA.NS",
        "name": "Aurobindo Pharma Ltd",
        "ticker": "AUROPHARMA",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Pharmaceuticals",
        "category": "Pharma & Health",
        "aliases": ["aurobindo", "aurobindo pharma", "auropharma"],
        "is_popular": True,
        "emoji": "💊"
    },
    {
        "symbol": "BIOCON.NS",
        "name": "Biocon Ltd",
        "ticker": "BIOCON",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Biopharmaceuticals & Biosimilars",
        "category": "Pharma & Health",
        "aliases": ["biocon", "biocon biologics", "kiran mazumdar"],
        "is_popular": True,
        "emoji": "🧬"
    },
    {
        "symbol": "ZYDUSLIFE.NS",
        "name": "Zydus Lifesciences Ltd",
        "ticker": "ZYDUSLIFE",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Pharmaceuticals",
        "category": "Pharma & Health",
        "aliases": ["zydus", "zydus life", "cadila healthcare", "zyduslife"],
        "is_popular": True,
        "emoji": "💊"
    },
    {
        "symbol": "MANKIND.NS",
        "name": "Mankind Pharma Ltd",
        "ticker": "MANKIND",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Domestic Formulations & OTC",
        "category": "Pharma & Health",
        "aliases": ["mankind", "mankind pharma", "manforce", "prega news"],
        "is_popular": True,
        "emoji": "💊"
    },
    {
        "symbol": "MAXHEALTH.NS",
        "name": "Max Healthcare Institute",
        "ticker": "MAXHEALTH",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Hospitals & Healthcare",
        "category": "Pharma & Health",
        "aliases": ["max healthcare", "max hospital", "maxhealth"],
        "is_popular": True,
        "emoji": "🏥"
    },

    # =========================================================================
    # METALS, MINING, COMMODITIES & CEMENT
    # =========================================================================
    {
        "symbol": "VEDL.NS",
        "name": "Vedanta Ltd",
        "ticker": "VEDL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Metals, Mining & Natural Resources",
        "category": "Metals & Mining",
        "aliases": ["vedanta", "vedl", "anil agarwal"],
        "is_popular": True,
        "emoji": "⛏️"
    },
    {
        "symbol": "JINDALSTEL.NS",
        "name": "Jindal Steel & Power Ltd",
        "ticker": "JINDALSTEL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Steel & Power",
        "category": "Metals & Mining",
        "aliases": ["jindal steel", "jindalstel", "jspl"],
        "is_popular": True,
        "emoji": "🏗️"
    },
    {
        "symbol": "SAIL.NS",
        "name": "Steel Authority of India Ltd",
        "ticker": "SAIL",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Steel Manufacturing",
        "category": "Metals & Mining",
        "aliases": ["sail", "steel authority of india"],
        "is_popular": True,
        "emoji": "🏗️"
    },
    {
        "symbol": "NMDC.NS",
        "name": "NMDC Ltd (National Mineral Dev)",
        "ticker": "NMDC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Iron Ore Mining",
        "category": "Metals & Mining",
        "aliases": ["nmdc", "iron ore"],
        "is_popular": True,
        "emoji": "⛏️"
    },
    {
        "symbol": "NATIONALUM.NS",
        "name": "National Aluminium Co Ltd (NALCO)",
        "ticker": "NATIONALUM",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Aluminium Smelting & Alumina",
        "category": "Metals & Mining",
        "aliases": ["national aluminium", "nalco", "nationalum"],
        "is_popular": True,
        "emoji": "🥈"
    },
    {
        "symbol": "AMBUJACEM.NS",
        "name": "Ambuja Cements Ltd",
        "ticker": "AMBUJACEM",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Cement Manufacturing",
        "category": "Cement & Building Materials",
        "aliases": ["ambuja", "ambuja cement", "ambujacem"],
        "is_popular": True,
        "emoji": "🧱"
    },
    {
        "symbol": "ACC.NS",
        "name": "ACC Ltd",
        "ticker": "ACC",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Cement Manufacturing",
        "category": "Cement & Building Materials",
        "aliases": ["acc", "acc cement", "acc ltd"],
        "is_popular": True,
        "emoji": "🧱"
    },

    # =========================================================================
    # US & GLOBAL TECH / MEGA-CAPS
    # =========================================================================
    {
        "symbol": "AAPL",
        "name": "Apple Inc",
        "ticker": "AAPL",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Consumer Electronics & Services",
        "category": "Global Mega-Caps",
        "aliases": ["apple", "aapl", "iphone", "ஆப்பிள்", "एप्पल"],
        "is_popular": True,
        "emoji": "🍏"
    },
    {
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "ticker": "MSFT",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Enterprise Software & Cloud",
        "category": "Global Mega-Caps",
        "aliases": ["microsoft", "msft", "windows", "azure", "மைக்ரோசாப்ட்", "माइक्रोसॉफ्ट"],
        "is_popular": True,
        "emoji": "🪟"
    },
    {
        "symbol": "GOOGL",
        "name": "Alphabet Inc (Google)",
        "ticker": "GOOGL",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Internet Services & Search",
        "category": "Global Mega-Caps",
        "aliases": ["google", "alphabet", "googl", "goog", "கூகிள்", "गूगल"],
        "is_popular": True,
        "emoji": "🔍"
    },
    {
        "symbol": "AMZN",
        "name": "Amazon.com Inc",
        "ticker": "AMZN",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "E-Commerce & AWS Cloud",
        "category": "Global Mega-Caps",
        "aliases": ["amazon", "amzn", "aws", "அமேசான்", "अमेज़न"],
        "is_popular": True,
        "emoji": "📦"
    },
    {
        "symbol": "NVDA",
        "name": "Nvidia Corporation",
        "ticker": "NVDA",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Semiconductors & AI GPUs",
        "category": "Global Mega-Caps",
        "aliases": ["nvidia", "nvda", "geforce", "என்விடியா", "एनवीडिया"],
        "is_popular": True,
        "emoji": "🤖"
    },
    {
        "symbol": "META",
        "name": "Meta Platforms Inc (Facebook)",
        "ticker": "META",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Social Media & VR",
        "category": "Global Mega-Caps",
        "aliases": ["meta", "facebook", "instagram", "whatsapp"],
        "is_popular": True,
        "emoji": "💬"
    },
    {
        "symbol": "TSLA",
        "name": "Tesla Inc",
        "ticker": "TSLA",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Electric Vehicles & Clean Energy",
        "category": "Global Mega-Caps",
        "aliases": ["tesla", "tsla", "elon musk", "டெஸ்லா", "टेस्ला"],
        "is_popular": True,
        "emoji": "⚡"
    },
    {
        "symbol": "NFLX",
        "name": "Netflix Inc",
        "ticker": "NFLX",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Streaming Entertainment",
        "category": "Global Mega-Caps",
        "aliases": ["netflix", "nflx"],
        "is_popular": True,
        "emoji": "🎬"
    },
    {
        "symbol": "AMD",
        "name": "Advanced Micro Devices",
        "ticker": "AMD",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Semiconductors & Processors",
        "category": "Global Mega-Caps",
        "aliases": ["amd", "ryzen", "radeon"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "INTC",
        "name": "Intel Corporation",
        "ticker": "INTC",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Semiconductors",
        "category": "Global Mega-Caps",
        "aliases": ["intel", "intc"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "QCOM",
        "name": "Qualcomm Inc",
        "ticker": "QCOM",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Wireless Chips & Snapdragons",
        "category": "Global Mega-Caps",
        "aliases": ["qualcomm", "qcom", "snapdragon"],
        "is_popular": False,
        "emoji": "📡"
    },
    {
        "symbol": "AVGO",
        "name": "Broadcom Inc",
        "ticker": "AVGO",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Semiconductors & Infrastructure Software",
        "category": "Global Mega-Caps",
        "aliases": ["broadcom", "avgo"],
        "is_popular": True,
        "emoji": "🔌"
    },
    {
        "symbol": "TSM",
        "name": "Taiwan Semiconductor (TSMC)",
        "ticker": "TSM",
        "exchange": "NYSE",
        "country": "US",
        "sector": "Foundry Semiconductor Manufacturing",
        "category": "Global Mega-Caps",
        "aliases": ["tsmc", "tsm", "taiwan semi"],
        "is_popular": True,
        "emoji": "🏭"
    },
    {
        "symbol": "PLTR",
        "name": "Palantir Technologies",
        "ticker": "PLTR",
        "exchange": "NYSE",
        "country": "US",
        "sector": "Big Data Analytics & AI Defense",
        "category": "Global Mega-Caps",
        "aliases": ["palantir", "pltr", "alex karp"],
        "is_popular": True,
        "emoji": "🔮"
    },
    {
        "symbol": "COIN",
        "name": "Coinbase Global",
        "ticker": "COIN",
        "exchange": "NASDAQ",
        "country": "US",
        "sector": "Cryptocurrency Exchange",
        "category": "Global Mega-Caps",
        "aliases": ["coinbase", "coin"],
        "is_popular": True,
        "emoji": "🪙"
    },

    # =========================================================================
    # MAJOR INDICES, COMMODITIES & CRYPTO
    # =========================================================================
    {
        "symbol": "^NSEI",
        "name": "NIFTY 50 Index",
        "ticker": "NIFTY",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Benchmark Indian Index",
        "category": "Indices & Commodities",
        "aliases": ["nifty", "nifty 50", "nifty50", "nse nifty", "நிப்டி", "निफ्टी"],
        "is_popular": True,
        "emoji": "🇮🇳"
    },
    {
        "symbol": "^BSESN",
        "name": "BSE SENSEX",
        "ticker": "SENSEX",
        "exchange": "BSE",
        "country": "IN",
        "sector": "Benchmark Indian Index",
        "category": "Indices & Commodities",
        "aliases": ["sensex", "bse sensex", "சென்செக்ஸ்", "सेंसेक्स"],
        "is_popular": True,
        "emoji": "🇮🇳"
    },
    {
        "symbol": "^NSEBANK",
        "name": "Bank Nifty Index",
        "ticker": "BANKNIFTY",
        "exchange": "NSE",
        "country": "IN",
        "sector": "Banking Sector Index",
        "category": "Indices & Commodities",
        "aliases": ["nifty bank", "bank nifty", "banknifty"],
        "is_popular": True,
        "emoji": "🏦"
    },
    {
        "symbol": "^CNXIT",
        "name": "NIFTY IT Index",
        "ticker": "NIFTYIT",
        "exchange": "NSE",
        "country": "IN",
        "sector": "IT Sector Index",
        "category": "Indices & Commodities",
        "aliases": ["nifty it", "cnx it", "cnxit"],
        "is_popular": True,
        "emoji": "💻"
    },
    {
        "symbol": "^GSPC",
        "name": "S&P 500 Index",
        "ticker": "SP500",
        "exchange": "US",
        "country": "US",
        "sector": "Benchmark US Index",
        "category": "Indices & Commodities",
        "aliases": ["s&p 500", "sp500", "s&p"],
        "is_popular": True,
        "emoji": "🇺🇸"
    },
    {
        "symbol": "^IXIC",
        "name": "NASDAQ Composite",
        "ticker": "NASDAQ",
        "exchange": "US",
        "country": "US",
        "sector": "US Tech Index",
        "category": "Indices & Commodities",
        "aliases": ["nasdaq", "nasdaq composite"],
        "is_popular": True,
        "emoji": "🇺🇸"
    },
    {
        "symbol": "GC=F",
        "name": "Gold Futures",
        "ticker": "GOLD",
        "exchange": "COMEX",
        "country": "Global",
        "sector": "Precious Metals",
        "category": "Indices & Commodities",
        "aliases": ["gold", "gold futures", "தங்கம்", "सोना"],
        "is_popular": True,
        "emoji": "🪙"
    },
    {
        "symbol": "SI=F",
        "name": "Silver Futures",
        "ticker": "SILVER",
        "exchange": "COMEX",
        "country": "Global",
        "sector": "Precious Metals",
        "category": "Indices & Commodities",
        "aliases": ["silver", "silver futures", "வெள்ளி", "चांदी"],
        "is_popular": True,
        "emoji": "🥈"
    },
    {
        "symbol": "CL=F",
        "name": "Crude Oil Futures",
        "ticker": "CRUDE",
        "exchange": "NYMEX",
        "country": "Global",
        "sector": "Energy Commodities",
        "category": "Indices & Commodities",
        "aliases": ["crude oil", "crude", "oil futures"],
        "is_popular": True,
        "emoji": "🛢️"
    },
    {
        "symbol": "BTC-USD",
        "name": "Bitcoin (USD)",
        "ticker": "BTC",
        "exchange": "Crypto",
        "country": "Global",
        "sector": "Cryptocurrency",
        "category": "Indices & Commodities",
        "aliases": ["bitcoin", "btc", "btc-usd"],
        "is_popular": True,
        "emoji": "₿"
    }
]

# Load extended master list if available
import os
import json
_master_path = os.path.join(os.path.dirname(__file__), "companies_master.json")
if os.path.exists(_master_path):
    try:
        with open(_master_path, "r", encoding="utf-8") as _f:
            _ext_companies = json.load(_f)
            _existing_symbols = {c["symbol"]: c for c in COMPANIES}
            for _c in _ext_companies:
                sym = _c["symbol"]
                if sym not in _existing_symbols:
                    COMPANIES.append(_c)
                    _existing_symbols[sym] = _c
                else:
                    existing = _existing_symbols[sym]
                    existing_aliases = set(existing.get("aliases", []))
                    for a in _c.get("aliases", []):
                        if a.lower() not in existing_aliases:
                            existing.setdefault("aliases", []).append(a)
    except Exception as _e:
        print(f"Notice: Could not load companies_master.json: {_e}")

# Fast lookup dicts
SYMBOL_MAP: Dict[str, Dict[str, Any]] = {c["symbol"]: c for c in COMPANIES}

def get_all_companies() -> List[Dict[str, Any]]:
    """Return all companies in the catalog."""
    return COMPANIES

def get_company_by_symbol(symbol: str) -> Optional[Dict[str, Any]]:
    """Lookup company metadata by ticker symbol."""
    return SYMBOL_MAP.get(symbol)

def search_companies(query: str, limit: int = 15) -> List[Dict[str, Any]]:
    """
    Search companies by name, ticker, or aliases with prefix and fuzzy match.
    """
    q = query.strip().lower()
    if not q:
        # Return popular companies by default
        return [c for c in COMPANIES if c.get("is_popular", False)][:limit]

    exact_matches = []
    starts_matches = []
    contains_matches = []

    for c in COMPANIES:
        name_lower = c["name"].lower()
        ticker_lower = c["ticker"].lower()
        symbol_lower = c["symbol"].lower()
        alias_list = [a.lower() for a in c.get("aliases", [])]

        if q == ticker_lower or q == symbol_lower or q in alias_list:
            exact_matches.append(c)
        elif ticker_lower.startswith(q) or name_lower.startswith(q) or any(a.startswith(q) for a in alias_list):
            starts_matches.append(c)
        elif q in name_lower or q in ticker_lower or any(q in a for a in alias_list) or q in c["sector"].lower():
            contains_matches.append(c)

    results = []
    seen = set()
    for c in exact_matches + starts_matches + contains_matches:
        if c["symbol"] not in seen:
            seen.add(c["symbol"])
            results.append(c)
        if len(results) >= limit:
            break

    return results

def get_categories() -> Dict[str, List[Dict[str, Any]]]:
    """Return companies grouped by category."""
    cats: Dict[str, List[Dict[str, Any]]] = {}
    for c in COMPANIES:
        cat = c.get("category", "Other")
        if cat not in cats:
            cats[cat] = []
        cats[cat].append(c)
    return cats

def build_catalog_alias_map() -> Dict[str, str]:
    """Build a mapping of every lowercased name, ticker, and alias to its symbol."""
    alias_map: Dict[str, str] = {}
    for c in COMPANIES:
        sym = c["symbol"]
        alias_map[c["ticker"].lower()] = sym
        alias_map[c["name"].lower()] = sym
        for a in c.get("aliases", []):
            alias_map[a.lower()] = sym
    return alias_map
