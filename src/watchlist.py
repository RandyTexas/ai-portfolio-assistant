WATCHLIST = [
    {"ticker": "AAPL", "category": "growth"},
    {"ticker": "MSFT", "category": "growth"},
    {"ticker": "KO", "category": "dividend"},
    {"ticker": "O", "category": "reit"},
    {"ticker": "SPY", "category": "etf"},
]


def get_ticker_symbols():
    return [item["ticker"] for item in WATCHLIST]


def has_ticker(ticker):
    return ticker.upper() in get_ticker_symbols()


def get_stock_by_ticker(ticker):
    ticker = ticker.upper()
    for item in WATCHLIST:
        if item["ticker"] == ticker:
            return item
    return None


def get_stocks_by_category(category):
    return [item for item in WATCHLIST if item["category"] == category]


def get_categories():
    return sorted({item["category"] for item in WATCHLIST})


def add_stock(ticker, category):
    ticker = ticker.upper()
    category = category.lower()

    if has_ticker(ticker):
        return False

    WATCHLIST.append({"ticker": ticker, "category": category})
    return True