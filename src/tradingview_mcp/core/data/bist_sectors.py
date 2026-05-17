"""BIST (Borsa Istanbul) sector classification for stock symbols.

Sectors map roughly to Borsa Istanbul's sector indices (BANK, HOLD, GIDA,
SINAI, METAL, etc.). The classification covers BIST100 constituents plus
common mid-caps; uncategorised symbols return 'other'.

All BIST equities are TRY-denominated, so `get_currency` always returns 'TRY'.
"""
from __future__ import annotations
from typing import Any, Dict, List, Set


# Sector metadata: approximate free-float market cap weight (%) inside BIST100.
# These are working estimates used for the weighted market view; refine when
# you have current sector-weighting data from Borsa Istanbul.
BIST_SECTOR_META: Dict[str, Dict[str, Any]] = {
    "banking":              {"market_cap_weight": 22.5},
    "holding":              {"market_cap_weight": 14.0},
    "industrials":          {"market_cap_weight": 10.0},
    "petrochemicals":       {"market_cap_weight": 9.0},
    "iron_steel_metals":    {"market_cap_weight": 6.5},
    "automotive":           {"market_cap_weight": 6.0},
    "energy_and_utilities": {"market_cap_weight": 5.5},
    "defense_aerospace":    {"market_cap_weight": 5.0},
    "telecom":              {"market_cap_weight": 4.5},
    "retail_and_food":      {"market_cap_weight": 4.0},
    "reit":                 {"market_cap_weight": 3.5},
    "transportation":       {"market_cap_weight": 3.0},
    "cement_glass":         {"market_cap_weight": 2.5},
    "technology":           {"market_cap_weight": 1.8},
    "mining":               {"market_cap_weight": 1.5},
    "insurance_and_finserv":{"market_cap_weight": 1.8},
    "chemicals_fertilizers":{"market_cap_weight": 1.2},
    "construction":         {"market_cap_weight": 1.0},
    "sports_and_media":     {"market_cap_weight": 0.6},
    "textiles_apparel":     {"market_cap_weight": 0.4},
    "other":                {"market_cap_weight": 0.3},
}


# Sector mapping: sector key -> set of ticker symbols (without BIST: prefix).
# Covers BIST30/50/100 constituents plus common mid-caps.
BIST_SECTORS: Dict[str, Set[str]] = {

    "banking": {
        "AKBNK",  # Akbank
        "GARAN",  # Garanti BBVA
        "ISCTR",  # Is Bankasi (C)
        "YKBNK",  # Yapi Kredi
        "VAKBN",  # Vakifbank
        "HALKB",  # Halkbank
        "ALBRK",  # Albaraka Turk
        "ICBCT",  # ICBC Turkey
        "QNBFB",  # QNB Finansbank
        "SKBNK",  # Sekerbank
        "TSKB",   # TSKB
        "DENIZ",  # Denizbank
    },

    "holding": {
        "KCHOL",  # Koc Holding
        "SAHOL",  # Sabanci Holding
        "AGHOL",  # Anadolu Grubu Holding
        "ALARK",  # Alarko Holding
        "DOHOL",  # Dogan Holding
        "BERA",   # Bera Holding
        "GLYHO",  # Global Yatirim Holding
        "TKHL",   # Turkiye Kalkinma Holding
        "ENKAI",  # Enka Insaat
        "EUHOL",  # Euro Holding
        "GSDHO",  # GSD Holding
        "IHLAS",  # Ihlas Holding
        "NTHOL",  # Net Holding
        "OSTIM",  # Ostim Endustriyel Yatirimlar
        "BRYAT",  # Borusan Yatirim
        "AVHOL",  # Avrasya Holding
    },

    "industrials": {
        "ASTOR",  # Astor Enerji (industrial machinery)
        "TKFEN",  # Tekfen Holding (heavy industry)
        "GESAN",  # Girisim Elektrik
        "KCAER",  # Kocaer Celik (also metals)
        "KONTR",  # Kontrolmatik
        "SMRTG",  # Smart Gunes
        "BRSAN",  # Borusan Mannesmann
        "PRKAB",  # Turk Prysmian Kablo
        "OTKAR",  # Otokar (defense + industrial)
        "TMSN",   # Tumosan
        "TUREX",  # Tureks Turizm
        "AKSA",   # Aksa (specialty industrials)
        "EGEEN",  # Ege Endustri
        "ENJSA",  # Enerjisa (utility + industrials)
        "ESCAR",  # Escar
        "ALKA",   # Alkim Kagit
        "ARCLK",  # Arcelik (white goods)
        "VESTL",  # Vestel (electronics)
        "VESBE",  # Vestel Beyaz Esya
    },

    "petrochemicals": {
        "TUPRS",  # Tupras
        "PETKM",  # Petkim
        "SASA",   # SASA Polyester
        "AKSA",   # Aksa
        "DEVA",   # Deva Holding (pharma-chem)
        "ALKIM",  # Alkim
        "RTALB",  # RT Alarko Carrier
    },

    "iron_steel_metals": {
        "EREGL",  # Eregli Demir Celik
        "KRDMD",  # Kardemir (D)
        "KRDMA",  # Kardemir (A)
        "KRDMB",  # Kardemir (B)
        "IZMDC",  # Izmir Demir Celik
        "CEMTS",  # Cemtas
        "CELHA",  # Celik Halat
        "KCAER",  # Kocaer Celik
        "BAKAB",  # Bak Ambalaj
        "BRSAN",  # Borusan Mannesmann
        "DMSAS",  # Demisas Dokum
        "CUSAN",  # Cuhadaroglu Metal
        "EGEEN",  # Ege Endustri (also industrial)
        "GUBRF",  # Gubre Fabrikalari (chemicals)
    },

    "automotive": {
        "FROTO",  # Ford Otosan
        "TOASO",  # Tofas
        "DOAS",   # Dogus Otomotiv
        "ASUZU",  # Anadolu Isuzu
        "OTKAR",  # Otokar
        "KARSN",  # Karsan
        "TTRAK",  # Turk Traktor
        "DITAS",  # Ditas Dogan
        "FMIZP",  # F-M Izmit Piston
        "PARSN",  # Parsan
        "JANTS",  # Jantsa
        "GOODY",  # Goodyear
        "BFREN",  # Bosch Fren
        "EGEEN",  # Ege Endustri (auto + industrial)
    },

    "energy_and_utilities": {
        "ENJSA",  # Enerjisa
        "AKSEN",  # Aksa Enerji
        "AYDEM",  # Aydem Enerji
        "AKFYE",  # Akfen Yenilenebilir
        "ZOREN",  # Zorlu Enerji
        "ODAS",   # Odas Elektrik
        "CWENE",  # CW Enerji
        "EUPWR",  # Europower
        "ENERY",  # Enerya Enerji
        "BIOEN",  # Biotrend Cevre
        "AHGAZ",  # Aksa Dogalgaz
        "AYGAZ",  # Aygaz
        "GWIND",  # Galata Wind
        "KARYE",  # Kartonsan Yenilenebilir Enerji
        "MAGEN",  # Margun Enerji
        "PAMEL",  # Pamel Yenilenebilir Elektrik
        "PRZMA",  # Prizma Press
        "CANTE",  # Can2 Termik
        "ESEN",   # Esen Sistem
        "IPEKE",  # Ipek Dogal Enerji
        "BASGZ",  # Baskent Dogalgaz
    },

    "defense_aerospace": {
        "ASELS",  # Aselsan
        "OTKAR",  # Otokar
        "TMSN",   # Tumosan
        "PAPIL",  # Papilon Savunma
        "SDTTR",  # SDT Uzay Savunma
        "KATMR",  # Katmerciler
        "REEDR",  # Reeder Teknoloji
        "PENTA",  # Penta Teknoloji
    },

    "telecom": {
        "TCELL",  # Turkcell
        "TTKOM",  # Turk Telekom
    },

    "retail_and_food": {
        "BIMAS",  # BIM
        "MGROS",  # Migros
        "SOKM",   # Sok Marketler
        "ULKER",  # Ulker
        "CCOLA",  # Coca-Cola Icecek
        "AEFES",  # Anadolu Efes
        "TABGD",  # TAB Gida
        "TUKAS",  # Tukas
        "TATGD",  # Tat Gida
        "PNSUT",  # Pinar Sut
        "PINSU",  # Pinar Su
        "PETUN",  # Pinar Et
        "BANVT",  # Banvit
        "KNFRT",  # Konfrut Gida
        "DARDL",  # Dardanel
        "EKSUN",  # Eksun Gida
        "FRIGO",  # Frigo Pak
        "MERKO",  # Merko Gida
        "OYLUM",  # Oylum
        "PEKGY",  # Peker GYO (food retail)
        "VANGD",  # Vanet Gida
        "TKNSA",  # Teknosa
        "MAVI",   # Mavi
        "SELEC",  # Selcuk Ecza Deposu
        "BIZIM",  # Bizim Toptan
        "CRFSA",  # Carrefoursa
        "INTEM",  # Intema
    },

    "reit": {
        "EKGYO",  # Emlak Konut
        "AKFGY",  # Akfen GYO
        "AKSGY",  # Aksa GYO
        "AKMGY",  # Akmerkez GYO
        "ALGYO",  # Alarko GYO
        "ASGYO",  # Aktif GYO
        "ATAGY",  # Ata GYO
        "AGYO",   # Atakule GYO
        "AVGYO",  # Avrasya GYO
        "DGGYO",  # Dogus GYO
        "DZGYO",  # Deniz GYO
        "EYGYO",  # Eyg GYO
        "HLGYO",  # Halk GYO
        "IDGYO",  # Idealist GYO
        "ISGYO",  # Is GYO
        "KRGYO",  # Kor Gayrimenkul
        "KZBGY",  # Kiziltepe GYO
        "MRGYO",  # Martiz GYO
        "MSGYO",  # Mistral GYO
        "NUGYO",  # Nurol GYO
        "OZKGY",  # Ozak GYO
        "OZGYO",  # Ozderici GYO
        "PAGYO",  # Panora GYO
        "PEGYO",  # PERA GYO
        "PEKGY",  # Peker GYO
        "RYGYO",  # Reysas GYO
        "SNGYO",  # Sinpas GYO
        "TRGYO",  # Torunlar GYO
        "VKGYO",  # Vakif GYO
        "YGGYO",  # YG GYO
        "YGYO",   # Yaprak GYO
        "YKGYO",  # Yapi Kredi Koray GYO
        "PSGYO",  # Pera GYO
        "AVGYO",  # Avrasya GYO
        "DZGYO",  # Deniz GYO
    },

    "transportation": {
        "THYAO",  # THY
        "PGSUS",  # Pegasus
        "TAVHL",  # TAV Havalimanlari
        "CLEBI",  # Celebi
        "GSDDE",  # GSD Denizcilik
        "BEYAZ",  # Beyaz Filo
        "REYSA",  # Reysas Tasimacilik
        "TUREX",  # Tureks Turizm
    },

    "cement_glass": {
        "CIMSA",  # Cimsa
        "AKCNS",  # Akcansa
        "OYAKC",  # Oyak Cimento
        "BUCIM",  # Bursa Cimento
        "GOLTS",  # Goltas Cimento
        "BTCIM",  # Batisoke Cimento
        "BSOKE",  # Batisoke Cimento (alt)
        "CIMEN",  # Cimentas
        "CMBTN",  # Cimbeton
        "CMENT",  # Cimentas
        "BASCM",  # Baspinar Cimento
        "KONYA",  # Konya Cimento
        "KUTPO",  # Kutahya Porselen
        "MRDIN",  # Mardin Cimento
        "NUHCM",  # Nuh Cimento
        "USAK",   # Usak Seramik
        "EGSER",  # Ege Seramik
        "SISE",   # Sise Cam (also flagship)
        "ANACM",  # Anadolu Cam
        "DENCM",  # Denizli Cam
        "SODA",   # Soda Sanayii
        "TRKCM",  # Trakya Cam
    },

    "technology": {
        "LOGO",   # Logo Yazilim
        "MIATK",  # Mia Teknoloji
        "OBASE",  # Obase
        "NETAS",  # Netas
        "ARDYZ",  # Ard Yazilim
        "ARENA",  # Arena Bilgisayar
        "DESPC",  # Despec Bilgisayar
        "DGATE",  # Datagate
        "EDATA",  # E-Data Teknoloji
        "ESCOM",  # Escort Teknoloji
        "FONET",  # Fonet Bilgi Teknolojileri
        "FORTE",  # Forte Bilgi Iletisim
        "HTTBT",  # Hitit Bilgisayar
        "INDES",  # Indeks Bilgisayar
        "INVEO",  # Inveo Yatirim
        "KAREL",  # Karel
        "KFEIN",  # Kafein Yazilim
        "PENTA",  # Penta Teknoloji
        "REEDR",  # Reeder
        "SMART",  # Smart Solar
        "VBTYZ",  # VBT Yazilim
        "YEOTK",  # Yeo Teknoloji
    },

    "mining": {
        "KOZAL",  # Koza Altin
        "KOZAA",  # Koza Anadolu
        "CVKMD",  # CVK Maden
        "IPEKE",  # Ipek Dogal Enerji (mining-linked)
        "PRKME",  # Park Elek Madencilik
        "AKENR",  # Akenerji (mining-linked legacy)
        "DGNMO",  # Dogan Burda Magazinler (placeholder; if any mining sub)
        "QUAGR",  # QUA Granite
        "ALMAD",  # Altinyag
    },

    "insurance_and_finserv": {
        "ANSGR",  # Anadolu Sigorta
        "AKGRT",  # Aksigorta
        "ANHYT",  # Anadolu Hayat
        "TURSG",  # Turkiye Sigorta
        "RAYSG",  # Ray Sigorta
        "AGESA",  # Avivasa Emeklilik
        "A1CAP",  # A1 Capital (non-bank financial)
        "GOZDE",  # Gozde Girisim Sermayesi (PE/VC)
        "LIDER",  # Lider Faktoring
        "INVEO",  # Inveo Yatirim
        "GLBMD",  # Global Menkul Degerler
        "GEDIK",  # Gedik Yatirim
        "HEDEF",  # Hedef Holding (financial)
        "ATLC",   # AT Lease
    },

    "chemicals_fertilizers": {
        "GUBRF",  # Gubre Fabrikalari
        "HEKTS",  # Hektas
        "BAGFS",  # Bagfas
        "RTALB",  # RT Alarko Carrier
        "AKSA",   # Aksa (also industrials)
        "BRISA",  # Brisa
        "DYOBY",  # DYO Boya
        "MRSHL",  # Marshall Boya
        "POLTK",  # Politeknik Metal
        "SODA",   # Soda Sanayii
        "ALKIM",  # Alkim Kimya
        "KMPUR",  # Kimpur
        "ECILC",  # Eczacibasi Ilac (pharma/chemicals)
        "DEVA",   # Deva Holding (pharma)
    },

    "construction": {
        "ENKAI",  # Enka (overlap with holding)
        "TKFEN",  # Tekfen (overlap with industrials)
        "BIENY",  # Bien Yapi
        "CUSAN",  # Cuhadaroglu
        "EDIP",   # Edip Gayrimenkul
        "ORGE",   # Orge Elektrik Taahhut
        "TURGG",  # Turk Tuborg
        "YYAPI",  # Yesil Yapi
        "DAPGM",  # Dap Gayrimenkul
        "GMTAS",  # Gimat Magazacilik
    },

    "sports_and_media": {
        "FENER",  # Fenerbahce
        "GSRAY",  # Galatasaray
        "BJKAS",  # Besiktas
        "TSPOR",  # Trabzonspor
        "DOBUR",  # Dogan Burda (media)
        "DOHOL",  # Dogan Holding (media stake)
        "HURGZ",  # Hurriyet Gazetecilik
        "IHGZT",  # Ihlas Gazetecilik
        "IHYAY",  # Ihlas Yayin
        "MMCAS",  # Marmaris Marina
    },

    "textiles_apparel": {
        "MAVI",   # Mavi Giyim
        "BLCYT",  # Bilici Yatirim
        "BOSSA",  # Bossa
        "BLUE",   # Blue Holding
        "DESA",   # Desa Deri
        "DAGI",   # Dagi Yatirim
        "DERIM",  # Derimod
        "KORDS",  # Kordsa (technical textiles)
        "MNDRS",  # Menderes Tekstil
        "RODRG",  # Rodrigo Tekstil
        "ROYAL",  # Royal Hali
        "SUWEN",  # Suwen
        "YATAS",  # Yatas (home textiles)
        "YUNSA",  # Yunsa
        "SNKRN",  # Sankron Tekstil
    },
}


def get_currency(symbol: str) -> str:
    """Return currency for a BIST symbol — always 'TRY'."""
    return "TRY"


# Reverse lookup: symbol -> sector (first match wins on overlaps)
_SYMBOL_TO_SECTOR: Dict[str, str] = {}
for _sector, _symbols in BIST_SECTORS.items():
    for _sym in _symbols:
        if _sym not in _SYMBOL_TO_SECTOR:
            _SYMBOL_TO_SECTOR[_sym] = _sector


def get_sector(symbol: str) -> str:
    """Return the sector for a BIST symbol, or 'other' if not classified."""
    clean = symbol.upper().replace("BIST:", "")
    return _SYMBOL_TO_SECTOR.get(clean, "other")


def get_symbols_by_sector(sector: str) -> List[str]:
    """Return list of BIST symbols (with BIST: prefix) for a given sector."""
    key = sector.lower().replace(" ", "_")
    symbols = BIST_SECTORS.get(key, set())
    return [f"BIST:{s}" for s in sorted(symbols)]


def get_all_sectors() -> List[str]:
    """Return list of all available BIST sectors."""
    return sorted(BIST_SECTORS.keys())


def get_sector_meta(sector: str) -> Dict[str, Any]:
    """Return metadata (market cap weight) for a sector."""
    key = sector.lower().replace(" ", "_")
    return BIST_SECTOR_META.get(key, {})


def get_sectors_by_weight(descending: bool = True) -> List[Dict[str, Any]]:
    """Return all sectors sorted by market cap weight."""
    result = []
    for key, meta in BIST_SECTOR_META.items():
        result.append({"sector": key, **meta})
    result.sort(key=lambda x: x["market_cap_weight"], reverse=descending)
    return result


# Display-friendly sector names
SECTOR_DISPLAY_NAMES: Dict[str, str] = {
    "banking":              "Banking",
    "holding":              "Holdings",
    "industrials":          "Industrial Goods & Services",
    "petrochemicals":       "Petrochemicals & Refining",
    "iron_steel_metals":    "Iron, Steel & Metals",
    "automotive":           "Automotive",
    "energy_and_utilities": "Energy & Utilities",
    "defense_aerospace":    "Defense & Aerospace",
    "telecom":              "Telecommunications",
    "retail_and_food":      "Retail, Food & Beverages",
    "reit":                 "Real Estate Investment Trusts (GYO)",
    "transportation":       "Transportation & Airlines",
    "cement_glass":         "Cement & Glass",
    "technology":           "Information Technology",
    "mining":               "Mining & Metals",
    "insurance_and_finserv":"Insurance & Non-Bank Financial Services",
    "chemicals_fertilizers":"Chemicals & Fertilizers",
    "construction":         "Construction & Engineering",
    "sports_and_media":     "Sports & Media",
    "textiles_apparel":     "Textiles & Apparel",
    "other":                "Other",
}
