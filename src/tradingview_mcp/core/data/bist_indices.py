"""BIST (Borsa Istanbul) index constituents.

Defines the constituent stocks for the main BIST indices:
- BIST30 (XU030):  Top 30 blue-chip stocks by free-float market cap
- BIST50 (XU050):  Top 50 stocks (BIST30 + next 20 most liquid)
- BIST100 (XU100): Headline index — top 100 stocks by liquidity & market cap
- BIST_KATILIM (XK100): Participation index — Islamic finance-compliant stocks
                        (no interest-based banks, alcohol, gambling, conventional insurance)

Index composition is reviewed quarterly by Borsa Istanbul; this file is a static
snapshot. Verify against the latest BIST review if precision matters for live trading.
All tickers below are confirmed present in `coinlist/bist.txt`.
"""
from __future__ import annotations
from typing import Dict, List


# BIST 30 — top 30 blue-chips, weighted by free-float market cap
BIST30_CONSTITUENTS: List[str] = [
    "THYAO",  # Türk Hava Yolları (Turkish Airlines)
    "GARAN",  # Garanti BBVA
    "AKBNK",  # Akbank
    "ISCTR",  # Türkiye İş Bankası (C)
    "YKBNK",  # Yapı Kredi Bankası
    "VAKBN",  # Vakıfbank
    "HALKB",  # Türkiye Halk Bankası
    "KCHOL",  # Koç Holding
    "SAHOL",  # Hacı Ömer Sabancı Holding
    "EREGL",  # Ereğli Demir ve Çelik
    "KOZAL",  # Koza Altın İşletmeleri
    "FROTO",  # Ford Otosan
    "TOASO",  # Tofaş Türk Otomobil
    "BIMAS",  # BİM Birleşik Mağazalar
    "MGROS",  # Migros Ticaret
    "ASELS",  # Aselsan Elektronik
    "PETKM",  # Petkim Petrokimya
    "TUPRS",  # Tüpraş - Türkiye Petrol Rafinerileri
    "SISE",   # Türkiye Şişe ve Cam Fabrikaları
    "ARCLK",  # Arçelik
    "SASA",   # Sasa Polyester Sanayi
    "AEFES",  # Anadolu Efes Biracılık
    "CCOLA",  # Coca-Cola İçecek
    "PGSUS",  # Pegasus Hava Taşımacılığı
    "TAVHL",  # TAV Havalimanları Holding
    "ENKAI",  # Enka İnşaat ve Sanayi
    "HEKTS",  # Hektaş Ticaret
    "TCELL",  # Turkcell İletişim Hizmetleri
    "TTKOM",  # Türk Telekomünikasyon
    "ULKER",  # Ülker Bisküvi Sanayi
]


# BIST 50 — BIST30 plus next 20 most liquid
BIST50_EXTRA_CONSTITUENTS: List[str] = [
    "SOKM",   # Şok Marketler
    "KORDS",  # Kordsa Teknik Tekstil
    "OYAKC",  # OYAK Çimento
    "KARSN",  # Karsan Otomotiv
    "DOAS",   # Doğuş Otomotiv
    "AGESA",  # AgeSA Hayat ve Emeklilik
    "ENJSA",  # Enerjisa Enerji
    "SDTTR",  # SDT Uzay ve Savunma
    "KOZAA",  # Koza Anadolu Metal Madencilik
    "KRDMD",  # Kardemir Karabük Demir Çelik (D)
    "CIMSA",  # Çimsa Çimento
    "TKFEN",  # Tekfen Holding
    "TKNSA",  # Teknosa İç ve Dış Ticaret
    "VESTL",  # Vestel Elektronik
    "MAVI",   # Mavi Giyim Sanayi
    "ASTOR",  # Astor Enerji
    "SMRTG",  # Smart Güneş Teknolojileri
    "YEOTK",  # Yeo Teknoloji Enerji
    "ODAS",   # Odaş Elektrik Üretim
    "TURSG",  # Türkiye Sigorta
]


# BIST 100 — BIST50 plus next 50 (broader large-cap universe)
BIST100_EXTRA_CONSTITUENTS: List[str] = [
    "MPARK",  # MLP Sağlık Hizmetleri
    "BERA",   # Bera Holding
    "GESAN",  # Girişim Elektrik Sanayi
    "KONTR",  # Kontrolmatik Teknoloji
    "EUREN",  # Eurenas Eurasian Eurobond
    "AKSEN",  # Aksa Enerji Üretim
    "AGHOL",  # Anadolu Grubu Holding
    "ALARK",  # Alarko Holding
    "BRSAN",  # Borusan Mannesmann
    "BFREN",  # Bosch Fren Sistemleri
    "DOHOL",  # Doğan Şirketler Grubu Holding
    "EKGYO",  # Emlak Konut GYO
    "GUBRF",  # Gübre Fabrikaları
    "ANSGR",  # Anadolu Sigorta
    "BRYAT",  # Borusan Yatırım
    "GLYHO",  # Global Yatırım Holding
    "KARTN",  # Kartonsan Karton Sanayi
    "KLMSN",  # Klimasan Klima Sanayi
    "LOGO",   # Logo Yazılım
    "MIATK",  # Mia Teknoloji
    "NETAS",  # Netaş Telekomünikasyon
    "NTHOL",  # Net Holding
    "SELEC",  # Selçuk Ecza Deposu
    "TMSN",   # Tümosan Motor ve Traktör
    "VESBE",  # Vestel Beyaz Eşya
    "YGGYO",  # Yeşil GYO
    "ZRGYO",  # Ziraat GYO
    "EGEEN",  # Ege Endüstri
    "YATAS",  # Yataş Yatak ve Yorgan
    "OTKAR",  # Otokar Otomotiv ve Savunma Sanayi
    "TTRAK",  # Türk Traktör
    "EGGUB",  # Ege Gübre Sanayi
    "EGSER",  # Ege Seramik
    "ANELE",  # Anel Elektrik
    "BANVT",  # Banvit Bandırma Vitaminli Yem
    "BLCYT",  # Bilici Yatırım
    "CEMTS",  # Çemtaş Çelik Makina Sanayi
    "ECILC",  # EİS Eczacıbaşı İlaç
    "INTEM",  # İntema İnşaat ve Tesisat
    "KAREL",  # Karel Elektronik
    "ORGE",   # Orge Enerji Elektrik
    "PARSN",  # Parsan Makina Parçaları
    "PRKAB",  # Türk Prysmian Kablo
    "PRKME",  # Park Elek. Madencilik
    "RAYSG",  # Ray Sigorta
    "EGEPO",  # Ege Profil Tic. ve San.
    "DEVA",   # Deva Holding
    "FENER",  # Fenerbahçe Futbol A.Ş.
    "ZOREN",  # Zorlu Enerji Elektrik
    "SKBNK",  # Şekerbank
]


def _bist30_set() -> set:
    return set(BIST30_CONSTITUENTS)


def _bist50_set() -> set:
    return set(BIST30_CONSTITUENTS) | set(BIST50_EXTRA_CONSTITUENTS)


def _bist100_set() -> set:
    return _bist50_set() | set(BIST100_EXTRA_CONSTITUENTS)


# Full ordered lists
BIST50_CONSTITUENTS: List[str] = list(BIST30_CONSTITUENTS) + list(BIST50_EXTRA_CONSTITUENTS)
BIST100_CONSTITUENTS: List[str] = list(BIST50_CONSTITUENTS) + list(BIST100_EXTRA_CONSTITUENTS)


# BIST KATILIM (Participation Index / XK100) — Islamic finance-compliant
# Excludes interest-based banks, conventional insurance, alcohol, gambling.
BIST_KATILIM_CONSTITUENTS: List[str] = [
    "THYAO",  # Türk Hava Yolları
    "ASELS",  # Aselsan
    "KCHOL",  # Koç Holding
    "TUPRS",  # Tüpraş
    "EREGL",  # Ereğli Demir Çelik
    "BIMAS",  # BİM
    "MGROS",  # Migros
    "FROTO",  # Ford Otosan
    "TOASO",  # Tofaş
    "SAHOL",  # Sabancı Holding
    "SISE",   # Şişe Cam
    "ARCLK",  # Arçelik
    "ENKAI",  # Enka İnşaat
    "TCELL",  # Turkcell
    "TTKOM",  # Türk Telekom
    "TAVHL",  # TAV Havalimanları
    "PGSUS",  # Pegasus
    "PETKM",  # Petkim
    "SASA",   # Sasa Polyester
    "KOZAL",  # Koza Altın
    "ULKER",  # Ülker
    "HEKTS",  # Hektaş
    "MPARK",  # MLP Sağlık
    "AKSEN",  # Aksa Enerji
    "AGHOL",  # Anadolu Grubu Holding
    "ALARK",  # Alarko Holding
    "GUBRF",  # Gübre Fabrikaları
    "KORDS",  # Kordsa
    "BRSAN",  # Borusan Mannesmann
    "SMRTG",  # Smart Güneş Teknolojileri
    "GESAN",  # Girişim Elektrik
    "KONTR",  # Kontrolmatik
    "ASTOR",  # Astor Enerji
    "YEOTK",  # Yeo Teknoloji
    "TTRAK",  # Türk Traktör
]


def get_bist30_symbols() -> List[str]:
    """Return BIST30 constituent symbols with BIST: prefix."""
    return [f"BIST:{s}" for s in BIST30_CONSTITUENTS]


def get_bist50_symbols() -> List[str]:
    """Return BIST50 constituent symbols with BIST: prefix."""
    return [f"BIST:{s}" for s in BIST50_CONSTITUENTS]


def get_bist100_symbols() -> List[str]:
    """Return BIST100 constituent symbols with BIST: prefix."""
    return [f"BIST:{s}" for s in BIST100_CONSTITUENTS]


def get_bist_katilim_symbols() -> List[str]:
    """Return BIST KATILIM (Participation) constituent symbols with BIST: prefix."""
    return [f"BIST:{s}" for s in BIST_KATILIM_CONSTITUENTS]


# Index metadata
BIST_INDICES: Dict[str, dict] = {
    "BIST30": {
        "name": "BIST 30 (XU030)",
        "description": "Top 30 most liquid blue-chip stocks, weighted by free-float market cap",
        "constituents_count": len(BIST30_CONSTITUENTS),
        "get_symbols": get_bist30_symbols,
    },
    "BIST50": {
        "name": "BIST 50 (XU050)",
        "description": "Top 50 stocks — BIST30 + next 20 most liquid mid-large caps",
        "constituents_count": len(BIST50_CONSTITUENTS),
        "get_symbols": get_bist50_symbols,
    },
    "BIST100": {
        "name": "BIST 100 (XU100)",
        "description": "Headline index — top 100 stocks by liquidity & market cap",
        "constituents_count": len(BIST100_CONSTITUENTS),
        "get_symbols": get_bist100_symbols,
    },
    "BISTKATILIM": {
        "name": "BIST Katılım (XK100)",
        "description": "Participation index — Islamic finance-compliant stocks "
                       "(excludes interest-based banks, conventional insurance, alcohol, gambling)",
        "constituents_count": len(BIST_KATILIM_CONSTITUENTS),
        "get_symbols": get_bist_katilim_symbols,
    },
}


def get_index_names() -> List[str]:
    """Return list of available BIST index names."""
    return list(BIST_INDICES.keys())


def is_bist30_stock(symbol: str) -> bool:
    """Check if a symbol is in the BIST30 index."""
    clean = symbol.upper().replace("BIST:", "")
    return clean in _bist30_set()


def is_bist50_stock(symbol: str) -> bool:
    """Check if a symbol is in the BIST50 index."""
    clean = symbol.upper().replace("BIST:", "")
    return clean in _bist50_set()


def is_bist100_stock(symbol: str) -> bool:
    """Check if a symbol is in the BIST100 index."""
    clean = symbol.upper().replace("BIST:", "")
    return clean in _bist100_set()
