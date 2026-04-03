from config.settings import APP_NAME, VERSION, DEFAULT_MODE
from watchlist import WATCHLIST, get_ticker_symbols, get_stocks_by_category


def display_watchlist(watchlist, title):
    print(f"\n{title} ({len(watchlist)} stocks):")
    for item in watchlist:
        print(f"- {item['ticker']} ({item['category']})")


def main():
    print(f"{APP_NAME} v{VERSION}")
    print(f"Mode: {DEFAULT_MODE}")

    display_watchlist(WATCHLIST, "Current watchlist")

    print("\nTicker symbols only:")
    for ticker in get_ticker_symbols():
        print(f"- {ticker}")

    display_watchlist(get_stocks_by_category("growth"), "Growth stocks")
    display_watchlist(get_stocks_by_category("dividend"), "Dividend stocks")
    display_watchlist(get_stocks_by_category("reit"), "REIT stocks")
    display_watchlist(get_stocks_by_category("etf"), "ETF stocks")


if __name__ == "__main__":
    main()