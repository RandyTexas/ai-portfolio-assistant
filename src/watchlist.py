WATCHLIST = [
    {"ticker": "AAPL", "category": "growth"},
    {"ticker": "MSFT", "category": "growth"},
    {"ticker": "KO", "category": "dividend"},
    {"ticker": "O", "category": "reit"},
    {"ticker": "SPY", "category": "etf"},
]


def get_ticker_symbols():
    return [item["ticker"] for item in WATCHLIST]


def get_stocks_by_category(category):
    return [item for item in WATCHLIST if item["category"] == category]


def get_categories():
    return sorted({item["category"] for item in WATCHLIST})