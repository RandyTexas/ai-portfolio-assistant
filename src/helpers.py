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
    print("9. View risk profile")
    print("10. Paper buy test")
    print("11. Paper sell test")
    print("12. View paper portfolio summary")
    print("13. View paper trade journal")
    print("14. Evaluate strategy trade setup")
    print("15. Evaluate paper trade decision")
    print("16. Execute paper trade from strategy")
    print("17. Evaluate exit rules")
    print("18. View effective strategy with ticker override")
    print("19. Evaluate open paper position for exit")
    print("20. Execute paper auto-sell from exit rules")
    print("21. View trade-style matrix profile")
    print("22. View merged effective rules")
    print("23. Evaluate trade using merged effective rules")
    print("24. Execute paper trade using merged effective rules")
    print("25. Evaluate open position using merged effective rules")
    print("26. Create AI Builder change request")
    print("27. View AI Builder change requests")
    print("28. Update AI Builder request status")
    print("29. View approved AI Builder requests")
    print("30. Add approved request to implementation queue")
    print("31. View implementation queue")
    print("32. Update implementation queue status")
    print("33. Get latest stock bar from market data API")
    print("34. Get latest crypto bar from market data API")
    print("35. Refresh watchlist market data")
    print("36. Evaluate live trade using market data")
    print("37. Execute live paper trade using market data")
    print("38. Save manual override for ticker")
    print("39. View saved manual ticker override")
    print("40. Disable manual ticker override")
    print("41. Enable manual ticker override")
    print("42. Delete manual ticker override")
    print("43. List all saved manual ticker overrides")
    print("44. Edit saved manual ticker override")
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


def display_change_requests(requests):
    print("\nAI Builder change requests:")

    if not requests:
        print("- no requests saved")
        return

    for item in requests:
        print(
            f"{item['id']}. [{item['status']}] "
            f"{item['title']} | priority={item['priority']}"
        )
        print(f"   request: {item['request_text']}")
        print(f"   created_at: {item['created_at']}")


def display_implementation_queue(queue_items):
    print("\nImplementation queue:")

    if not queue_items:
        print("- no queued items")
        return

    for item in queue_items:
        print(
            f"{item['queue_id']}. request_id={item['request_id']} "
            f"[{item['queue_status']}] {item['title']} | priority={item['priority']}"
        )
        print(f"   request: {item['request_text']}")
        print(f"   queued_at: {item['queued_at']}")


def display_watchlist_market_data(results):
    print("\nWatchlist market data refresh:")

    if not results:
        print("- no watchlist results")
        return

    for item in results:
        print(f"- {item['ticker']} ({item['category']}) | status={item['status']}")

        if item["status"] == "ok" and item["bar"]:
            bar = item["bar"]
            print(f"   close: {bar['close']}")
            print(f"   high: {bar['high']}")
            print(f"   low: {bar['low']}")
            print(f"   volume: {bar['volume']}")
            print(f"   timestamp: {bar['timestamp']}")
        elif item["status"] == "error":
            print(f"   error: {item['error']}")


def display_manual_ticker_overrides(overrides):
    print("\nSaved manual ticker overrides:")

    if not overrides:
        print("- no saved manual overrides")
        return

    for item in overrides:
        print(f"- ticker: {item['ticker']}")
        print(f"  - name: {item['name']}")
        print(f"  - enabled: {item['enabled']}")
        print("  - rules:")
        if not item["rules"]:
            print("    - none")
        else:
            for key, value in item["rules"].items():
                print(f"    - {key}: {value}")