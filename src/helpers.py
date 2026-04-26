def print_banner(app_name, version, mode):
    print(f"{app_name} v{version}")
    print(f"Mode: {mode}")


def print_menu():
    print("\nMenu")
    print("1. View full watchlist")
    print("2. View available categories")
    print("3. View stocks by category")
    print("4. Look up stock by ticker")
    print("5. Add stock")
    print("6. Remove stock")
    print("7. Show ticker symbols only")
    print("8. Build basic stock research report")
    print("9. View strategy profile")
    print("10. Paper buy test")
    print("11. Paper sell test")
    print("12. View paper portfolio summary")
    print("13. View paper trade journal")
    print("14. Evaluate strategy trade setup")
    print("0. Exit")


def display_watchlist(watchlist, title):
    print(f"\n{title} ({len(watchlist)} stocks):")

    if not watchlist:
        print("- none")
        return

    for item in watchlist:
        print(f"- {item['ticker']} ({item['category']})")


def display_categories(categories):
    print("\nAvailable categories:")

    if not categories:
        print("- none")
        return

    for category in categories:
        print(f"- {category}")


def display_ticker_symbols(symbols):
    print("\nTicker symbols only:")

    if not symbols:
        print("- none")
        return

    for ticker in symbols:
        print(f"- {ticker}")


def display_stock_lookup(ticker, stock):
    print(f"\nStock lookup for {ticker.upper()}:")

    if stock is None:
        print("- not found")
        return

    print(f"- ticker: {stock['ticker']}")
    print(f"- category: {stock['category']}")


def display_trade_history(trade_history):
    print("\nPaper trade journal:")

    if not trade_history:
        print("- no trades recorded")
        return

    for index, trade in enumerate(trade_history, start=1):
        print(
            f"{index}. {trade['action']} {trade['ticker']} | "
            f"shares={trade['shares']} | "
            f"price={trade['price']:.2f} | "
            f"total={trade['total']:.2f}"
        )