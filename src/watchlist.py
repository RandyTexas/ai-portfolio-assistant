import json
from copy import deepcopy

from config.settings import DATA_DIR, WATCHLIST_FILE, DEFAULT_WATCHLIST


def _normalize_stock_entry(ticker, category):
    return {
        "ticker": ticker.strip().upper(),
        "category": category.strip().lower(),
    }


def save_watchlist(watchlist):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_watchlist = [
        _normalize_stock_entry(item["ticker"], item["category"])
        for item in watchlist
    ]

    with WATCHLIST_FILE.open("w", encoding="utf-8") as file:
        json.dump(cleaned_watchlist, file, indent=4)


def ensure_watchlist_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not WATCHLIST_FILE.exists():
        save_watchlist(deepcopy(DEFAULT_WATCHLIST))


def load_watchlist():
    ensure_watchlist_file()

    with WATCHLIST_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        _normalize_stock_entry(item["ticker"], item["category"])
        for item in data
    ]


def get_ticker_symbols(watchlist=None):
    if watchlist is None:
        watchlist = load_watchlist()

    return [item["ticker"] for item in watchlist]


def has_ticker(ticker, watchlist=None):
    ticker = ticker.strip().upper()
    return ticker in get_ticker_symbols(watchlist)


def get_stock_by_ticker(ticker, watchlist=None):
    ticker = ticker.strip().upper()

    if watchlist is None:
        watchlist = load_watchlist()

    for item in watchlist:
        if item["ticker"] == ticker:
            return item

    return None


def get_stocks_by_category(category, watchlist=None):
    category = category.strip().lower()

    if watchlist is None:
        watchlist = load_watchlist()

    return [item for item in watchlist if item["category"] == category]


def get_categories(watchlist=None):
    if watchlist is None:
        watchlist = load_watchlist()

    return sorted({item["category"] for item in watchlist})


def add_stock(ticker, category):
    watchlist = load_watchlist()
    new_stock = _normalize_stock_entry(ticker, category)

    if has_ticker(new_stock["ticker"], watchlist):
        return False

    watchlist.append(new_stock)
    save_watchlist(watchlist)
    return True


def remove_stock(ticker):
    ticker = ticker.strip().upper()
    watchlist = load_watchlist()

    for item in watchlist:
        if item["ticker"] == ticker:
            watchlist.remove(item)
            save_watchlist(watchlist)
            return True

    return False