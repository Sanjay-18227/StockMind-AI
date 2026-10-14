"""
StockMind AI — Comprehensive Catalog Builder
Combines all existing companies with comprehensive coverage of:
- All NIFTY 50 & NIFTY Next 50 companies
- High-growth midcaps, smallcaps, PSUs, defence, railways, and renewable green energy
- Consumer tech, fintech, IPOs (FirstCry, Mamaearth, Premier Energies, Waaree, Zaggle, etc.)
- US Tech mega-caps, cybersecurity, global indices, commodities, and crypto
"""

import json
import os

# 1. Load existing master companies if available
existing_master_path = "c:/Users/acer/Desktop/stackmarket/data/companies_master.json"
existing_list = []
if os.path.exists(existing_master_path):
    with open(existing_master_path, "r", encoding="utf-8") as f:
        existing_list = json.load(f)

# Also load existing aliases from data/companies.py
import sys
sys.path.insert(0, "c:/Users/acer/Desktop/stackmarket")
try:
    import data.companies as dc
    for c in dc.COMPANIES:
        # Merge any unique aliases into existing_list
        for m in existing_list:
            if m["symbol"] == c["symbol"]:
                existing_aliases = set(a.lower() for a in m.get("aliases", []))
                for a in c.get("aliases", []):
                    if a.lower() not in existing_aliases:
                        m.setdefault("aliases", []).append(a)
                        existing_aliases.add(a.lower())
except Exception as e:
    print(f"Warning importing data.companies: {e}")

# Build map by symbol
master_map = {c["symbol"]: c for c in existing_list}

NEW_COMPANIES = [
    # --- RENEWABLE ENERGY, POWER & UTILITIES ---
    ("PREMIERENE.NS", "Premier Energies Ltd", "PREMIERENE", "NSE", "IN", "Solar PV Cells & Modules", "Energy & Green", ["premier energies", "premier energy", "premierene"], True, "☀️"),
    ("WAAREEENER.NS", "Waaree Energies Ltd", "WAAREEENER", "NSE", "IN", "Solar PV Modules & Green Hydrogen", "Energy & Green", ["waaree", "waaree energies", "waareeener"], True, "☀️"),
    ("INOXWIND.NS", "Inox Wind Ltd", "INOXWIND", "NSE", "IN", "Wind Energy Equipment & EPC", "Energy & Green", ["inox wind", "inoxwind"], True, "💨"),
    ("KPIGREEN.NS", "KPI Green Energy Ltd", "KPIGREEN", "NSE", "IN", "Solar & Hybrid Power Producer", "Energy & Green", ["kpi green", "kpi green energy", "kpigreen"], False, "🌱"),
    ("SWSOLAR.NS", "Sterling and Wilson Renewable Energy", "SWSOLAR", "NSE", "IN", "Solar EPC Solutions", "Energy & Green", ["sterling and wilson", "swsolar"], False, "☀️"),
    ("BORORENEW.NS", "Borosil Renewables Ltd", "BORORENEW", "NSE", "IN", "Solar Glass Manufacturing", "Energy & Green", ["borosil renewables", "bororenew"], False, "🪟"),
    ("SERVOTECH.NS", "Servotech Power Systems", "SERVOTECH", "NSE", "IN", "EV Chargers & Solar Inverters", "Energy & Green", ["servotech", "servotech power"], False, "🔌"),
    ("OLECTRA.NS", "Olectra Greentech Ltd", "OLECTRA", "NSE", "IN", "Electric Buses & EV Powertrains", "Auto & EV", ["olectra", "olectra greentech"], True, "🚌"),
    ("JBMMAUTO.NS", "JBM Auto Ltd", "JBMMAUTO", "NSE", "IN", "Electric Buses & Auto Systems", "Auto & EV", ["jbm auto", "jbm"], True, "🚌"),
    ("HBLPOWER.NS", "HBL Power Systems Ltd", "HBLPOWER", "NSE", "IN", "Kavach Train Collision & Batteries", "Industrial Engineering", ["hbl power", "kavach", "hblpower"], True, "🚆"),

    # --- RAILWAYS & DEFENCE INFRASTRUCTURE ---
    ("IRCON.NS", "Ircon International Ltd", "IRCON", "NSE", "IN", "Railway Construction & Infrastructure", "Defence & Rail", ["ircon", "ircon international"], True, "🚆"),
    ("HUDCO.NS", "Housing & Urban Development Corp", "HUDCO", "NSE", "IN", "Housing & Urban Infrastructure Finance", "Banking & Finance", ["hudco"], True, "🏙️"),
    ("DYNAMATECH.NS", "Dynamatic Technologies Ltd", "DYNAMATECH", "NSE", "IN", "Aerospace & Hydraulic Systems", "Defence & Rail", ["dynamatic", "dynamatic tech"], False, "✈️"),
    ("IDEAFORGE.NS", "Ideaforge Technology Ltd", "IDEAFORGE", "NSE", "IN", "UAV Drones & Defence Surveillance", "Defence & Rail", ["ideaforge", "drones"], True, "🛸"),
    ("APOLLOMICR.NS", "Apollo Micro Systems Ltd", "APOLLOMICR", "NSE", "IN", "Electronic & Electromechanical Defence", "Defence & Rail", ["apollo micro", "apollo micro systems"], False, "📡"),
    ("DCXINDIA.NS", "DCX Systems Ltd", "DCXINDIA", "NSE", "IN", "System Integration & Cable Harnesses", "Defence & Rail", ["dcx systems", "dcx india"], False, "🔌"),

    # --- NEW-AGE CONSUMER TECH & SAAS ---
    ("BRAINBEES.NS", "Brainbees Solutions Ltd (FirstCry)", "BRAINBEES", "NSE", "IN", "Baby & Kids Omnichannel Retail", "New-Age & Consumer", ["firstcry", "brainbees", "first cry"], True, "👶"),
    ("HONASA.NS", "Honasa Consumer Ltd (Mamaearth)", "HONASA", "NSE", "IN", "D2C Personal & Beauty Care", "New-Age & Consumer", ["mamaearth", "honasa", "the derma co"], True, "🌿"),
    ("ZAGGLE.NS", "Zaggle Prepaid Ocean Services", "ZAGGLE", "NSE", "IN", "Fintech SaaS & Spend Management", "New-Age & Consumer", ["zaggle"], True, "💳"),
    ("RATEGAIN.NS", "RateGain Travel Technologies", "RATEGAIN", "NSE", "IN", "Hospitality & Travel SaaS AI", "New-Age & Consumer", ["rategain"], False, "🏨"),
    ("AFFLE.NS", "Affle (India) Ltd", "AFFLE", "NSE", "IN", "Consumer Intelligence & Mobile Adtech", "New-Age & Consumer", ["affle", "affle india"], True, "📱"),
    ("LATENTVIEW.NS", "Latent View Analytics Ltd", "LATENTVIEW", "NSE", "IN", "Data & AI Analytics Consulting", "Tech & IT", ["latent view", "latentview"], False, "📊"),
    ("NETWEB.NS", "Netweb Technologies India", "NETWEB", "NSE", "IN", "Supercomputing & AI Server Systems", "Tech & IT", ["netweb", "netweb technologies", "ai server"], True, "🖥️"),
    ("YATRA.NS", "Yatra Online Ltd", "YATRA", "NSE", "IN", "Online Travel & Corporate Bookings", "New-Age & Consumer", ["yatra", "yatra online"], False, "✈️"),
    ("FINOPB.NS", "Fino Payments Bank Ltd", "FINOPB", "NSE", "IN", "Digital & Rural Banking Services", "Banking & Finance", ["fino", "fino payments bank"], False, "📱"),

    # --- BANKING, SFBs, HOUSING FINANCE & BROKERAGES ---
    ("IOB.NS", "Indian Overseas Bank", "IOB", "NSE", "IN", "Public Sector Banking", "Banking & Finance", ["iob", "indian overseas bank"], True, "🏦"),
    ("PSB.NS", "Punjab & Sind Bank", "PSB", "NSE", "IN", "Public Sector Banking", "Banking & Finance", ["punjab and sind bank", "psb"], False, "🏦"),
    ("J&KBANK.NS", "The Jammu & Kashmir Bank Ltd", "J&KBANK", "NSE", "IN", "Private Sector Banking", "Banking & Finance", ["j&k bank", "jk bank"], False, "🏦"),
    ("KTKBANK.NS", "The Karnataka Bank Ltd", "KTKBANK", "NSE", "IN", "Private Sector Banking", "Banking & Finance", ["karnataka bank", "ktk bank"], False, "🏦"),
    ("SOUTHBANK.NS", "The South Indian Bank Ltd", "SOUTHBANK", "NSE", "IN", "Private Sector Banking", "Banking & Finance", ["south indian bank", "sib"], False, "🏦"),
    ("CSBBANK.NS", "CSB Bank Ltd", "CSBBANK", "NSE", "IN", "Private Sector Banking", "Banking & Finance", ["csb bank", "catholic syrian bank"], False, "🏦"),
    ("DCBBANK.NS", "DCB Bank Ltd", "DCBBANK", "NSE", "IN", "Private Sector Banking", "Banking & Finance", ["dcb bank", "dcb"], False, "🏦"),
    ("JANA.NS", "Jana Small Finance Bank", "JANA", "NSE", "IN", "Small Finance Bank", "Banking & Finance", ["jana bank", "jana small finance"], False, "🏦"),
    ("UTKARSHBNK.NS", "Utkarsh Small Finance Bank", "UTKARSHBNK", "NSE", "IN", "Small Finance Bank", "Banking & Finance", ["utkarsh bank"], False, "🏦"),
    ("ESAFSFB.NS", "ESAF Small Finance Bank", "ESAFSFB", "NSE", "IN", "Small Finance Bank", "Banking & Finance", ["esaf bank"], False, "🏦"),
    ("SURYODAY.NS", "Suryoday Small Finance Bank", "SURYODAY", "NSE", "IN", "Small Finance Bank", "Banking & Finance", ["suryoday bank"], False, "🏦"),
    ("SBICARD.NS", "SBI Cards and Payment Services", "SBICARD", "NSE", "IN", "Credit Cards & Payments", "Banking & Finance", ["sbi card", "sbi cards", "sbicard"], True, "💳"),
    ("ABCAPITAL.NS", "Aditya Birla Capital Ltd", "ABCAPITAL", "NSE", "IN", "Diversified Financial Services", "Banking & Finance", ["aditya birla capital", "ab capital"], True, "💳"),
    ("CHOLAHLDNG.NS", "Cholamandalam Financial Holdings", "CHOLAHLDNG", "NSE", "IN", "Investment & Financial Holding", "Banking & Finance", ["chola holdings"], False, "💼"),
    ("PNBHOUSING.NS", "PNB Housing Finance Ltd", "PNBHOUSING", "NSE", "IN", "Housing Finance & Mortgages", "Banking & Finance", ["pnb housing", "pnb housing finance"], True, "🏡"),
    ("CANFINHOME.NS", "Can Fin Homes Ltd", "CANFINHOME", "NSE", "IN", "Housing Finance", "Banking & Finance", ["can fin homes", "canfinhome"], False, "🏡"),
    ("AAVAS.NS", "Aavas Financiers Ltd", "AAVAS", "NSE", "IN", "Affordable Housing Finance", "Banking & Finance", ["aavas", "aavas financiers"], False, "🏡"),
    ("HOMEFIRST.NS", "Home First Finance Company", "HOMEFIRST", "NSE", "IN", "Technology Driven Housing Finance", "Banking & Finance", ["home first", "homefirst"], False, "🏡"),
    ("APTUS.NS", "Aptus Value Housing Finance", "APTUS", "NSE", "IN", "Affordable Housing Loans", "Banking & Finance", ["aptus", "aptus housing"], False, "🏡"),
    ("CREDITACC.NS", "CreditAccess Grameen Ltd", "CREDITACC", "NSE", "IN", "Microfinance & Rural Lending", "Banking & Finance", ["creditaccess", "grameen"], True, "🪙"),
    ("SPANDANA.NS", "Spandana Sphoorty Financial", "SPANDANA", "NSE", "IN", "Rural Microfinance NBFC", "Banking & Finance", ["spandana"], False, "🪙"),
    ("FUSION.NS", "Fusion Micro Finance Ltd", "FUSION", "NSE", "IN", "Microfinance Institution", "Banking & Finance", ["fusion micro finance"], False, "🪙"),
    ("MOTILALOFS.NS", "Motilal Oswal Financial Services", "MOTILALOFS", "NSE", "IN", "Wealth & Asset Management, Brokerage", "Banking & Finance", ["motilal oswal", "motilal"], True, "📈"),
    ("ANANDRATHI.NS", "Anand Rathi Wealth Ltd", "ANANDRATHI", "NSE", "IN", "Private Wealth & Financial Solutions", "Banking & Finance", ["anand rathi"], True, "📈"),
    ("GEOJITFSL.NS", "Geojit Financial Services Ltd", "GEOJITFSL", "NSE", "IN", "Retail Brokerage & Financial Products", "Banking & Finance", ["geojit"], False, "📱"),
    ("5PAISA.NS", "5paisa Capital Ltd", "5PAISA", "NSE", "IN", "Discount Online Brokerage", "Banking & Finance", ["5paisa", "five paisa"], False, "📱"),

    # --- IT SERVICES, SAAS & ELECTRONICS EMS ---
    ("NEWGEN.NS", "Newgen Software Technologies", "NEWGEN", "NSE", "IN", "Low Code Digital Transformation", "Tech & IT", ["newgen", "newgen software"], True, "💻"),
    ("TANLA.NS", "Tanla Platforms Ltd", "TANLA", "NSE", "IN", "CPaaS & Cloud Communications", "Tech & IT", ["tanla", "tanla platforms"], True, "💬"),
    ("ROUTE.NS", "Route Mobile Ltd", "ROUTE", "NSE", "IN", "Cloud Communication & Messaging", "Tech & IT", ["route mobile"], False, "📱"),
    ("FSL.NS", "Firstsource Solutions Ltd", "FSL", "NSE", "IN", "Business Process Management (BPM)", "Tech & IT", ["firstsource", "fsl"], True, "🎧"),
    ("ECLERX.NS", "eClerx Services Ltd", "ECLERX", "NSE", "IN", "Financial Analytics & Data Process", "Tech & IT", ["eclerx"], False, "📊"),
    ("MASTEK.NS", "Mastek Ltd", "MASTEK", "NSE", "IN", "Enterprise Digital Engineering", "Tech & IT", ["mastek"], False, "💻"),
    ("CIGNITITEC.NS", "Cigniti Technologies Ltd", "CIGNITITEC", "NSE", "IN", "AI & Digital Engineering Services", "Tech & IT", ["cigniti"], False, "🧪"),
    ("SAKSOFT.NS", "Saksoft Ltd", "SAKSOFT", "NSE", "IN", "Digital Solutions & Fintech IT", "Tech & IT", ["saksoft"], False, "💻"),
    ("DATAMATICS.NS", "Datamatics Global Services", "DATAMATICS", "NSE", "IN", "Intelligent Automation & AI", "Tech & IT", ["datamatics"], False, "🤖"),
    ("AURIONPRO.NS", "Aurionpro Solutions Ltd", "AURIONPRO", "NSE", "IN", "Banking Tech & Smart Mobility", "Tech & IT", ["aurionpro"], True, "🚆"),
    ("AVALON.NS", "Avalon Technologies Ltd", "AVALON", "NSE", "IN", "End-to-End EMS Electronics", "Tech & IT", ["avalon", "avalon tech"], False, "🔌"),
    ("PGEL.NS", "PG Electroplast Ltd", "PGEL", "NSE", "IN", "Electronic Manufacturing & Plastic Moulding", "Tech & IT", ["pg electroplast", "pgel"], True, "🔌"),
    ("CYIENTDLM.NS", "Cyient DLM Ltd", "CYIENTDLM", "NSE", "IN", "Electronics Manufacturing Services", "Tech & IT", ["cyient dlm"], False, "🔌"),
    ("STLTECH.NS", "Sterlite Technologies Ltd", "STLTECH", "NSE", "IN", "Optical Fibre & 5G Connectivity", "Tech & IT", ["sterlite tech", "stl"], False, "📡"),
    ("ITI.NS", "ITI Ltd (Indian Telephone Industries)", "ITI", "NSE", "IN", "Telecom Gear & Defence Encryption PSU", "Tech & IT", ["iti ltd", "iti"], False, "☎️"),

    # --- AUTO COMPONENTS, ANCILLARY & COMMERCIAL VEHICLES ---
    ("FORCEMOT.NS", "Force Motors Ltd", "FORCEMOT", "NSE", "IN", "Commercial Vans, Engines & Tractors", "Auto & EV", ["force motors", "force motor", "forcemot"], True, "🚐"),
    ("UNOMINDA.NS", "Uno Minda Ltd", "UNOMINDA", "NSE", "IN", "Tier 1 Auto Components & EV Electronics", "Auto & EV", ["uno minda", "minda"], True, "🚗"),
    ("ENDURANCE.NS", "Endurance Technologies Ltd", "ENDURANCE", "NSE", "IN", "Two/Three-Wheeler Die Casting & Brakes", "Auto & EV", ["endurance tech", "endurance"], True, "⚙️"),
    ("CRAFTSMAN.NS", "Craftsman Automation Ltd", "CRAFTSMAN", "NSE", "IN", "Precision Engineering & Powertrain", "Auto & EV", ["craftsman automation"], False, "⚙️"),
    ("VARROC.NS", "Varroc Engineering Ltd", "VARROC", "NSE", "IN", "Polymer, Electrical & Lighting Systems", "Auto & EV", ["varroc"], False, "💡"),
    ("GABRIEL.NS", "Gabriel India Ltd", "GABRIEL", "NSE", "IN", "Ride Control & Shock Absorbers", "Auto & EV", ["gabriel", "gabriel india"], False, "🛞"),
    ("SUPRAJIT.NS", "Suprajit Engineering Ltd", "SUPRAJIT", "NSE", "IN", "Automotive Mechanical Cables & Halogen", "Auto & EV", ["suprajit"], False, "⚙️"),
    ("LUMAXTECH.NS", "Lumax Auto Technologies", "LUMAXTECH", "NSE", "IN", "Gear Shifters & Telematics", "Auto & EV", ["lumax auto", "lumaxtech"], False, "⚙️"),
    ("LUMAXIND.NS", "Lumax Industries Ltd", "LUMAXIND", "NSE", "IN", "Automotive Headlamps & LED Lighting", "Auto & EV", ["lumax industries"], False, "💡"),
    ("RKFORGE.NS", "Ramkrishna Forgings Ltd", "RKFORGE", "NSE", "IN", "Heavy Forgings & Railway Axles", "Auto & EV", ["ramkrishna forgings", "rkforge"], True, "🏗️"),
    ("ROLEXRINGS.NS", "Rolex Rings Ltd", "ROLEXRINGS", "NSE", "IN", "Bearing Rings & Automotive Components", "Auto & EV", ["rolex rings"], False, "🛞"),
    ("PRICOLLTD.NS", "Pricol Ltd", "PRICOLLTD", "NSE", "IN", "Instrument Clusters & Telematics", "Auto & EV", ["pricol"], False, "🎛️"),
    ("JAMNAAUTO.NS", "Jamna Auto Industries", "JAMNAAUTO", "NSE", "IN", "Tapered Leaf & Parabolic Springs", "Auto & EV", ["jamna auto"], False, "🚛"),
    ("SUBROS.NS", "Subros Ltd", "SUBROS", "NSE", "IN", "Automotive Air Conditioning", "Auto & EV", ["subros"], False, "❄️"),
    ("SHARDAMOTR.NS", "Sharda Motor Industries", "SHARDAMOTR", "NSE", "IN", "Exhaust Systems & Catalytic Converters", "Auto & EV", ["sharda motor"], False, "💨"),
    ("TVSSRICHAK.NS", "TVS Srichakra Ltd (TVS Eurogrip)", "TVSSRICHAK", "NSE", "IN", "Two-Wheeler & Agri Tyres", "Auto & EV", ["tvs tyres", "tvs eurogrip", "tvssrichak"], False, "🛞"),
    ("GOODYEAR.NS", "Goodyear India Ltd", "GOODYEAR", "NSE", "IN", "Farm & Commercial Tyres", "Auto & EV", ["goodyear", "goodyear india"], False, "🛞"),
    ("ATULAUTO.NS", "Atul Auto Ltd", "ATULAUTO", "NSE", "IN", "Three-Wheeler Commercial Vehicles", "Auto & EV", ["atul auto"], False, "🛺"),

    # --- INFRASTRUCTURE, HIGHWAYS & CIVIL CONSTRUCTION ---
    ("KNRCON.NS", "KNR Constructions Ltd", "KNRCON", "NSE", "IN", "Highways, Expressways & Flyovers EPC", "Infrastructure", ["knr constructions", "knrcon"], True, "🛣️"),
    ("PNCINFRA.NS", "PNC Infratech Ltd", "PNCINFRA", "NSE", "IN", "Highway Concessions & Water Projects", "Infrastructure", ["pnc infratech", "pncinfra"], True, "🛣️"),
    ("GRINFRA.NS", "G R Infraprojects Ltd", "GRINFRA", "NSE", "IN", "Roads, Highways & Metro Rail EPC", "Infrastructure", ["gr infra", "gr infraprojects"], False, "🛣️"),
    ("DILIPBUILD.NS", "Dilip Buildcon Ltd", "DILIPBUILD", "NSE", "IN", "Highway & Urban Infrastructure EPC", "Infrastructure", ["dilip buildcon"], False, "🛣️"),
    ("ASHOKA.NS", "Ashoka Buildcon Ltd", "ASHOKA", "NSE", "IN", "Highway BOT & Smart City Projects", "Infrastructure", ["ashoka buildcon"], False, "🛣️"),
    ("ITDCEM.NS", "ITD Cementation India Ltd", "ITDCEM", "NSE", "IN", "Maritime Structures & Metro Tunneling", "Infrastructure", ["itd cementation", "itdcem"], True, "🚇"),
    ("AHLUCONT.NS", "Ahluwalia Contracts (India) Ltd", "AHLUCONT", "NSE", "IN", "Hospitals, Institutional & Metro Stations", "Infrastructure", ["ahluwalia contracts"], False, "🏗️"),
    ("PSPPROJECT.NS", "PSP Projects Ltd", "PSPPROJECT", "NSE", "IN", "Surat Diamond Bourse & Institutional", "Infrastructure", ["psp projects"], False, "🏢"),
    ("CAPACITE.NS", "Capacit'e Infraprojects Ltd", "CAPACITE", "NSE", "IN", "Super High-Rise Buildings & Hospitals", "Infrastructure", ["capacite"], False, "🏢"),
    ("MANINFRA.NS", "Man Infraconstruction Ltd", "MANINFRA", "NSE", "IN", "Port Infrastructure & Premium Residences", "Infrastructure", ["man infra"], False, "🏗️"),

    # --- METALS, SPECIALTY STEEL, PIPES & MINING ---
    ("HINDZINC.NS", "Hindustan Zinc Ltd (Vedanta)", "HINDZINC", "NSE", "IN", "Zinc, Lead & Silver Smelting", "Metals & Mining", ["hindustan zinc", "hzl", "hindzinc"], True, "🥈"),
    ("HINDCOPPER.NS", "Hindustan Copper Ltd", "HINDCOPPER", "NSE", "IN", "Copper Mining & Smelting PSU", "Metals & Mining", ["hindustan copper"], True, "🥉"),
    ("MOIL.NS", "MOIL Ltd (Manganese Ore India)", "MOIL", "NSE", "IN", "Manganese Ore Mining PSU", "Metals & Mining", ["moil"], True, "⛏️"),
    ("GMDC.NS", "Gujarat Mineral Development Corp", "GMDC", "NSE", "IN", "Lignite & Bauxite Mining PSU", "Metals & Mining", ["gmdc"], True, "⛏️"),
    ("JSL.NS", "Jindal Stainless Ltd", "JSL", "NSE", "IN", "India's Largest Stainless Steel Maker", "Metals & Mining", ["jindal stainless", "jsl"], True, "🏗️"),
    ("JINDALSAW.NS", "Jindal SAW Ltd", "JINDALSAW", "NSE", "IN", "Submerged Arc Welded & Ductile Iron Pipes", "Metals & Mining", ["jindal saw"], True, "🚰"),
    ("APLAPOLLO.NS", "APL Apollo Tubes Ltd", "APLAPOLLO", "NSE", "IN", "Structural Steel ERW Tubes", "Metals & Mining", ["apl apollo"], True, "🏗️"),
    ("RATNAMANI.NS", "Ratnamani Metals & Tubes Ltd", "RATNAMANI", "NSE", "IN", "Seamless Stainless Steel Tubes", "Metals & Mining", ["ratnamani metals"], True, "🚰"),
    ("WELCORP.NS", "Welspun Corp Ltd", "WELCORP", "NSE", "IN", "Large Diameter Pipes & Steel Bars", "Metals & Mining", ["welspun corp", "welcorp"], True, "🚰"),
    ("SHYAMMET.NS", "Shyam Metalics and Energy Ltd", "SHYAMMET", "NSE", "IN", "Long Steel, Pellets & Ferro Alloys", "Metals & Mining", ["shyam metalics"], False, "🏗️"),
    ("JAIBALAJI.NS", "Jai Balaji Industries Ltd", "JAIBALAJI", "NSE", "IN", "Ductile Iron Pipes & Sponge Iron", "Metals & Mining", ["jai balaji"], False, "🏗️"),
    ("LLOYDSME.NS", "Lloyds Metals and Energy Ltd", "LLOYDSME", "NSE", "IN", "Iron Ore Mining & Sponge Iron", "Metals & Mining", ["lloyds metals"], False, "⛏️"),
    ("GODAWARI.NS", "Godawari Power & Ispat Ltd", "GODAWARI", "NSE", "IN", "Iron Ore Pellets & Sponge Iron", "Metals & Mining", ["godawari power"], False, "⚡"),
    ("USHAMART.NS", "Usha Martin Ltd", "USHAMART", "NSE", "IN", "Wire Ropes & Strands", "Metals & Mining", ["usha martin"], False, "🏗️"),
    ("GRAVITA.NS", "Gravita India Ltd", "GRAVITA", "NSE", "IN", "Lead, Aluminium & Plastic Recycling", "Metals & Mining", ["gravita", "gravita india"], True, "♻️"),

    # --- CEMENT, HOME IMPROVEMENT, GLASS & PAINTS ---
    ("JKCEMENT.NS", "JK Cement Ltd", "JKCEMENT", "NSE", "IN", "Grey Cement & White Cement Wall Putty", "Cement & Building Materials", ["jk cement"], True, "🧱"),
    ("STARCEMENT.NS", "Star Cement Ltd", "STARCEMENT", "NSE", "IN", "Northeast India Cement Market Leader", "Cement & Building Materials", ["star cement"], False, "🧱"),
    ("HEIDELBERG.NS", "HeidelbergCement India Ltd", "HEIDELBERG", "NSE", "IN", "Cement & Ready-Mix Concrete", "Cement & Building Materials", ["heidelberg cement"], False, "🧱"),
    ("PRISMJOHN.NS", "Prism Johnson Ltd (H&R Johnson)", "PRISMJOHN", "NSE", "IN", "Cement, Ceramic Tiles & RMC", "Cement & Building Materials", ["prism johnson", "hr johnson"], False, "🧱"),
    ("SAGCEM.NS", "Sagar Cements Ltd", "SAGCEM", "NSE", "IN", "Ordinary Portland & Slag Cement", "Cement & Building Materials", ["sagar cements"], False, "🧱"),
    ("INDIGOPNTS.NS", "Indigo Paints Ltd", "INDIGOPNTS", "NSE", "IN", "Decorative Paints & Exterior Emulsions", "Consumer & Industrials", ["indigo paints"], True, "🎨"),
    ("PRINCEPIPE.NS", "Prince Pipes and Fittings Ltd", "PRINCEPIPE", "NSE", "IN", "PVC Plumbing & Agriculture Piping", "Industrial Engineering", ["prince pipes"], True, "🚰"),
    ("SOMANYCERA.NS", "Somany Ceramics Ltd", "SOMANYCERA", "NSE", "IN", "Vitrified Tiles & Sanitaryware", "Consumer & Industrials", ["somany ceramics", "somany"], False, "🧱"),
    ("ORIENTBELL.NS", "Orient Bell Ltd", "ORIENTBELL", "NSE", "IN", "Floor & Wall Ceramic Tiles", "Consumer & Industrials", ["orient bell"], False, "🧱"),
    ("GREENPANEL.NS", "Greenpanel Industries Ltd", "GREENPANEL", "NSE", "IN", "India's Largest Wood MDF Manufacturer", "Consumer & Industrials", ["greenpanel", "mdf"], True, "🪵"),
    ("GREENPLY.NS", "Greenply Industries Ltd", "GREENPLY", "NSE", "IN", "Plywood & Decorative Veneers", "Consumer & Industrials", ["greenply"], False, "🪵"),
    ("ASAHIINDIA.NS", "Asahi India Glass Ltd (AIS)", "ASAHIINDIA", "NSE", "IN", "Automotive & Architectural Glass", "Consumer & Industrials", ["asahi india", "ais glass"], True, "🪟"),
    ("BOROLTD.NS", "Borosil Ltd", "BOROLTD", "NSE", "IN", "Microwavable Glassware & Kitchenware", "Consumer & Industrials", ["borosil"], True, "🍵"),
    ("LAOPALA.NS", "La Opala RG Ltd", "LAOPALA", "NSE", "IN", "Opal Glass Tableware & Dinner Sets", "Consumer & Industrials", ["la opala"], False, "🍽️"),

    # --- CONSUMER GOODS, APPLIANCES, LUGGAGE & STATIONERY ---
    ("ORIENTELEC.NS", "Orient Electric Ltd", "ORIENTELEC", "NSE", "IN", "Fans, Lighting & Home Appliances", "Consumer & Industrials", ["orient electric"], False, "💡"),
    ("BAJAJELEC.NS", "Bajaj Electricals Ltd", "BAJAJELEC", "NSE", "IN", "Consumer Lighting & Kitchen Appliances", "Consumer & Industrials", ["bajaj electricals"], True, "💡"),
    ("IFBIND.NS", "IFB Industries Ltd", "IFBIND", "NSE", "IN", "Washing Machines & Kitchen Appliances", "Consumer & Industrials", ["ifb", "ifb industries"], True, "🧺"),
    ("TTKPRESTIG.NS", "TTK Prestige Ltd", "TTKPRESTIG", "NSE", "IN", "Pressure Cookers & Kitchen Cookware", "Consumer & Industrials", ["prestige cooker", "ttk prestige"], True, "🍳"),
    ("HAWKINCOOK.BO", "Hawkins Cookers Ltd", "HAWKINCOOK", "BSE", "IN", "Pressure Cookers & Cookware", "Consumer & Industrials", ["hawkins", "hawkins cookers"], True, "🍳"),
    ("VIPIND.NS", "VIP Industries Ltd (Skybags/Carlton)", "VIPIND", "NSE", "IN", "Luggage & Travel Accessories", "FMCG & Retail", ["vip luggage", "skybags", "vip industries"], True, "🧳"),
    ("SAFARI.NS", "Safari Industries (India) Ltd", "SAFARI", "NSE", "IN", "Hard & Soft Luggage Bags", "FMCG & Retail", ["safari luggage", "safari"], True, "🧳"),
    ("CELLO.NS", "Cello World Ltd", "CELLO", "NSE", "IN", "Consumer Houseware, Opalware & Pens", "Consumer & Industrials", ["cello", "cello world"], True, "🍶"),
    ("DOMS.NS", "DOMS Industries Ltd", "DOMS", "NSE", "IN", "Stationery, Art Materials & Pencils", "Consumer & Industrials", ["doms", "doms industries", "doms pencil"], True, "✏️"),
    ("FLAIR.NS", "Flair Writing Industries Ltd", "FLAIR", "NSE", "IN", "Writing Instruments & Pens", "Consumer & Industrials", ["flair", "flair pens"], True, "🖊️"),
    ("LINC.NS", "Linc Ltd (Pentonic)", "LINC", "NSE", "IN", "Ballpoint & Gel Pens (Pentonic)", "Consumer & Industrials", ["linc", "pentonic"], False, "🖊️"),
    ("CAMLIN.NS", "Kokuyo Camlin Ltd", "CAMLIN", "NSE", "IN", "Art Supplies, Paints & Geometry Boxes", "Consumer & Industrials", ["camlin", "kokuyo camlin"], False, "🎨"),

    # --- TEXTILES, INNERWEAR & BRANDED APPAREL ---
    ("KPRMILL.NS", "K.P.R. Mill Ltd", "KPRMILL", "NSE", "IN", "Yarn, Knitted Apparel & Sugar", "FMCG & Retail", ["kpr mill"], True, "🧵"),
    ("TRIDENT.NS", "Trident Ltd", "TRIDENT", "NSE", "IN", "Terry Towels, Yarn & Wheat Straw Paper", "FMCG & Retail", ["trident", "trident ltd"], True, "🛁"),
    ("WELSPUNLIV.NS", "Welspun Living Ltd", "WELSPUNLIV", "NSE", "IN", "Home Textiles (Bed & Bath)", "FMCG & Retail", ["welspun living", "welspun india"], True, "🛏️"),
    ("ALOKINDS.NS", "Alok Industries Ltd (Reliance)", "ALOKINDS", "NSE", "IN", "Integrated Textiles & Apparel", "FMCG & Retail", ["alok industries"], True, "🧵"),
    ("RUPA.NS", "Rupa & Company Ltd (Frontline)", "RUPA", "NSE", "IN", "Innerwear, Thermal & Casualwear", "FMCG & Retail", ["rupa", "rupa frontline"], False, "🩲"),
    ("LUXIND.NS", "Lux Industries Ltd (Lux Cozi)", "LUXIND", "NSE", "IN", "Hosiery & Innerwear Brands", "FMCG & Retail", ["lux cozi", "lux industries"], False, "🩲"),
    ("DOLLAR.NS", "Dollar Industries Ltd", "DOLLAR", "NSE", "IN", "Hosiery & Knitwear", "FMCG & Retail", ["dollar club", "dollar industries"], False, "🩲"),
    ("SHOPERSTOP.NS", "Shoppers Stop Ltd", "SHOPERSTOP", "NSE", "IN", "Department Stores & Beauty Retailing", "FMCG & Retail", ["shoppers stop"], True, "🛍️"),
    ("ARVIND.NS", "Arvind Ltd", "ARVIND", "NSE", "IN", "Denim, Woven Fabrics & Branded Apparel", "FMCG & Retail", ["arvind", "arvind mills"], False, "👖"),
    ("GOKEX.NS", "Gokaldas Exports Ltd", "GOKEX", "NSE", "IN", "Garment Manufacturing & Exports", "FMCG & Retail", ["gokaldas exports"], False, "👔"),
    ("ETHOSLTD.NS", "Ethos Ltd", "ETHOSLTD", "NSE", "IN", "Luxury Swiss Watch Retailing", "FMCG & Retail", ["ethos watches", "ethos"], True, "⌚"),
    ("THANGAMAYL.NS", "Thangamayil Jewellery Ltd", "THANGAMAYL", "NSE", "IN", "Gold, Silver & Diamond Jewellery", "FMCG & Retail", ["thangamayil"], False, "💍"),
    ("PCJEWELLER.NS", "PC Jeweller Ltd", "PCJEWELLER", "NSE", "IN", "Gold & Diamond Jewellery Retail", "FMCG & Retail", ["pc jeweller", "pcj"], False, "💍"),

    # --- FOODS, DAIRY, AGRI, POULTRY & SUGAR ---
    ("BECTORFOOD.NS", "Mrs. Bectors Food Specialities", "BECTORFOOD", "NSE", "IN", "Cremica Biscuits & English Oven Breads", "FMCG & Retail", ["mrs bectors", "cremica", "english oven"], True, "🍞"),
    ("ADFFOODS.NS", "ADF Foods Ltd (Ashoka)", "ADFFOODS", "NSE", "IN", "Indian Meal Pickles, Pastes & Frozen", "FMCG & Retail", ["adf foods", "ashoka foods"], False, "🍛"),
    ("LTFOODS.NS", "LT Foods Ltd (Daawat Basmati)", "LTFOODS", "NSE", "IN", "Specialty Basmati Rice & Organic", "FMCG & Retail", ["daawat", "daawat rice", "lt foods"], True, "🍚"),
    ("KRBL.NS", "KRBL Ltd (India Gate Basmati)", "KRBL", "NSE", "IN", "India Gate Basmati Rice & Milling", "FMCG & Retail", ["india gate", "india gate rice", "krbl"], True, "🍚"),
    ("CCL.NS", "CCL Products (India) Ltd", "CCL", "NSE", "IN", "Instant Soluble Coffee Processor", "FMCG & Retail", ["ccl products", "ccl coffee"], True, "☕"),
    ("AVANTIFEED.NS", "Avanti Feeds Ltd", "AVANTIFEED", "NSE", "IN", "Shrimp Feeds & Processing", "FMCG & Retail", ["avanti feeds"], True, "🦐"),
    ("APEX.NS", "Apex Frozen Foods Ltd", "APEX", "NSE", "IN", "Aquaculture & Frozen Seafood", "FMCG & Retail", ["apex frozen foods"], False, "🦐"),
    ("VENKEYS.NS", "Venky's (India) Ltd", "VENKEYS", "NSE", "IN", "Poultry Breeding, Animal Health & Food", "FMCG & Retail", ["venkys", "venky's"], True, "🍗"),
    ("GODREJAGRO.NS", "Godrej Agrovet Ltd", "GODREJAGRO", "NSE", "IN", "Animal Feed, Palm Oil & Crop Protection", "FMCG & Retail", ["godrej agrovet"], True, "🌾"),
    ("HERITGFOOD.NS", "Heritage Foods Ltd", "HERITGFOOD", "NSE", "IN", "Dairy Products, Milk & Curd", "FMCG & Retail", ["heritage foods", "heritage milk"], True, "🥛"),
    ("PARAGMILK.NS", "Parag Milk Foods Ltd (Gowardhan/Go)", "PARAGMILK", "NSE", "IN", "Gowardhan Ghee, Go Cheese & Dairy", "FMCG & Retail", ["gowardhan", "go cheese", "parag milk"], True, "🧀"),
    ("DODLA.NS", "Dodla Dairy Ltd", "DODLA", "NSE", "IN", "Fresh Milk & Fermented Dairy Products", "FMCG & Retail", ["dodla dairy", "dodla"], False, "🥛"),
    ("HATSUN.NS", "Hatsun Agro Product Ltd (Arokya/Arun)", "HATSUN", "NSE", "IN", "Arokya Milk, Arun Icecreams & Ibaco", "FMCG & Retail", ["arun icecream", "arokya milk", "hatsun"], True, "🍦"),
    ("VADILALIND.NS", "Vadilal Industries Ltd", "VADILALIND", "NSE", "IN", "Ice Creams & Frozen Foods", "FMCG & Retail", ["vadilal", "vadilal icecream"], False, "🍨"),
    ("ZYDUSWELL.NS", "Zydus Wellness Ltd", "ZYDUSWELL", "NSE", "IN", "Complan, Sugar Free, Glucon-D & Nycil", "FMCG & Retail", ["complan", "sugar free", "zydus wellness"], True, "🥤"),
    ("PRATAAP.NS", "Prataap Snacks Ltd (Yellow Diamond)", "PRATAAP", "NSE", "IN", "Yellow Diamond Potato Chips & Namkeen", "FMCG & Retail", ["yellow diamond", "prataap snacks"], False, "🥔"),
    ("EIDPARRY.NS", "E.I.D. - Parry (India) Ltd", "EIDPARRY", "NSE", "IN", "Refined Sugar, Ethanol & Nutraceuticals", "FMCG & Retail", ["eid parry", "parry sugar"], True, "🍬"),
    ("BALRAMCHIN.NS", "Balrampur Chini Mills Ltd", "BALRAMCHIN", "NSE", "IN", "Integrated Sugar, Power & Fuel Ethanol", "FMCG & Retail", ["balrampur chini"], True, "🍬"),
    ("TRIVENI.NS", "Triveni Engineering & Industries", "TRIVENI", "NSE", "IN", "Sugar Manufacturing & Engineering", "FMCG & Retail", ["triveni engineering"], False, "🍬"),
    ("RENUKA.NS", "Shree Renuka Sugars Ltd", "RENUKA", "NSE", "IN", "Refined Sugar & Fuel Ethanol", "FMCG & Retail", ["renuka sugars", "shree renuka"], True, "🍬"),

    # --- BEVERAGES, BREWERIES & RESTAURANT CHAINS ---
    ("TI.NS", "Tilaknagar Industries (Mansion House)", "TI", "NSE", "IN", "Mansion House Brandy & Premium Liquor", "FMCG & Retail", ["mansion house", "tilaknagar"], True, "🥃"),
    ("SAPPHIRE.NS", "Sapphire Foods India (KFC/Pizza Hut)", "SAPPHIRE", "NSE", "IN", "QSR Franchisee Operator", "FMCG & Retail", ["sapphire foods"], True, "🍗"),
    ("RBA.NS", "Restaurant Brands Asia (Burger King)", "RBA", "NSE", "IN", "Burger King India & Popeyes", "FMCG & Retail", ["burger king india", "rba"], True, "🍔"),
    ("BARBEQUE.NS", "Barbeque-Nation Hospitality Ltd", "BARBEQUE", "NSE", "IN", "Casual Dining Barbeque Buffets", "FMCG & Retail", ["barbeque nation"], False, "🍢"),

    # --- PHARMACEUTICALS, APIS, CONTRACT CDMO & DIAGNOSTICS ---
    ("AJANTPHARM.NS", "Ajanta Pharma Ltd", "AJANTPHARM", "NSE", "IN", "Ophthalmology, Dermatology & Cardiology", "Pharma & Health", ["ajanta pharma"], True, "💊"),
    ("APLLTD.NS", "Alembic Pharmaceuticals Ltd", "APLLTD", "NSE", "IN", "Active Pharmaceutical Formulations", "Pharma & Health", ["alembic pharma", "alembic"], False, "💊"),
    ("AARTIDRUGS.NS", "Aarti Drugs Ltd", "AARTIDRUGS", "NSE", "IN", "Active Pharmaceutical Ingredients (APIs)", "Pharma & Health", ["aarti drugs"], False, "🧪"),
    ("STRIDES.NS", "Strides Pharma Science Ltd", "STRIDES", "NSE", "IN", "Niche Finished Dosage Formulations", "Pharma & Health", ["strides pharma", "strides"], False, "💊"),
    ("NEULANDLAB.NS", "Neuland Laboratories Ltd", "NEULANDLAB", "NSE", "IN", "Complex API & CDMO Chemistry", "Pharma & Health", ["neuland labs"], True, "🔬"),
    ("MARKSANS.NS", "Marksans Pharma Ltd", "MARKSANS", "NSE", "IN", "OTC & Prescription Generics", "Pharma & Health", ["marksans pharma"], False, "💊"),
    ("CAPL.NS", "Caplin Point Laboratories Ltd", "CAPL", "NSE", "IN", "Injectables & Global Formulations", "Pharma & Health", ["caplin point"], False, "💉"),
    ("FDC.NS", "FDC Ltd (Electral ORS/Zifi)", "FDC", "NSE", "IN", "Electral Oral Rehydration & Antibiotics", "Pharma & Health", ["electral", "fdc"], False, "🥤"),
    ("POLYMED.NS", "Poly Medicure Ltd", "POLYMED", "NSE", "IN", "Medical Devices, IV Cannulas & Catheters", "Pharma & Health", ["poly medicure", "polymed"], True, "🩹"),
    ("NH.NS", "Narayana Hrudayalaya Ltd", "NH", "NSE", "IN", "Cardiac Care Hospitals & Health Network", "Pharma & Health", ["narayana hrudayalaya", "narayana health"], True, "🏥"),
    ("KIMS.NS", "Krishna Institute of Medical Sciences", "KIMS", "NSE", "IN", "Multi-Speciality Hospital Chain", "Pharma & Health", ["kims hospital", "kims"], True, "🏥"),
    ("YATHARTH.NS", "Yatharth Hospital & Trauma Care", "YATHARTH", "NSE", "IN", "Super-Specialty Tertiary Care Hospitals", "Pharma & Health", ["yatharth hospital"], False, "🏥"),
    ("VIJAYA.NS", "Vijaya Diagnostic Centre Ltd", "VIJAYA", "NSE", "IN", "Integrated Pathology & Radiology Labs", "Pharma & Health", ["vijaya diagnostic"], False, "🔬"),
    ("THYROCARE.NS", "Thyrocare Technologies Ltd", "THYROCARE", "NSE", "IN", "Preventive Healthcare Diagnostic Labs", "Pharma & Health", ["thyrocare"], False, "🧪"),
    ("ABBOTINDIA.NS", "Abbott India Ltd", "ABBOTINDIA", "NSE", "IN", "Multinational Pharmaceuticals (Thyronorm)", "Pharma & Health", ["abbott", "abbott india"], True, "💊"),
    ("PFIZER.NS", "Pfizer Ltd (India)", "PFIZER", "NSE", "IN", "Biopharmaceuticals & Vaccines", "Pharma & Health", ["pfizer india"], False, "💊"),
    ("SANOFI.NS", "Sanofi India Ltd", "SANOFI", "NSE", "IN", "Diabetes Care & Vaccines (Lantus)", "Pharma & Health", ["sanofi india"], False, "💊"),
    ("GLAXO.NS", "GlaxoSmithKline Pharmaceuticals India", "GLAXO", "NSE", "IN", "Prescription Medicines & Vaccines", "Pharma & Health", ["gsk india", "glaxo"], False, "💊"),
    ("PGHH.NS", "Procter & Gamble Hygiene and Health", "PGHH", "NSE", "IN", "Whisper Feminine Hygiene & Vicks", "FMCG & Retail", ["whisper", "vicks", "pghh"], True, "🩹"),
    ("GILLETTE.NS", "Gillette India Ltd", "GILLETTE", "NSE", "IN", "Gillette Shaving Blades & Oral-B", "FMCG & Retail", ["gillette", "oral-b"], True, "🪒"),

    # --- SPECIALTY CHEMICALS & FERTILIZERS ---
    ("AETHER.NS", "Aether Industries Ltd", "AETHER", "NSE", "IN", "Advanced Intermediates & Specialty Chem", "Chemicals & Industrials", ["aether", "aether industries"], True, "🧪"),
    ("CLEAN.NS", "Clean Science and Technology", "CLEAN", "NSE", "IN", "Eco-Friendly Specialty Chemicals (BHA)", "Chemicals & Industrials", ["clean science"], True, "🌱"),
    ("FINEORG.NS", "Fine Organic Industries Ltd", "FINEORG", "NSE", "IN", "Oleochemical Green Additives", "Chemicals & Industrials", ["fine organic"], True, "🧪"),
    ("ATUL.NS", "Atul Ltd", "ATUL", "NSE", "IN", "Specialty Chemicals, Dyes & Polymers", "Chemicals & Industrials", ["atul"], False, "🧪"),
    ("NAVINFLUOR.NS", "Navin Fluorine International", "NAVINFLUOR", "NSE", "IN", "Refrigerants & Specialty Fluorochemicals", "Chemicals & Industrials", ["navin fluorine"], True, "🧪"),
    ("ALKYLAMINE.NS", "Alkyl Amines Chemicals Ltd", "ALKYLAMINE", "NSE", "IN", "Aliphatic Amines & Amine Derivatives", "Chemicals & Industrials", ["alkyl amines"], False, "🧪"),
    ("BALAMINES.NS", "Balaji Amines Ltd", "BALAMINES", "NSE", "IN", "Methylamines & Specialty Chemicals", "Chemicals & Industrials", ["balaji amines"], False, "🧪"),
    ("SUMICHEM.NS", "Sumitomo Chemical India Ltd", "SUMICHEM", "NSE", "IN", "Household Insecticides & Crop Protection", "Chemicals & Industrials", ["sumitomo chemical", "sumichem"], True, "🌾"),
    ("DHANUKA.NS", "Dhanuka Agritech Ltd", "DHANUKA", "NSE", "IN", "Herbicides & Plant Growth Regulators", "Chemicals & Industrials", ["dhanuka"], False, "🌾"),
    ("RALLIS.NS", "Rallis India Ltd (Tata Enterprise)", "RALLIS", "NSE", "IN", "Agrochemicals, Seeds & Soil Nutrients", "Chemicals & Industrials", ["rallis", "rallis india"], False, "🌱"),
    ("DEEPAKFERT.NS", "Deepak Fertilisers and Petrochem", "DEEPAKFERT", "NSE", "IN", "Technical Ammonium Nitrate & Nitric Acid", "Chemicals & Industrials", ["deepak fertilisers", "deepakfert"], True, "🌾"),
    ("GSFC.NS", "Gujarat State Fertilizers & Chemicals", "GSFC", "NSE", "IN", "Fertilizers & Industrial Caprolactam", "Chemicals & Industrials", ["gsfc"], False, "🌾"),
    ("RCF.NS", "Rashtriya Chemicals and Fertilizers", "RCF", "NSE", "IN", "Urea & Complex Fertilizers PSU", "Chemicals & Industrials", ["rcf"], False, "🌾"),
    ("FACT.NS", "Fertilisers and Chemicals Travancore", "FACT", "NSE", "IN", "Ammonium Phosphate Fertilizers PSU", "Chemicals & Industrials", ["fact"], False, "🌾"),
    ("ANURAS.NS", "Anupam Rasayan India Ltd", "ANURAS", "NSE", "IN", "Custom Synthesis & Life Science Specialty", "Chemicals & Industrials", ["anupam rasayan"], False, "🧪"),
    ("ROSSARI.NS", "Rossari Biotech Ltd", "ROSSARI", "NSE", "IN", "Textile Specialty Chemicals & Animal Health", "Chemicals & Industrials", ["rossari biotech"], False, "🧪"),
    ("NEOGEN.NS", "Neogen Chemicals Ltd", "NEOGEN", "NSE", "IN", "Lithium Battery Salts & Bromine Chem", "Chemicals & Industrials", ["neogen chemicals"], True, "🔋"),
    ("AMIORG.NS", "Ami Organics Ltd", "AMIORG", "NSE", "IN", "Pharma Intermediates & Electrolytes", "Chemicals & Industrials", ["ami organics"], False, "🧪"),

    # --- CAPITAL GOODS, HEAVY MACHINERY & BEARINGS ---
    ("KEC.NS", "KEC International Ltd (RPG Group)", "KEC", "NSE", "IN", "Power Transmission EPC & Railways", "Industrial Engineering", ["kec international", "kec"], True, "⚡"),
    ("KPIL.NS", "Kalpataru Projects International", "KPIL", "NSE", "IN", "Power Transmission, Oil & Gas EPC", "Industrial Engineering", ["kalpataru projects", "kpil"], True, "⚡"),
    ("ENGINERSIN.NS", "Engineers India Ltd (EIL)", "ENGINERSIN", "NSE", "IN", "Hydrocarbon & Petrochemical Engineering PSU", "Industrial Engineering", ["engineers india", "eil"], True, "📐"),
    ("PRAJIND.NS", "Praj Industries Ltd", "PRAJIND", "NSE", "IN", "Bioethanol Plants & 2G Biorefineries", "Industrial Engineering", ["praj industries", "praj"], True, "🌱"),
    ("TRITURBINE.NS", "Triveni Turbine Ltd", "TRITURBINE", "NSE", "IN", "Industrial Steam Turbines", "Industrial Engineering", ["triveni turbine"], True, "⚙️"),
    ("ELECON.NS", "Elecon Engineering Co Ltd", "ELECON", "NSE", "IN", "Industrial Gearboxes & Material Handling", "Industrial Engineering", ["elecon engineering"], True, "⚙️"),
    ("TIMKEN.NS", "Timken India Ltd", "TIMKEN", "NSE", "IN", "Engineered Bearings & Power Transmission", "Industrial Engineering", ["timken", "timken india"], True, "🛞"),
    ("SCHAEFFLER.NS", "Schaeffler India Ltd", "SCHAEFFLER", "NSE", "IN", "Ball & Roller Bearings (FAG/INA)", "Industrial Engineering", ["schaeffler", "fag bearings"], True, "🛞"),
    ("SKFINDIA.NS", "SKF India Ltd", "SKFINDIA", "NSE", "IN", "Precision Bearings & Lubrication", "Industrial Engineering", ["skf", "skf india"], True, "🛞"),
    ("AIAENG.NS", "AIA Engineering Ltd", "AIAENG", "NSE", "IN", "High Chrome Grinding Media for Cement", "Industrial Engineering", ["aia engineering"], False, "⚙️"),
    ("HONAUT.NS", "Honeywell Automation India Ltd", "HONAUT", "NSE", "IN", "Industrial Automation & Building Control", "Industrial Engineering", ["honeywell automation"], True, "🤖"),
    ("3MINDIA.NS", "3M India Ltd", "3MINDIA", "NSE", "IN", "Scotch Adhesives, Abrasives & Healthcare", "Consumer & Industrials", ["3m india", "3m"], True, "🧰"),
    ("CARBORUNIV.NS", "Carborundum Universal Ltd (CUMI)", "CARBORUNIV", "NSE", "IN", "Abrasives, Industrial Ceramics & Refractories", "Industrial Engineering", ["carborundum universal", "cumi"], False, "🪨"),
    ("GRINDWELL.NS", "Grindwell Norton Ltd (Saint-Gobain)", "GRINDWELL", "NSE", "IN", "Silicon Carbide Abrasives & Ceramics", "Industrial Engineering", ["grindwell norton"], False, "🪨"),

    # --- REAL ESTATE & RESIDENTIAL DEVELOPERS ---
    ("KEYSTONE.NS", "Keystone Realtors Ltd (Rustomjee)", "KEYSTONE", "NSE", "IN", "Urban Gated Communities & Redevelopment", "Real Estate", ["rustomjee", "keystone"], True, "🏢"),
    ("KOLTEPATIL.NS", "Kolte-Patil Developers Ltd", "KOLTEPATIL", "NSE", "IN", "Integrated Townships & Residential", "Real Estate", ["kolte patil"], False, "🏢"),
    ("PURVA.NS", "Puravankara Ltd", "PURVA", "NSE", "IN", "Luxury & Theme-Based Residences", "Real Estate", ["puravankara"], False, "🏢"),
    ("MAHLIFE.NS", "Mahindra Lifespace Developers", "MAHLIFE", "NSE", "IN", "Sustainable Green Homes & Smart Cities", "Real Estate", ["mahindra lifespaces"], True, "🏡"),
    ("ASHIANA.NS", "Ashiana Housing Ltd", "ASHIANA", "NSE", "IN", "Senior Living & Kid-Centric Homes", "Real Estate", ["ashiana housing"], False, "🏡"),
    ("AJMERA.NS", "Ajmera Realty & Infra India", "AJMERA", "NSE", "IN", "Residential Township Development", "Real Estate", ["ajmera realty"], False, "🏢"),
    ("TARC.NS", "TARC Ltd", "TARC", "NSE", "IN", "Luxury High-End Residences in Delhi NCR", "Real Estate", ["tarc"], False, "🏙️"),
    ("CENTURYTEX.NS", "Century Textiles (Birla Estates)", "CENTURYTEX", "NSE", "IN", "Premium Real Estate & Pulp Paper", "Real Estate", ["birla estates", "century textiles"], True, "🏢"),

    # --- MEDIA, BROADCASTING, PUBLISHING & HOTELS ---
    ("NETWORK18.NS", "Network18 Media & Investments", "NETWORK18", "NSE", "IN", "JioCinema, News18 & Media Conglomerate", "Media & Entertainment", ["network18", "jiocinema"], True, "📺"),
    ("TV18BRDCST.NS", "TV18 Broadcast Ltd", "TV18BRDCST", "NSE", "IN", "CNBC-TV18, CNN-News18 & Regional News", "Media & Entertainment", ["tv18", "cnbc tv18"], False, "📺"),
    ("DISHTV.NS", "Dish TV India Ltd", "DISHTV", "NSE", "IN", "Direct-To-Home (DTH) Satellite Television", "Media & Entertainment", ["dish tv"], False, "📡"),
    ("DEN.NS", "Den Networks Ltd", "DEN", "NSE", "IN", "Digital Cable Television & Fixed Broadband", "Media & Entertainment", ["den networks"], False, "📺"),
    ("HATHWAY.NS", "Hathway Cable & Datacom Ltd", "HATHWAY", "NSE", "IN", "Fibre-to-the-Home Broadband & Cable", "Media & Entertainment", ["hathway"], False, "🌐"),
    ("DBCORP.NS", "D.B. Corp Ltd (Dainik Bhaskar)", "DBCORP", "NSE", "IN", "Print Newspaper & Digital Media Apps", "Media & Entertainment", ["dainik bhaskar", "db corp"], True, "📰"),
    ("JAGRAN.NS", "Jagran Prakashan Ltd (Dainik Jagran)", "JAGRAN", "NSE", "IN", "Print Newspaper & OOH Advertising", "Media & Entertainment", ["dainik jagran", "jagran"], False, "📰"),
    ("MHRIL.NS", "Mahindra Holidays & Resorts India", "MHRIL", "NSE", "IN", "Club Mahindra Vacation Timeshare", "Hotels & Tourism", ["club mahindra", "mahindra holidays"], True, "🏖️"),
    ("SAMHI.NS", "SAMHI Hotels Ltd", "SAMHI", "NSE", "IN", "Marriott, Fairfield & Holiday Inn Chain", "Hotels & Tourism", ["samhi hotels", "samhi"], False, "🏨"),
    ("PARK.NS", "Apeejay Surrendra Park Hotels", "PARK", "NSE", "IN", "Boutique Luxury Hotels (The Park)", "Hotels & Tourism", ["the park hotel", "park hotels"], False, "🏨"),
    ("TAJGVK.NS", "Taj GVK Hotels & Resorts", "TAJGVK", "NSE", "IN", "Luxury Five-Star Hotels (Taj Brand)", "Hotels & Tourism", ["taj gvk"], False, "🏨"),
    ("BLS.NS", "BLS International Services Ltd", "BLS", "NSE", "IN", "Visa Processing & Citizen Tech Services", "Hotels & Tourism", ["bls international", "bls"], True, "🛂"),
    ("THOMASCOOK.NS", "Thomas Cook (India) Ltd", "THOMASCOOK", "NSE", "IN", "Omnichannel Travel & Forex Remittances", "Hotels & Tourism", ["thomas cook"], True, "🧳"),

    # --- US MEGA-CAP TECH, CYBERSECURITY & AI GIANTS ---
    ("CRWD", "CrowdStrike Holdings Inc", "CRWD", "NASDAQ", "US", "Cloud Cybersecurity & Falcon AI Platform", "Global Mega-Caps", ["crowdstrike", "crwd"], True, "🦅"),
    ("PANW", "Palo Alto Networks Inc", "PANW", "NASDAQ", "US", "Next-Gen Enterprise Cybersecurity", "Global Mega-Caps", ["palo alto networks", "panw"], True, "🛡️"),
    ("NOW", "ServiceNow Inc", "NOW", "NYSE", "US", "Enterprise Cloud Workflow Automation", "Global Mega-Caps", ["servicenow", "now"], True, "⚡"),
    ("INTU", "Intuit Inc", "INTU", "NASDAQ", "US", "Financial & Tax Software (TurboTax/QuickBooks)", "Global Mega-Caps", ["intuit", "turbotax", "quickbooks"], True, "🧾"),
    ("ADSK", "Autodesk Inc", "ADSK", "NASDAQ", "US", "3D Architecture & CAD Software (AutoCAD)", "Global Mega-Caps", ["autodesk", "autocad"], True, "📐"),
    ("TXN", "Texas Instruments Inc", "TXN", "NASDAQ", "US", "Analog & Embedded Semiconductor Chips", "Global Mega-Caps", ["texas instruments", "ti"], True, "🔌"),
    ("AMAT", "Applied Materials Inc", "AMAT", "NASDAQ", "US", "Semiconductor Wafer Fab Equipment", "Global Mega-Caps", ["applied materials", "amat"], True, "🔬"),
    ("LRCX", "Lam Research Corporation", "LRCX", "NASDAQ", "US", "Semiconductor Etching Equipment", "Global Mega-Caps", ["lam research", "lrcx"], True, "🔬"),
    ("KLAC", "KLA Corporation", "KLAC", "NASDAQ", "US", "Semiconductor Process Metrology", "Global Mega-Caps", ["kla", "klac"], True, "🔬"),
    ("MRVL", "Marvell Technology Inc", "MRVL", "NASDAQ", "US", "Custom AI Silicon & Data Center Chips", "Global Mega-Caps", ["marvell", "mrvl"], True, "💻"),
    ("DELL", "Dell Technologies Inc", "DELL", "NYSE", "US", "AI Hardware Infrastructure & Servers", "Global Mega-Caps", ["dell", "dell tech"], True, "🖥️"),
    ("HPQ", "HP Inc", "HPQ", "NYSE", "US", "Personal Systems & Printing", "Global Mega-Caps", ["hp", "hp inc"], False, "🖨️"),
    ("HOOD", "Robinhood Markets Inc", "HOOD", "NASDAQ", "US", "Modern Retail Investing App & Crypto", "Global Mega-Caps", ["robinhood", "hood"], True, "🏹"),
    ("SOFI", "SoFi Technologies Inc", "SOFI", "NASDAQ", "US", "Digital Consumer Banking & Lending", "Global Mega-Caps", ["sofi"], True, "📱"),
    ("SQ", "Block Inc (Square & Cash App)", "SQ", "NYSE", "US", "Merchant Point-of-Sale & Digital Payments", "Global Mega-Caps", ["block", "square", "cash app"], True, "🟩"),
    ("AFRM", "Affirm Holdings Inc", "AFRM", "NASDAQ", "US", "Buy Now Pay Later (BNPL) Consumer Lending", "Global Mega-Caps", ["affirm"], False, "💳"),
    ("NU", "Nu Holdings Ltd (Nubank)", "NU", "NYSE", "US", "Digital Neo-Banking Latin America", "Global Mega-Caps", ["nubank", "nu"], True, "💜"),
    ("MELI", "MercadoLibre Inc", "MELI", "NASDAQ", "US", "E-Commerce & Mercado Pago Latin America", "Global Mega-Caps", ["mercadolibre", "meli"], True, "📦"),
    ("SE", "Sea Limited (Shopee)", "SE", "NYSE", "US", "E-Commerce & Digital Entertainment", "Global Mega-Caps", ["shopee", "sea limited"], True, "🛍️"),
    ("GRAB", "Grab Holdings Ltd", "GRAB", "NASDAQ", "US", "Super-App Ride-Hailing & Deliveries SEA", "Global Mega-Caps", ["grab"], False, "🚗"),
    ("RDDT", "Reddit Inc", "RDDT", "NYSE", "US", "Community Discussions & Social Content", "Global Mega-Caps", ["reddit", "rddt"], True, "🤖"),
    ("SNAP", "Snap Inc (Snapchat)", "SNAP", "NYSE", "US", "Visual Messaging & Augmented Reality", "Global Mega-Caps", ["snapchat", "snap"], False, "👻"),
    ("PINS", "Pinterest Inc", "PINS", "NYSE", "US", "Visual Discovery & Lifestyle Curation", "Global Mega-Caps", ["pinterest", "pins"], False, "📌"),
    ("TTD", "The Trade Desk Inc", "TTD", "NASDAQ", "US", "Independent Programmatic Ad Buying", "Global Mega-Caps", ["the trade desk", "ttd"], True, "📊"),
    ("APP", "AppLovin Corporation", "APP", "NASDAQ", "US", "Mobile App Monetization & AI Ad Engine", "Global Mega-Caps", ["applovin", "app"], True, "📈"),
    ("PATH", "UiPath Inc", "PATH", "NYSE", "US", "Robotic Process Automation (RPA) & AI Agents", "Global Mega-Caps", ["uipath", "path"], False, "🤖"),
    ("U", "Unity Software Inc", "U", "NYSE", "US", "Real-Time 3D Game Engine & Metaverse", "Global Mega-Caps", ["unity", "unity software"], False, "🎮"),
    ("RBLX", "Roblox Corporation", "RBLX", "NYSE", "US", "Immersive Multiplayer Gaming Platform", "Global Mega-Caps", ["roblox", "rblx"], True, "🕹️"),
    ("RIVN", "Rivian Automotive Inc", "RIVN", "NASDAQ", "US", "Electric Adventure Pickups & Delivery Vans", "Global Mega-Caps", ["rivian", "rivn"], True, "🚙"),
    ("LCID", "Lucid Group Inc", "LCID", "NASDAQ", "US", "Luxury High-Performance Electric Sedans", "Global Mega-Caps", ["lucid", "lucid motors"], False, "⚡"),
    ("JD", "JD.com Inc", "JD", "NASDAQ", "US", "Direct E-Commerce & Logistics China", "Global Mega-Caps", ["jd.com", "jd"], False, "📦"),
    ("PDD", "PDD Holdings Inc (Temu)", "PDD", "NASDAQ", "US", "Global Cross-Border E-Commerce & Pinduoduo", "Global Mega-Caps", ["temu", "pdd", "pinduoduo"], True, "🛍️"),
    ("NIO", "NIO Inc", "NIO", "NYSE", "US", "Smart Premium Electric Vehicles & Battery Swap", "Global Mega-Caps", ["nio"], False, "🚗"),
    ("LI", "Li Auto Inc", "LI", "NASDAQ", "US", "Range-Extended Electric Smart SUVs", "Global Mega-Caps", ["li auto", "li"], False, "🚗"),
    ("XPEV", "XPeng Inc", "XPEV", "NYSE", "US", "Autonomous Smart Electric Vehicles", "Global Mega-Caps", ["xpeng", "xpev"], False, "🚗"),

    # --- US BLUECHIPS, AEROSPACE & MEDICAL TECHNOLOGY ---
    ("CAT", "Caterpillar Inc", "CAT", "NYSE", "US", "Construction & Heavy Mining Equipment", "Global Mega-Caps", ["caterpillar", "cat"], True, "🚜"),
    ("DE", "Deere & Company (John Deere)", "DE", "NYSE", "US", "Agricultural, Turf & Forestry Machinery", "Global Mega-Caps", ["john deere", "deere"], True, "🚜"),
    ("GE", "GE Aerospace (General Electric)", "GE", "NYSE", "US", "Commercial & Military Aircraft Jet Engines", "Global Mega-Caps", ["ge", "general electric"], True, "✈️"),
    ("LMT", "Lockheed Martin Corporation", "LMT", "NYSE", "US", "Aerospace, Defence & F-35 Fighter Jets", "Global Mega-Caps", ["lockheed", "lockheed martin"], True, "🛡️"),
    ("RTX", "RTX Corporation (Raytheon)", "RTX", "NYSE", "US", "Defence Missiles & Pratt & Whitney Engines", "Global Mega-Caps", ["raytheon", "rtx"], True, "🚀"),
    ("UNH", "UnitedHealth Group Inc", "UNH", "NYSE", "US", "Healthcare Insurance & Optum Health", "Global Mega-Caps", ["unitedhealth", "unh"], True, "🏥"),
    ("HD", "The Home Depot Inc", "HD", "NYSE", "US", "Home Improvement Retail Megastores", "Global Mega-Caps", ["home depot", "hd"], True, "🔨"),
    ("LOW", "Lowe's Companies Inc", "LOW", "NYSE", "US", "Home Improvement & Hardware Retail", "Global Mega-Caps", ["lowes", "lowe's"], False, "🏡"),
    ("T", "AT&T Inc", "T", "NYSE", "US", "Telecommunications & 5G Wireless Network", "Global Mega-Caps", ["at&t", "att"], True, "📶"),
    ("VZ", "Verizon Communications Inc", "VZ", "NYSE", "US", "Broadband & Wireless Telecommunications", "Global Mega-Caps", ["verizon", "vz"], True, "📶"),
    ("ISRG", "Intuitive Surgical Inc", "ISRG", "NASDAQ", "US", "Robotic Da Vinci Surgical Systems", "Global Mega-Caps", ["intuitive surgical", "da vinci"], True, "🤖"),
    ("VRTX", "Vertex Pharmaceuticals", "VRTX", "NASDAQ", "US", "Cystic Fibrosis & Gene Therapies", "Global Mega-Caps", ["vertex"], False, "🧬"),

    # --- EXPANDED INDICES, COMMODITIES & CRYPTOCURRENCIES ---
    ("^NSEMDCP50", "NIFTY Midcap 50", "MIDCAP50", "NSE", "IN", "Indian Midcap 50 Benchmark Index", "Indices & Commodities", ["nifty midcap", "midcap 50", "midcap"], True, "🇮🇳"),
    ("^DJI", "Dow Jones Industrial Average", "DOWJONES", "US", "US", "US 30 Industrial Bluechips Index", "Indices & Commodities", ["dow jones", "dow", "djia"], True, "🇺🇸"),
    ("^RUT", "Russell 2000 Index", "RUSSELL2000", "US", "US", "US Small-Cap Benchmark Index", "Indices & Commodities", ["russell 2000", "russell"], False, "🇺🇸"),
    ("^FTSE", "FTSE 100 Index", "FTSE100", "LSE", "Global", "UK 100 Benchmark Index", "Indices & Commodities", ["ftse", "ftse 100"], False, "🇬🇧"),
    ("^N225", "Nikkei 225 Index", "NIKKEI225", "TSE", "Global", "Japan Tokyo Benchmark Index", "Indices & Commodities", ["nikkei", "nikkei 225"], True, "🇯🇵"),
    ("^HSI", "Hang Seng Index", "HANGSENG", "HKEX", "Global", "Hong Kong Benchmark Index", "Indices & Commodities", ["hang seng"], False, "🇭🇰"),
    ("BZ=F", "Brent Crude Oil Futures", "BRENT", "ICE", "Global", "Global Benchmark Petroleum", "Indices & Commodities", ["brent crude", "brent"], True, "🛢️"),
    ("NG=F", "Natural Gas Futures", "NATGAS", "NYMEX", "Global", "Natural Gas Energy Commodity", "Indices & Commodities", ["natural gas", "nat gas"], True, "🔥"),
    ("HG=F", "Copper Futures", "COPPER", "COMEX", "Global", "Industrial Metal Commodity", "Indices & Commodities", ["copper", "copper futures"], True, "🥉"),
    ("PL=F", "Platinum Futures", "PLATINUM", "NYMEX", "Global", "Precious Industrial Metal", "Indices & Commodities", ["platinum"], False, "💍"),
    ("ETH-USD", "Ethereum (USD)", "ETH", "Crypto", "Global", "Smart Contract Platform Cryptocurrency", "Indices & Commodities", ["ethereum", "eth"], True, "🔷"),
    ("SOL-USD", "Solana (USD)", "SOL", "Crypto", "Global", "High Performance L1 Cryptocurrency", "Indices & Commodities", ["solana", "sol"], True, "🟣"),
    ("BNB-USD", "Binance Coin (USD)", "BNB", "Crypto", "Global", "Binance Ecosystem Cryptocurrency", "Indices & Commodities", ["binance coin", "bnb"], False, "🟡"),
    ("XRP-USD", "Ripple XRP (USD)", "XRP", "Crypto", "Global", "Cross-Border Settlement Cryptocurrency", "Indices & Commodities", ["xrp", "ripple"], True, "🪙"),
    ("ADA-USD", "Cardano (USD)", "ADA", "Crypto", "Global", "Proof of Stake Cryptocurrency", "Indices & Commodities", ["cardano", "ada"], False, "🪙"),
    ("DOGE-USD", "Dogecoin (USD)", "DOGE", "Crypto", "Global", "Meme Cryptocurrency", "Indices & Commodities", ["doge", "dogecoin"], True, "🐕")
]

# Merge into master_map
for c in NEW_COMPANIES:
    sym = c[0]
    entry = {
        "symbol": c[0],
        "name": c[1],
        "ticker": c[2],
        "exchange": c[3],
        "country": c[4],
        "sector": c[5],
        "category": c[6],
        "aliases": c[7],
        "is_popular": c[8],
        "emoji": c[9]
    }
    if sym in master_map:
        # Merge aliases
        existing = master_map[sym]
        existing_aliases = set(a.lower() for a in existing.get("aliases", []))
        for a in entry["aliases"]:
            if a.lower() not in existing_aliases:
                existing.setdefault("aliases", []).append(a)
                existing_aliases.add(a.lower())
    else:
        master_map[sym] = entry

final_list = list(master_map.values())
print(f"Total compiled companies in Master Catalog: {len(final_list)}")

# Save to data/companies_master.json
with open("c:/Users/acer/Desktop/stackmarket/data/companies_master.json", "w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=2, ensure_ascii=False)

print("Saved to c:/Users/acer/Desktop/stackmarket/data/companies_master.json")
