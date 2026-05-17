"""BIST (Borsa Istanbul) index constituents.

Defines the constituent stocks for the main BIST indices:
- BIST30 (XU030):  Top 30 large-cap blue-chip stocks
- BIST50 (XU050):  Top 50 most liquid stocks (BIST30 + next 20)
- BIST100 (XU100): Top 100 most liquid stocks, broad-market benchmark

Borsa Istanbul revises index compositions periodically (typically every
3 months). The static lists below are a snapshot baseline; the
`fetch_*_dynamic` helpers attempt to fetch the current composition from
TradingView's screener and fall back to the static list on failure.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple


# ── Static constituent baselines ───────────────────────────────────────────────
# Snapshot of BIST30 (XU030). Update when Borsa Istanbul publishes a new
# index revision — typically the first business day of January / April /
# July / October.
BIST30_CONSTITUENTS: List[str] = [
    "AKBNK",   # Akbank
    "ALARK",   # Alarko Holding
    "ASELS",   # Aselsan
    "ASTOR",   # Astor Enerji
    "BIMAS",   # BIM Birlesik Magazalar
    "DOAS",    # Dogus Otomotiv
    "EKGYO",   # Emlak Konut GYO
    "ENJSA",   # Enerjisa Enerji
    "ENKAI",   # Enka Insaat
    "EREGL",   # Eregli Demir Celik
    "FROTO",   # Ford Otosan
    "GARAN",   # Garanti BBVA
    "GUBRF",   # Gubre Fabrikalari
    "HEKTS",   # Hektas
    "ISCTR",   # Is Bankasi (C)
    "KCHOL",   # Koc Holding
    "KOZAL",   # Koza Altin
    "KRDMD",   # Kardemir (D)
    "MGROS",   # Migros
    "PETKM",   # Petkim
    "PGSUS",   # Pegasus
    "SAHOL",   # Sabanci Holding
    "SASA",    # SASA Polyester
    "SISE",    # Sise Cam
    "TCELL",   # Turkcell
    "THYAO",   # Turk Hava Yollari
    "TOASO",   # Tofas Oto
    "TUPRS",   # Tupras
    "VAKBN",   # Vakifbank
    "YKBNK",   # Yapi Kredi
]

# BIST50 additions (the next ~20 stocks beyond BIST30 — most liquid mid/large caps)
_BIST50_EXTRA: List[str] = [
    "AEFES",   # Anadolu Efes
    "AGHOL",   # Anadolu Grubu Holding
    "AKSEN",   # Aksa Enerji
    "ARCLK",   # Arcelik
    "BIENY",   # Bien Yapi
    "CCOLA",   # Coca-Cola Icecek
    "CIMSA",   # Cimsa
    "CWENE",   # CW Enerji
    "DOHOL",   # Dogan Holding
    "ENERY",   # Enerya Enerji
    "EUPWR",   # Europower
    "HALKB",   # Halkbank
    "KCAER",   # Kocaer Celik
    "KONTR",   # Kontrolmatik
    "KOZAA",   # Koza Anadolu
    "ODAS",    # Odas Elektrik
    "OYAKC",   # Oyak Cimento
    "SMRTG",   # Smart Gunes Enerji
    "TABGD",   # TAB Gida
    "TAVHL",   # TAV Havalimanlari
    "TKFEN",   # Tekfen Holding
    "TTKOM",   # Turk Telekom
    "TUKAS",   # Tukas
    "ULKER",   # Ulker Biskuvi
]

# BIST100 additions (the remaining ~50 mid/small caps to reach 100)
_BIST100_EXTRA: List[str] = [
    "A1CAP",   # A1 Capital
    "AHGAZ",   # Aksa Dogalgaz
    "AKCNS",   # Akcansa
    "AKFGY",   # Akfen GYO
    "AKFYE",   # Akfen Yenilenebilir Enerji
    "AKSA",    # Aksa
    "ALBRK",   # Albaraka Turk
    "ANSGR",   # Anadolu Sigorta
    "ASUZU",   # Anadolu Isuzu
    "AYDEM",   # Aydem Enerji
    "AYGAZ",   # Aygaz
    "BERA",    # Bera Holding
    "BIOEN",   # Biotrend Cevre
    "BRSAN",   # Borusan Mannesmann
    "BRYAT",   # Borusan Yatirim
    "BUCIM",   # Bursa Cimento
    "CANTE",   # Can2 Termik
    "CLEBI",   # Celebi Hava Servisi
    "CVKMD",   # CVK Maden
    "DEVA",    # Deva Holding
    "ECILC",   # Eczacibasi Ilac
    "EGEEN",   # Ege Endustri
    "FENER",   # Fenerbahce Sportif
    "GESAN",   # Girisim Elektrik
    "GLYHO",   # Global Yatirim Holding
    "GOLTS",   # Goltas Cimento
    "GOZDE",   # Gozde Girisim Sermayesi
    "GSRAY",   # Galatasaray Sportif
    "IPEKE",   # Ipek Dogal Enerji
    "IZMDC",   # Izmir Demir Celik
    "KARSN",   # Karsan Otomotiv
    "KMPUR",   # Kimpur
    "KORDS",   # Kordsa
    "KZBGY",   # Kiziltepe GYO
    "LIDER",   # Lider Faktoring
    "LOGO",    # Logo Yazilim
    "MAVI",    # Mavi Giyim
    "MIATK",   # Mia Teknoloji
    "OBASE",   # Obase Bilgisayar
    "OTKAR",   # Otokar
    "PAPIL",   # Papilon Savunma
    "PENTA",   # Penta Teknoloji
    "PRKAB",   # Turk Prysmian Kablo
    "QUAGR",   # QUA Granite
    "REEDR",   # Reeder Teknoloji
    "SDTTR",   # SDT Uzay Savunma
    "SELEC",   # Selcuk Ecza Deposu
    "SKBNK",   # Sekerbank
    "SOKM",    # Sok Marketler
    "TATGD",   # Tat Gida
    "TKHL",    # Turkiye Kalkinma Holding
    "TKNSA",   # Teknosa
    "TMSN",    # Tumosan
    "TRGYO",   # Torunlar GYO
    "TSPOR",   # Trabzonspor
    "TTRAK",   # Turk Traktor
    "TUREX",   # Tureks Turizm
    "TURSG",   # Turkiye Sigorta
    "VESBE",   # Vestel Beyaz Esya
    "VESTL",   # Vestel
    "YATAS",   # Yatas
    "YEOTK",   # Yeo Teknoloji
    "ZOREN",   # Zorlu Enerji
]

# Deduplicated full BIST50 and BIST100 lists
def _dedupe(items: List[str]) -> List[str]:
    seen: set = set()
    out: List[str] = []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
    return out


BIST50_CONSTITUENTS: List[str] = _dedupe(BIST30_CONSTITUENTS + _BIST50_EXTRA)
BIST100_CONSTITUENTS: List[str] = _dedupe(BIST50_CONSTITUENTS + _BIST100_EXTRA)


# ── Static getters ─────────────────────────────────────────────────────────────

def get_bist30_symbols_static() -> List[str]:
    """Return BIST30 constituent symbols with BIST: prefix (static snapshot)."""
    return [f"BIST:{s}" for s in BIST30_CONSTITUENTS]


def get_bist50_symbols_static() -> List[str]:
    """Return BIST50 constituent symbols with BIST: prefix (static snapshot)."""
    return [f"BIST:{s}" for s in BIST50_CONSTITUENTS]


def get_bist100_symbols_static() -> List[str]:
    """Return BIST100 constituent symbols with BIST: prefix (static snapshot)."""
    return [f"BIST:{s}" for s in BIST100_CONSTITUENTS]


# ── Dynamic fetchers (TradingView screener) ────────────────────────────────────
# Filter on the `index` column to pull whichever stocks TradingView currently
# considers part of the index. Wrapped in try/except so failure falls back
# to the static baseline.

_TV_INDEX_CODES: Dict[str, str] = {
    "BIST30":  "BIST:XU030",
    "BIST50":  "BIST:XU050",
    "BIST100": "BIST:XU100",
}


def _fetch_index_constituents_dynamic(index_key: str) -> Optional[List[str]]:
    """Try to fetch live BIST index members via TradingView screener.

    The scanner has no server-side filter for index membership — the `index`
    column rejects filter clauses with HTTP 400. So we pull the whole Turkey
    universe (~630 stocks, single request) with the `indexes` field, then
    match client-side on the requested index `proname`.

    Returns symbols prefixed with `BIST:`, or None if the live fetch
    fails (caller should fall back to the static list).
    """
    try:
        from tradingview_screener import Query
    except Exception:
        return None

    tv_code = _TV_INDEX_CODES.get(index_key)
    if not tv_code:
        return None

    try:
        q = (
            Query()
            .set_markets("turkey")
            .select("name", "indexes")
            .limit(1000)
        )
        _, df = q.get_scanner_data()
        if df is None or df.empty:
            return None
        out: List[str] = []
        for _, row in df.iterrows():
            memberships = row.get("indexes") or []
            if not isinstance(memberships, list):
                continue
            for ix in memberships:
                if isinstance(ix, dict) and ix.get("proname") == tv_code:
                    tk = row.get("ticker")
                    if tk and isinstance(tk, str):
                        out.append(tk if ":" in tk else f"BIST:{tk}")
                    break
        return out or None
    except Exception:
        return None


def get_bist30_symbols(prefer_dynamic: bool = True) -> List[str]:
    """Return BIST30 symbols. Dynamic fetch with static fallback."""
    if prefer_dynamic:
        live = _fetch_index_constituents_dynamic("BIST30")
        if live:
            return live
    return get_bist30_symbols_static()


def get_bist50_symbols(prefer_dynamic: bool = True) -> List[str]:
    """Return BIST50 symbols. Dynamic fetch with static fallback."""
    if prefer_dynamic:
        live = _fetch_index_constituents_dynamic("BIST50")
        if live:
            return live
    return get_bist50_symbols_static()


def get_bist100_symbols(prefer_dynamic: bool = True) -> List[str]:
    """Return BIST100 symbols. Dynamic fetch with static fallback."""
    if prefer_dynamic:
        live = _fetch_index_constituents_dynamic("BIST100")
        if live:
            return live
    return get_bist100_symbols_static()


def _with_source(index_key: str, static_fn) -> Tuple[List[str], str]:
    """Return (symbols, source) where source is 'dynamic' or 'static'.

    Reports the true fetch outcome — useful for callers that surface
    constituent freshness to users.
    """
    live = _fetch_index_constituents_dynamic(index_key)
    if live:
        return live, "dynamic (TradingView screener)"
    return static_fn(), "static baseline"


def get_bist30_symbols_with_source() -> Tuple[List[str], str]:
    return _with_source("BIST30", get_bist30_symbols_static)


def get_bist50_symbols_with_source() -> Tuple[List[str], str]:
    return _with_source("BIST50", get_bist50_symbols_static)


def get_bist100_symbols_with_source() -> Tuple[List[str], str]:
    return _with_source("BIST100", get_bist100_symbols_static)


# ── Index metadata ─────────────────────────────────────────────────────────────

BIST_INDICES: Dict[str, dict] = {
    "BIST30": {
        "name": "BIST 30 Index (XU030)",
        "description": "Top 30 large-cap blue-chip stocks on Borsa Istanbul, free-float market cap weighted.",
        "tv_code": "BIST:XU030",
        "constituents_count": len(BIST30_CONSTITUENTS),
        "get_symbols": get_bist30_symbols,
        "get_symbols_static": get_bist30_symbols_static,
        "get_symbols_with_source": get_bist30_symbols_with_source,
    },
    "BIST50": {
        "name": "BIST 50 Index (XU050)",
        "description": "Top 50 most liquid Borsa Istanbul stocks — BIST30 plus the next 20 most actively traded names.",
        "tv_code": "BIST:XU050",
        "constituents_count": len(BIST50_CONSTITUENTS),
        "get_symbols": get_bist50_symbols,
        "get_symbols_static": get_bist50_symbols_static,
        "get_symbols_with_source": get_bist50_symbols_with_source,
    },
    "BIST100": {
        "name": "BIST 100 Index (XU100)",
        "description": "Broad-market benchmark — top 100 most liquid stocks on Borsa Istanbul.",
        "tv_code": "BIST:XU100",
        "constituents_count": len(BIST100_CONSTITUENTS),
        "get_symbols": get_bist100_symbols,
        "get_symbols_static": get_bist100_symbols_static,
        "get_symbols_with_source": get_bist100_symbols_with_source,
    },
}


def get_index_names() -> List[str]:
    """Return list of available BIST index names."""
    return list(BIST_INDICES.keys())


def is_bist30_stock(symbol: str) -> bool:
    """Check if a symbol is in the BIST30 static baseline."""
    clean = symbol.upper().replace("BIST:", "")
    return clean in BIST30_CONSTITUENTS


def is_bist50_stock(symbol: str) -> bool:
    """Check if a symbol is in the BIST50 static baseline."""
    clean = symbol.upper().replace("BIST:", "")
    return clean in BIST50_CONSTITUENTS


def is_bist100_stock(symbol: str) -> bool:
    """Check if a symbol is in the BIST100 static baseline."""
    clean = symbol.upper().replace("BIST:", "")
    return clean in BIST100_CONSTITUENTS
