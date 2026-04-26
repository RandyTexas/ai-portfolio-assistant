from watchlist import get_stock_by_ticker


def build_basic_stock_report(ticker):
    ticker = ticker.strip().upper()
    stock = get_stock_by_ticker(ticker)

    if stock is None:
        return {
            "ticker": ticker,
            "status": "research scaffold only",
            "in_watchlist": False,
            "summary": f"No saved watchlist entry or live market data yet for {ticker}.",
            "category_guess": None,
            "notes": [
                "This is a placeholder research report.",
                "Future versions will pull real market and company data.",
            ],
        }

    return {
        "ticker": ticker,
        "status": "watchlist match found",
        "in_watchlist": True,
        "summary": f"{ticker} is currently saved in the watchlist.",
        "category_guess": stock["category"],
        "notes": [
            "This is still a local scaffold report.",
            "Future versions will attach live market and company research.",
        ],
    }