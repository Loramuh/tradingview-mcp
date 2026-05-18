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
# Snapshot of BIST30 (XU030) as of 2026-05-18 — synced from TradingView's
# live index membership. Borsa Istanbul revises index composition quarterly
# (typically first business day of January / April / July / October), so
# re-run the sync script after each revision. The dynamic fetcher in
# `_fetch_index_constituents_dynamic` will normally supersede these lists;
# they exist as the offline fallback.
BIST30_CONSTITUENTS: List[str] = [
    "AEFES",  # Anadolu Efes Biracilik ve
    "AKBNK",  # Akbank
    "ASELS",  # Aselsan Elektronik Sanayi ve
    "ASTOR",  # Astor Enerji
    "BIMAS",  # BIM Birlesik Magazalar
    "DSTKF",  # Destek Finans Faktoring
    "EKGYO",  # Emlak Konut Gayrimenkul
    "ENKAI",  # Enka Insaat ve Sanayi
    "EREGL",  # Eregli Demir Ve Celik
    "FROTO",  # Ford Otomotiv Sanayi
    "GARAN",  # Turkiye Garanti Bankasi
    "GUBRF",  # Gubre Fabrikalari
    "ISCTR",  # Turkiye Is Bankasi
    "KCHOL",  # Koc Holding
    "KRDMD",  # Kardemir Karabuk Demir Celik
    "MGROS",  # Migros Ticaret
    "PETKM",  # Petkim Petrokimya Holding
    "PGSUS",  # Pegasus Hava Tasimaciligi
    "SAHOL",  # Haci Omer Sabanci Holding
    "SASA",   # Sasa Polyester Sanayi
    "SISE",   # Turkiye Sise ve Cam
    "TAVHL",  # TAV Havalimanlari Holding
    "TCELL",  # Turkcell Iletisim Hizmetleri
    "THYAO",  # Turk Hava Yollari
    "TOASO",  # Tofas Turk Otomobil Fabrikasi
    "TRALT",  # Turk Altin Isletmeleri
    "TTKOM",  # Turk Telekomunikasyon
    "TUPRS",  # Turkiye Petrol Rafinerileri
    "VAKBN",  # Turkiye Vakiflar Bankasi
    "YKBNK",  # Yapi ve Kredi Bankasi
]

# BIST50 additions (the 20 stocks beyond BIST30 — most liquid mid/large caps)
# Snapshot as of 2026-05-18.
_BIST50_EXTRA: List[str] = [
    "ALARK",  # Alarko Holding
    "ARCLK",  # Arcelik
    "BRSAN",  # Borusan Birlesik Boru Fabrikalari
    "BTCIM",  # Baticim Bati Anadolu Cimento
    "CANTE",  # Can2 Termik
    "CCOLA",  # Coca-Cola Icecek
    "CIMSA",  # Cimsa Cimento Sanayi ve
    "DOAS",   # Dogus Otomotiv Servis ve
    "HALKB",  # Turkiye Halk Bankasi
    "HEKTS",  # Hektas Ticaret
    "KONTR",  # Kontrolmatik Teknoloji Enerji
    "KUYAS",  # Kuyas Yatirim
    "MAVI",   # Mavi Giyim Sanayi ve Ticaret
    "MIATK",  # MIA Teknoloji
    "OYAKC",  # Oyak Cimento Fabrikalari
    "PASEU",  # Pasifik Eurasia Lojistik dis
    "TRMET",  # TR Anadolu Metal Madencilik
    "TSKB",   # Turkiye Sinai Kalkinma Bankasi
    "TURSG",  # Turkiye Sigorta
    "ULKER",  # Ulker Biskuvi Sanayi
]

# BIST100 additions (the 50 stocks beyond BIST50 to reach 100)
# Snapshot as of 2026-05-18.
_BIST100_EXTRA: List[str] = [
    "AGHOL",  # AG Anadolu Grubu Holding
    "AKSA",   # Aksa Akrilik Kimya Sanayii
    "AKSEN",  # Aksa Enerji Uretim
    "ALTNY",  # Altinay Savunma Teknolojileri
    "ANSGR",  # Anadolu Anonim Turk Sigorta
    "BALSU",  # Balsu Gida Sanayi ve Ticaret
    "BRYAT",  # Borusan Yatirim ve Pazarlama
    "BSOKE",  # Batisoke Soke Cimento Sanayii
    "CVKMD",  # CVK Maden Isletmeleri Sanayi
    "CWENE",  # CW Enerji Muhendislik Ticaret
    "DAPGM",  # DAP Gayrimenkul Gelistirme
    "DOHOL",  # Dogan Sirketler Grubu Holding
    "ECILC",  # EIS Eczacibasi Ilac, Sinai ve
    "EFOR",   # Efor Yatirim Sanayi Ticaret
    "ENERY",  # Enerya Enerji
    "ENJSA",  # Enerjisa Enerji
    "EUPWR",  # Europower Enerji ve Otomasyon
    "EUREN",  # Europen Endustri Insaat
    "FENER",  # Fenerbahce Futbol
    "GENIL",  # Gen Ilac ve Saglik Urunleri
    "GESAN",  # Girisim Elektrik Sanayi
    "GLRMK",  # Gulermak Agir Sanayi Insaat
    "GRSEL",  # Gur-Sel Turizm Tasimacilik Ve
    "GRTHO",  # Grainturk Holding
    "GSRAY",  # Galatasaray Sportif Sinai
    "ISMEN",  # Is Yatirim Menkul Degerler
    "IZENR",  # Izdemir Enerji Elektrik Uretim
    "KLRHO",  # Kiler Holding
    "KTLEV",  # Katilimevim Tasarruf Finansman
    "MAGEN",  # Margun Enerji Uretim Sanayi
    "MPARK",  # MLP Saglik Hizmetleri
    "OBAMS",  # Oba Makarnacilik Sanayi Ve
    "ODAS",   # Odas Elektrik Uretim Sanayi
    "OTKAR",  # Otokar Otomotiv ve Savunma
    "PAHOL",  # Pasifik Holding
    "PATEK",  # Pasifik Teknoloji
    "PSGYO",  # Pasifik Gayrimenkul Yatirim
    "QUAGR",  # Qua Granite Hayal Yapi ve
    "RALYH",  # Ral Yatirim Holding
    "REEDR",  # Reeder Teknoloji Sanayi ve
    "SARKY",  # Sarkuysan Elektrolitik Bakir
    "SKBNK",  # Sekerbank
    "SOKM",   # Sok Marketler Ticaret
    "TABGD",  # TAB Gida Sanayi ve Ticaret
    "TKFEN",  # Tekfen Holding
    "TRENJ",  # TR Dogal Enerji Kaynaklari
    "TUKAS",  # Tukas Gida Sanayi ve Ticaret
    "TUREX",  # Tureks Turizm Tasimacilik
    "VESTL",  # Vestel Elektronik Sanayi ve
    "ZOREN",  # Zorlu Enerji Elektrik Uretim
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
