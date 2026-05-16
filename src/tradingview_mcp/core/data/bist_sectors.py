"""BIST (Borsa Istanbul) sector classification for stock symbols.

Sector metadata (market cap weight, etc.) is an approximate static snapshot of
relative BIST sector weights — useful for relative ranking, not for exact
portfolio attribution. Update if precision matters for live trading.
"""
from __future__ import annotations
from typing import Any, Dict, List, Set


# Sector metadata: approximate market cap weight (%) within the BIST 100 universe.
# Used by the sector rotation scanner for weighted aggregation.
BIST_SECTOR_META: Dict[str, Dict[str, Any]] = {
    "banks": {
        "market_cap_weight": 25.00,
        "sector_index": "XBANK",
    },
    "holding": {
        "market_cap_weight": 14.50,
        "sector_index": "XHOLD",
    },
    "transportation_and_logistics": {
        "market_cap_weight": 10.00,
        "sector_index": "XULAS",
    },
    "chemicals_and_petrochemicals": {
        "market_cap_weight": 9.50,
        "sector_index": "XKMYA",
    },
    "mining_and_metals": {
        "market_cap_weight": 7.00,
        "sector_index": "XMADN",
    },
    "electricity_and_energy": {
        "market_cap_weight": 6.50,
        "sector_index": "XELKT",
    },
    "food_and_beverages": {
        "market_cap_weight": 5.50,
        "sector_index": "XGIDA",
    },
    "automotive": {
        "market_cap_weight": 5.00,
        "sector_index": "XOTOM",
    },
    "industrial_goods": {
        "market_cap_weight": 4.00,
        "sector_index": "XUSIN",
    },
    "building_materials_and_cement": {
        "market_cap_weight": 3.50,
        "sector_index": "XTAST",
    },
    "telecommunications": {
        "market_cap_weight": 3.00,
        "sector_index": "XILTM",
    },
    "electronics_and_appliances": {
        "market_cap_weight": 3.00,
        "sector_index": "XUSIN",
    },
    "defense": {
        "market_cap_weight": 2.50,
        "sector_index": "XSAVU",
    },
    "construction": {
        "market_cap_weight": 2.00,
        "sector_index": "XINSA",
    },
    "insurance": {
        "market_cap_weight": 2.00,
        "sector_index": "XSGRT",
    },
    "real_estate_reits": {
        "market_cap_weight": 1.80,
        "sector_index": "XGMYO",
    },
    "technology_software": {
        "market_cap_weight": 1.80,
        "sector_index": "XBLSM",
    },
    "healthcare_and_pharma": {
        "market_cap_weight": 1.50,
        "sector_index": "XKBUL",
    },
    "textile_and_apparel": {
        "market_cap_weight": 1.20,
        "sector_index": "XTEKS",
    },
    "retail": {
        "market_cap_weight": 1.00,
        "sector_index": "XTCRT",
    },
    "paper_and_packaging": {
        "market_cap_weight": 0.50,
        "sector_index": "XKAGT",
    },
    "sports": {
        "market_cap_weight": 0.40,
        "sector_index": "XSPOR",
    },
}


# Sector mapping: sector name -> set of ticker symbols (without BIST: prefix)
BIST_SECTORS: Dict[str, Set[str]] = {
    "banks": {
        "GARAN", "AKBNK", "ISCTR", "YKBNK", "VAKBN", "HALKB", "SKBNK",
    },
    "holding": {
        "KCHOL", "SAHOL", "AGHOL", "ALARK", "BRYAT", "GLYHO", "NTHOL",
        "DOHOL", "BERA", "TKFEN",
    },
    "insurance": {
        "AGESA", "ANSGR", "TURSG", "RAYSG",
    },
    "food_and_beverages": {
        "ULKER", "BIMAS", "MGROS", "SOKM", "AEFES", "CCOLA", "BANVT",
    },
    "chemicals_and_petrochemicals": {
        "PETKM", "TUPRS", "SASA", "HEKTS", "GUBRF", "EGGUB",
    },
    "textile_and_apparel": {
        "MAVI", "KORDS", "YATAS",
    },
    "transportation_and_logistics": {
        "THYAO", "PGSUS", "TAVHL",
    },
    "telecommunications": {
        "TCELL", "TTKOM", "NETAS",
    },
    "technology_software": {
        "LOGO", "KAREL", "MIATK",
    },
    "electricity_and_energy": {
        "ENJSA", "AKSEN", "ODAS", "ZOREN", "ASTOR", "SMRTG", "YEOTK",
        "GESAN", "KONTR", "ORGE",
    },
    "real_estate_reits": {
        "EKGYO", "YGGYO", "ZRGYO",
    },
    "mining_and_metals": {
        "KOZAL", "KOZAA", "EREGL", "KRDMD", "PRKME", "PRKAB", "PARSN",
        "CEMTS", "TMSN",
    },
    "industrial_goods": {
        "KLMSN", "BFREN", "BLCYT", "BRSAN", "EGEEN",
    },
    "automotive": {
        "FROTO", "TOASO", "KARSN", "DOAS", "TTRAK", "OTKAR",
    },
    "healthcare_and_pharma": {
        "MPARK", "SELEC", "DEVA", "ECILC",
    },
    "building_materials_and_cement": {
        "SISE", "CIMSA", "OYAKC", "EGSER", "INTEM",
    },
    "electronics_and_appliances": {
        "ARCLK", "VESTL", "VESBE",
    },
    "defense": {
        "ASELS", "SDTTR",
    },
    "construction": {
        "ENKAI", "ANELE",
    },
    "retail": {
        "TKNSA",
    },
    "paper_and_packaging": {
        "KARTN",
    },
    "sports": {
        "FENER",
    },
}


# Reverse lookup: symbol -> sector
_SYMBOL_TO_SECTOR: Dict[str, str] = {}
for _sector, _symbols in BIST_SECTORS.items():
    for _sym in _symbols:
        if _sym not in _SYMBOL_TO_SECTOR:
            _SYMBOL_TO_SECTOR[_sym] = _sector


def get_currency(symbol: str) -> str:
    """All BIST stocks trade in Turkish Lira."""
    return "TRY"


def get_sector(symbol: str) -> str:
    """Return the sector for a BIST symbol, or 'other' if not classified."""
    clean = symbol.upper().replace("BIST:", "")
    return _SYMBOL_TO_SECTOR.get(clean, "other")


def get_symbols_by_sector(sector: str) -> List[str]:
    """Return list of BIST symbols for a given sector."""
    key = sector.lower().replace(" ", "_")
    symbols = BIST_SECTORS.get(key, set())
    return [f"BIST:{s}" for s in sorted(symbols)]


def get_all_sectors() -> List[str]:
    """Return list of all available BIST sectors."""
    return sorted(BIST_SECTORS.keys())


def get_sector_meta(sector: str) -> Dict[str, Any]:
    """Return metadata (market cap weight, sector index) for a sector."""
    key = sector.lower().replace(" ", "_")
    return BIST_SECTOR_META.get(key, {})


def get_sectors_by_weight(descending: bool = True) -> List[Dict[str, Any]]:
    """Return all sectors sorted by approximate market cap weight."""
    result = []
    for key, meta in BIST_SECTOR_META.items():
        result.append({"sector": key, **meta})
    result.sort(key=lambda x: x["market_cap_weight"], reverse=descending)
    return result


# Display-friendly sector names
SECTOR_DISPLAY_NAMES: Dict[str, str] = {
    "banks": "Banks (XBANK)",
    "holding": "Holding Companies (XHOLD)",
    "insurance": "Insurance (XSGRT)",
    "food_and_beverages": "Food & Beverages (XGIDA)",
    "chemicals_and_petrochemicals": "Chemicals & Petrochemicals (XKMYA)",
    "textile_and_apparel": "Textile & Apparel (XTEKS)",
    "transportation_and_logistics": "Transportation & Logistics (XULAS)",
    "telecommunications": "Telecommunications (XILTM)",
    "technology_software": "Technology & Software (XBLSM)",
    "electricity_and_energy": "Electricity & Energy (XELKT)",
    "real_estate_reits": "Real Estate & REITs (XGMYO)",
    "mining_and_metals": "Mining & Metals (XMADN)",
    "industrial_goods": "Industrial Goods (XUSIN)",
    "automotive": "Automotive (XOTOM)",
    "healthcare_and_pharma": "Healthcare & Pharmaceuticals",
    "construction": "Construction (XINSA)",
    "building_materials_and_cement": "Building Materials & Cement (XTAST)",
    "electronics_and_appliances": "Electronics & Home Appliances",
    "defense": "Defense (XSAVU)",
    "retail": "Retail (XTCRT)",
    "paper_and_packaging": "Paper & Packaging (XKAGT)",
    "sports": "Sports (XSPOR)",
}
