from config.settings import APP_NAME, VERSION, DEFAULT_MODE
from watchlist import WATCHLIST, get_ticker_symbols, get_stocks_by_category


def display_watchlist(watchlist):
    print(f"Current watchlist ({len(watchlist)} stocks):")
    for item in watchlist:
        print(f"- {item['ticker']} ({item['category']})")


def main():
    print(f"{APP_NAME} v{VERSION}")
    print(f"Mode: {DEFAULT_MODE}")
    display_watchlist(WATCHLIST)

    print("\nTicker symbols only:")
    for ticker in get_ticker_symbols():
        print(f"- {ticker}")

    print("\nGrowth stocks:")
    growth_stocks = get_stocks_by_category("growth")
    for item in growth_stocks:
        print(f"- {item['ticker']} ({item['category']})")


if __name__ == "__main__":
    main()