def display_watchlist(watchlist, title):
    print(f"\n{title} ({len(watchlist)} stocks):")
    for item in watchlist:
        print(f"- {item['ticker']} ({item['category']})")