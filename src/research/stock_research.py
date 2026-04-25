def build_basic_stock_report(ticker):
    ticker = ticker.strip().upper()

    return {
        "ticker": ticker,
        "status": "research scaffold only",
        "summary": f"No live market data yet for {ticker}.",
        "category_guess": None,
        "notes": [
            "This is a placeholder research report.",
            "Future versions will pull real market and company data.",
        ],
    }