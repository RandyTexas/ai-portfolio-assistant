from market_data import get_latest_stock_bar
from watchlist import get_stock_by_ticker


def build_basic_stock_report(ticker, feed="iex"):
    ticker = ticker.strip().upper()
    stock = get_stock_by_ticker(ticker)

    market_data = None
    market_data_status = "not_requested"

    try:
        market_data = get_latest_stock_bar(ticker, feed=feed)
        market_data_status = "ok" if market_data else "no_data"
    except Exception as exc:
        market_data_status = f"error: {exc}"

    if stock is None:
        return {
            "ticker": ticker,
            "status": "research scaffold only",
            "in_watchlist": False,
            "summary": f"No saved watchlist entry yet for {ticker}.",
            "category_guess": None,
            "notes": [
                "This is a placeholder research report.",
                "Future versions will pull real company and market data.",
            ],
            "market_data_status": market_data_status,
            "latest_bar": market_data,
        }

    return {
        "ticker": ticker,
        "status": "watchlist match found",
        "in_watchlist": True,
        "summary": f"{ticker} is currently saved in the watchlist.",
        "category_guess": stock["category"],
        "notes": [
            f"{ticker} is tracked as a {stock['category']} idea.",
            "Future versions can add company fundamentals and news signals.",
        ],
        "market_data_status": market_data_status,
        "latest_bar": market_data,
    }
    