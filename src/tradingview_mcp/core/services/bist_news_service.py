"""BIST News & Disclosure Service.

Scrapes Turkish financial sources for BIST-listed stocks. Returns structured
data; the calling layer (Claude Desktop's LLM) interprets and evaluates.

Sources:
- **Bigpara** (bigpara.hurriyet.com.tr): stock-specific page scraping. Most
  parseable, ticker-only URL pattern.
- **Mynet Finans** (finans.mynet.com): stock-specific page scraping. SSR
  content but URL needs a slug — we maintain a small ticker→slug map and
  fall back to a search URL if unknown.
- **KAP** (kap.org.tr): URL bundle only. Their frontend is Next.js
  client-rendered with no SSR data dump — scraping requires a headless
  browser (playwright). Out of scope for this iteration; the URLs are
  surfaced so the caller (or Claude Desktop's WebFetch) can grab them.

Caching: 15-minute in-memory TTL keyed by (source, symbol). News doesn't
move minute-to-minute, and respecting publisher servers matters.

All public functions return plain dicts and are independently unit-testable.
"""
from __future__ import annotations

import gzip
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from threading import RLock
from typing import Any

try:
    from bs4 import BeautifulSoup
    _BS4_AVAILABLE = True
except ImportError:
    _BS4_AVAILABLE = False

# ── HTTP helpers ──────────────────────────────────────────────────────────────

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
_DEFAULT_HEADERS = {
    "User-Agent": _UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate",
}
_FETCH_TIMEOUT = 10  # seconds


def _fetch_html(url: str, timeout: float = _FETCH_TIMEOUT) -> str | None:
    """Fetch HTML with proper headers and gzip handling. Returns None on error."""
    try:
        req = urllib.request.Request(url, headers=_DEFAULT_HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return raw.decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None


# ── TTL cache ─────────────────────────────────────────────────────────────────

_CACHE_TTL_SECONDS = 900  # 15 min
_cache: dict[tuple, tuple[float, Any]] = {}
_cache_lock = RLock()


def _cache_get(key: tuple) -> Any | None:
    with _cache_lock:
        entry = _cache.get(key)
        if entry is None:
            return None
        ts, value = entry
        if time.time() - ts > _CACHE_TTL_SECONDS:
            _cache.pop(key, None)
            return None
        return value


def _cache_set(key: tuple, value: Any) -> None:
    with _cache_lock:
        _cache[key] = (time.time(), value)


# ── Symbol helpers ────────────────────────────────────────────────────────────

def _clean_symbol(symbol: str) -> str:
    """Strip BIST: prefix and uppercase. 'BIST:EREGL' → 'EREGL'."""
    raw = (symbol or "").strip().upper()
    if ":" in raw:
        raw = raw.split(":", 1)[1]
    return raw


# Bigpara uses just the ticker in URL — clean.
def _bigpara_stock_url(symbol: str) -> str:
    s = _clean_symbol(symbol)
    return f"https://bigpara.hurriyet.com.tr/borsa/hisse-fiyatlari/{s}/"


def _bigpara_news_url(symbol: str) -> str:
    s = _clean_symbol(symbol)
    return f"https://bigpara.hurriyet.com.tr/borsa/hisse-haberleri/{s}/"


# Mynet uses ticker-slug format. Without a slug we can try ticker-only redirect.
# Add to this map as we learn the slugs (live verification recommended).
_MYNET_SLUGS: dict[str, str] = {
    "EREGL": "eregl-eregli-demir-celik",
    "THYAO": "thyao-turk-hava-yollari",
    "AKBNK": "akbnk-akbank",
    "GARAN": "garan-turkiye-garanti-bankasi",
    "ISCTR": "isctr-turkiye-is-bankasi-c",
    "KCHOL": "kchol-koc-holding",
    "SAHOL": "sahol-haci-omer-sabanci-holding",
    "ASELS": "asels-aselsan-elektronik-sanayi-ve",
    "BIMAS": "bimas-bim-birlesik-magazalar",
    "TUPRS": "tuprs-tupras-turkiye-petrol-rafinerileri",
    "FROTO": "froto-ford-otomotiv-sanayi",
    "PETKM": "petkm-petkim-petrokimya-holding",
    "TCELL": "tcell-turkcell-iletisim-hizmetleri",
    "VAKBN": "vakbn-vakiflar-bankasi",
    "YKBNK": "ykbnk-yapi-ve-kredi-bankasi",
    "HALKB": "halkb-turkiye-halk-bankasi",
    "GUBRF": "gubrf-gubre-fabrikalari",
    "ASTOR": "astor-astor-enerji",
    "INDES": "indes-indeks-bilgisayar",
    "PENTA": "penta-penta-teknoloji",
}


def _mynet_stock_url(symbol: str) -> str:
    s = _clean_symbol(symbol)
    slug = _MYNET_SLUGS.get(s)
    if slug:
        return f"https://finans.mynet.com/borsa/hisseler/{slug}/"
    # Fallback: try ticker-only; Mynet sometimes redirects but may 404.
    return f"https://finans.mynet.com/borsa/hisseler/{s.lower()}/"


# KAP URL — best-effort search URL. Real disclosure list pages need company
# OID (e.g. 1010 for EREGL) and we don't maintain that mapping yet.
def _kap_search_url(symbol: str) -> str:
    s = _clean_symbol(symbol)
    return f"https://www.kap.org.tr/tr/bildirim-sorgu?keyword={urllib.parse.quote(s)}"


def _tradingview_news_url(symbol: str) -> str:
    s = _clean_symbol(symbol)
    return f"https://www.tradingview.com/symbols/BIST-{s}/news/"


# ── Bigpara scraper ───────────────────────────────────────────────────────────

_UI_NOISE_TITLES = {
    "tümünü göster", "devamı", "daha fazla", "tümü", "diğer haberler",
    "tüm haberler", "haber detayı",
}


def _parse_bigpara_news(html: str, limit: int = 10) -> list[dict]:
    """Extract news items from a Bigpara stock page or news page.

    Note: Bigpara stock pages render generic sidebar news, not symbol-specific
    articles. Items are tagged stock_specific=False so callers can weigh them
    as market backdrop rather than direct signal.
    """
    if not _BS4_AVAILABLE or not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    items: list[dict] = []
    seen: set[str] = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.startswith("/haberler/"):
            continue
        # Real articles have ≥3 path segments: /haberler/<category>/<slug>/
        parts = [p for p in href.strip("/").split("/") if p]
        if len(parts) < 3:
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 12:
            continue
        if title.lower() in _UI_NOISE_TITLES:
            continue
        full_url = urllib.parse.urljoin("https://bigpara.hurriyet.com.tr", href)
        if full_url in seen:
            continue
        seen.add(full_url)

        published = None
        parent = a.parent
        if parent:
            date_el = parent.find(class_=re.compile(r"date|time|tarih", re.I))
            if date_el:
                published = date_el.get_text(strip=True)

        items.append({
            "title": title,
            "url": full_url,
            "summary": None,
            "published": published,
            "source": "Bigpara",
            "stock_specific": False,
        })
        if len(items) >= limit:
            break
    return items


def fetch_bigpara_news(symbol: str, limit: int = 10, use_cache: bool = True) -> list[dict]:
    """Fetch news items for a BIST symbol from Bigpara.

    Note: Bigpara doesn't publish stock-specific article listings — its stock
    page only links to general news categories. Falls back to the general
    Bigpara RSS feed (market-wide news) so the calling LLM still has Turkish
    market context to evaluate against. Items returned are NOT
    symbol-filtered; treat them as market backdrop.
    """
    sym = _clean_symbol(symbol)
    key = ("bigpara_general", sym, limit)
    if use_cache:
        hit = _cache_get(key)
        if hit is not None:
            return hit

    # Try the stock page first in case Bigpara starts surfacing articles later.
    html = _fetch_html(_bigpara_stock_url(sym))
    items = _parse_bigpara_news(html or "", limit=limit)

    # Fall back to the general feed if we found nothing.
    if not items:
        items = _fetch_bigpara_general_rss(limit=limit)

    _cache_set(key, items)
    return items


def _fetch_bigpara_general_rss(limit: int = 10) -> list[dict]:
    """Pull Bigpara's general 'GÜNDEM' RSS feed. Not stock-specific —
    used as market context backdrop."""
    try:
        import feedparser
    except ImportError:
        return []
    try:
        feed = feedparser.parse(
            "https://bigpara.hurriyet.com.tr/rss/",
            agent=_UA,
            request_headers={"User-Agent": _UA},
        )
    except Exception:
        return []
    items: list[dict] = []
    for entry in feed.entries[:limit]:
        title = entry.get("title", "").strip()
        if not title:
            continue
        items.append({
            "title": title,
            "url": entry.get("link", ""),
            "summary": entry.get("summary", "")[:200] or None,
            "published": entry.get("published", None),
            "source": "Bigpara (general)",
            "stock_specific": False,
        })
    return items


# ── Mynet scraper ─────────────────────────────────────────────────────────────

def _parse_mynet_news(html: str, limit: int = 10) -> list[dict]:
    """Extract news items from a Mynet Finans stock page."""
    if not _BS4_AVAILABLE or not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    items: list[dict] = []
    seen: set[str] = set()

    # Mynet renders article cards with anchors to /haber/<slug>.
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/haber/" not in href and "/haberi/" not in href:
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 12:
            continue
        full_url = urllib.parse.urljoin("https://finans.mynet.com", href)
        # Filter to financial news domains
        if "mynet.com" not in full_url:
            continue
        if full_url in seen:
            continue
        seen.add(full_url)
        items.append({
            "title": title,
            "url": full_url,
            "summary": None,
            "published": None,
            "source": "Mynet Finans",
            "stock_specific": True,  # Mynet's stock page anchors are usually
                                       # relevant; LLM should still verify by title.
        })
        if len(items) >= limit:
            break
    return items


def fetch_mynet_news(symbol: str, limit: int = 10, use_cache: bool = True) -> list[dict]:
    """Fetch news items for a BIST symbol from Mynet Finans."""
    sym = _clean_symbol(symbol)
    key = ("mynet", sym, limit)
    if use_cache:
        hit = _cache_get(key)
        if hit is not None:
            return hit
    url = _mynet_stock_url(sym)
    html = _fetch_html(url)
    items = _parse_mynet_news(html or "", limit=limit)
    _cache_set(key, items)
    return items


# ── KAP — URL bundle only (frontend Next.js client-render limits scraping) ──

def get_kap_links(symbol: str) -> dict:
    """Return KAP-related URLs for a BIST symbol.

    Note: scraping disclosure content requires playwright (KAP's frontend is
    Next.js client-rendered with no SSR data). Out of scope here. Surface the
    URLs so Claude Desktop's WebFetch can grab them or the user can click.
    """
    sym = _clean_symbol(symbol)
    return {
        "symbol": sym,
        "search": _kap_search_url(sym),
        "instructions": (
            "KAP frontend is JavaScript-rendered — direct scraping not supported "
            "in this version. Open the search URL in browser to view disclosures, "
            "or call WebFetch from Claude Desktop on the rendered page."
        ),
    }


# ── Aggregation ───────────────────────────────────────────────────────────────

def get_news_links(symbol: str) -> dict:
    """Return all news/disclosure URLs for a BIST symbol — for manual review
    or downstream WebFetch by the LLM layer."""
    sym = _clean_symbol(symbol)
    return {
        "symbol": sym,
        "bigpara_stock": _bigpara_stock_url(sym),
        "bigpara_news": _bigpara_news_url(sym),
        "mynet_stock": _mynet_stock_url(sym),
        "kap_search": _kap_search_url(sym),
        "tradingview_news": _tradingview_news_url(sym),
        "mynet_slug_known": sym in _MYNET_SLUGS,
    }


def fetch_bist_news(
    symbol: str,
    source: str = "all",
    limit_per_source: int = 10,
) -> dict:
    """Fetch news items from one or all sources.

    Args:
        symbol: BIST stock symbol (e.g. 'EREGL' or 'BIST:EREGL').
        source: One of 'bigpara', 'mynet', or 'all' (default).
        limit_per_source: Max items to fetch per source.

    Returns:
        Dict with per-source item lists + a merged 'items' list.
    """
    sym = _clean_symbol(symbol)
    src = (source or "all").strip().lower()
    out: dict[str, Any] = {"symbol": sym, "source_filter": src, "sources": {}}

    if src in ("bigpara", "all"):
        out["sources"]["bigpara"] = fetch_bigpara_news(sym, limit=limit_per_source)
    if src in ("mynet", "all"):
        out["sources"]["mynet"] = fetch_mynet_news(sym, limit=limit_per_source)

    merged: list[dict] = []
    for items in out["sources"].values():
        merged.extend(items)
    out["items"] = merged
    out["total_items"] = len(merged)
    return out


# ── Rule-based sentiment / flag heuristics ────────────────────────────────────

# Turkish keyword sets for rule-based sentiment scoring. Conservative — only
# strong-signal terms. Anything ambiguous returns neutral.
_POSITIVE_KEYWORDS = {
    "kar artışı", "kar büyümesi", "rekor kar", "rekor satış", "rekor ciro",
    "büyüme", "yükseliş", "yükselişle", "tavan", "ihracat artışı",
    "yatırım", "alım önerisi", "yükseliş trendi", "güçlü performans",
    "olumlu", "pozitif", "rekor", "temettü", "kar payı", "bedelsiz",
    "sermaye artırımı", "yeni anlaşma", "yeni sözleşme", "ortaklık",
    "satın alma", "yeni fabrika", "yeni tesis", "kapasite artışı",
    "halka arz başarılı", "kar açıkladı",
}

_NEGATIVE_KEYWORDS = {
    "zarar", "düşüş", "iflas", "kayıp", "kriz", "satış önerisi",
    "soruşturma", "dava", "ceza", "mahkeme", "düşüş trendi",
    "olumsuz", "negatif", "uyarı", "yangın", "kaza", "ölü", "yaralı",
    "üretim durdu", "fabrika kapatıldı", "ihracat yasağı", "yaptırım",
    "spk soruşturması", "borçlanma", "temerrüt", "konkordato",
    "tasarruf önlemi", "kapatma", "küçülme",
}

# KAP/disclosure category keywords (when present in title, marks the kind
# of regulatory event — important context regardless of sentiment).
_KAP_CATEGORY_KEYWORDS = {
    "bilanço": "financial_report",
    "finansal rapor": "financial_report",
    "kar payı": "dividend",
    "temettü": "dividend",
    "sermaye artırımı": "capital_increase",
    "olağanüstü genel kurul": "extraordinary_meeting",
    "olağan genel kurul": "annual_meeting",
    "yönetim kurulu": "board_decision",
    "esas sözleşme": "articles_of_association",
    "özel durum": "material_event",
    "olağandışı": "unusual_event",
    "geri alım": "buyback",
    "halka arz": "ipo",
    "birleşme": "merger",
    "devralma": "acquisition",
    "iştirak": "subsidiary",
}


def _classify_item(title: str) -> dict:
    """Tag a news/disclosure title with sentiment + category hints.

    Pure heuristic — meant to surface signal, not replace LLM judgment.
    """
    t = (title or "").lower()
    pos_hits = [k for k in _POSITIVE_KEYWORDS if k in t]
    neg_hits = [k for k in _NEGATIVE_KEYWORDS if k in t]
    categories = [v for k, v in _KAP_CATEGORY_KEYWORDS.items() if k in t]

    if pos_hits and not neg_hits:
        sentiment = "positive"
    elif neg_hits and not pos_hits:
        sentiment = "negative"
    elif pos_hits and neg_hits:
        sentiment = "mixed"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "positive_keywords": pos_hits,
        "negative_keywords": neg_hits,
        "categories": list(set(categories)),
    }


def build_news_digest(symbol: str, limit: int = 15) -> dict:
    """Aggregate news from all sources, classify each item, return structured digest.

    The returned dict is designed to be consumed by an LLM in the calling
    layer (Claude Desktop) — pre-classification surfaces obvious signal so the
    LLM can focus on synthesis.
    """
    sym = _clean_symbol(symbol)
    news = fetch_bist_news(sym, source="all", limit_per_source=limit)
    items = news.get("items") or []

    classified = []
    sentiment_counts = {"positive": 0, "negative": 0, "mixed": 0, "neutral": 0}
    category_counts: dict[str, int] = {}
    flags: list[str] = []

    for it in items:
        c = _classify_item(it.get("title", ""))
        sentiment_counts[c["sentiment"]] += 1
        for cat in c["categories"]:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        classified.append({**it, **c})

    # Rule-based flags
    if sentiment_counts["negative"] >= 3:
        flags.append("Multiple negative news items — review carefully before trading")
    if "unusual_event" in category_counts or "material_event" in category_counts:
        flags.append("KAP material/unusual event mentioned — check official KAP disclosure")
    if "extraordinary_meeting" in category_counts:
        flags.append("Extraordinary general meeting referenced — material decisions ahead")
    if "dividend" in category_counts:
        flags.append("Dividend / kar payı news present — price may have ex-dividend gap")

    links = get_news_links(sym)

    return {
        "symbol": sym,
        "total_items": len(classified),
        "items": classified[:limit],
        "sentiment_summary": sentiment_counts,
        "category_summary": category_counts,
        "flags": flags,
        "manual_review_links": {
            "kap_search": links["kap_search"],
            "tradingview_news": links["tradingview_news"],
        },
        "notes": [
            "Rule-based sentiment uses Turkish keyword matching — surface only, "
            "rely on LLM in the calling layer for nuanced evaluation.",
            "KAP disclosures are not fetched in this version (Next.js client-render "
            "limits direct scraping). Use the kap_search URL to verify regulatory data.",
        ],
    }
