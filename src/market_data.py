import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from config.settings import ALPACA_DATA_BASE_URL, ALPACA_CRYPTO_LOC
from watchlist import load_watchlist


def _get_auth_headers():
    api_key = os.getenv("APCA_API_KEY_ID", "").strip()
    api_secret = os.getenv("APCA_API_SECRET_KEY", "").strip()

    if not api_key or not api_secret:
        raise ValueError(
            "Missing Alpaca API credentials. Set APCA_API_KEY_ID and APCA_API_SECRET_KEY."
        )

    return {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": api_secret,
        "Accept": "application/json",
    }


def _fetch_json(url):
    headers = _get_auth_headers()
    request = Request(url, headers=headers, method="GET")

    try:
        with urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def get_latest_stock_bar(symbol, feed="iex"):
    symbol = symbol.strip().upper()

    params = urlencode({"feed": feed})
    url = f"{ALPACA_DATA_BASE_URL}/v2/stocks/{symbol}/bars/latest?{params}"

    data = _fetch_json(url)
    bar = data.get("bar")

    if not bar:
        return None

    return {
        "symbol": symbol,
        "asset_type": "stock",
        "timestamp": bar.get("t"),
        "open": bar.get("o"),
        "high": bar.get("h"),
        "low": bar.get("l"),
        "close": bar.get("c"),
        "volume": bar.get("v"),
    }


def get_latest_crypto_bar(symbol, loc=None):
    symbol = symbol.strip().upper()
    loc = loc or ALPACA_CRYPTO_LOC

    params = urlencode({"symbols": symbol})
    url = f"{ALPACA_DATA_BASE_URL}/v1beta3/crypto/{loc}/latest/bars?{params}"

    data = _fetch_json(url)
    bars = data.get("bars", {})
    bar = bars.get(symbol)

    if not bar:
        return None

    return {
        "symbol": symbol,
        "asset_type": "crypto",
        "timestamp": bar.get("t"),
        "open": bar.get("o"),
        "high": bar.get("h"),
        "low": bar.get("l"),
        "close": bar.get("c"),
        "volume": bar.get("v"),
    }


def get_latest_market_bar(symbol, feed="iex"):
    symbol = symbol.strip().upper()

    if "/" in symbol:
        return get_latest_crypto_bar(symbol)

    return get_latest_stock_bar(symbol, feed=feed)


def refresh_watchlist_market_data(feed="iex"):
    watchlist = load_watchlist()
    results = []

    for item in watchlist:
        symbol = item["ticker"]

        try:
            bar = get_latest_stock_bar(symbol, feed=feed)
            results.append(
                {
                    "ticker": symbol,
                    "category": item["category"],
                    "status": "ok" if bar else "no_data",
                    "bar": bar,
                }
            )
        except Exception as exc:
            results.append(
                {
                    "ticker": symbol,
                    "category": item["category"],
                    "status": "error",
                    "error": str(exc),
                    "bar": None,
                }
            )

    return results