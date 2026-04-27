from config.settings import APP_NAME, VERSION, DEFAULT_MODE
from helpers import (
    print_banner,
    print_menu,
    display_watchlist,
    display_categories,
    display_ticker_symbols,
    display_stock_lookup,
    display_trade_history,
)
from paper_trading import (
    create_paper_portfolio,
    paper_buy,
    paper_sell,
    get_portfolio_summary,
    get_trade_history,
)
from research.stock_research import build_basic_stock_report
from strategy import get_strategy_profile
from trade_decision import evaluate_paper_trade_decision
from watchlist import (
    load_watchlist,
    get_categories,
    get_stocks_by_category,
    get_stock_by_ticker,
    get_ticker_symbols,
    add_stock,
    remove_stock,
)


def main():
    print_banner(APP_NAME, VERSION, DEFAULT_MODE)
    portfolio = create_paper_portfolio()

    while True:
        print_menu()

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            watchlist = load_watchlist()
            display_watchlist(watchlist, "Current watchlist")

        elif choice == "2":
            categories = get_categories()
            display_categories(categories)

        elif choice == "3":
            category = input("Enter category: ").strip().lower()
            stocks = get_stocks_by_category(category)
            display_watchlist(stocks, f"{category.title()} stocks")

        elif choice == "4":
            ticker = input("Enter ticker: ").strip().upper()
            stock = get_stock_by_ticker(ticker)
            display_stock_lookup(ticker, stock)

        elif choice == "5":
            ticker = input("Enter ticker to add: ").strip()
            category = input("Enter category: ").strip()

            if not ticker or not category:
                print("Ticker and category are required.")
                continue

            success = add_stock(ticker, category)

            if success:
                print(f"Added {ticker.upper()} as {category.lower()}.")
            else:
                print(f"{ticker.upper()} is already in the watchlist.")

        elif choice == "6":
            ticker = input("Enter ticker to remove: ").strip()

            if not ticker:
                print("Ticker is required.")
                continue

            success = remove_stock(ticker)

            if success:
                print(f"Removed {ticker.upper()} from the watchlist.")
            else:
                print(f"{ticker.upper()} was not found in the watchlist.")

        elif choice == "7":
            symbols = get_ticker_symbols()
            display_ticker_symbols(symbols)

        elif choice == "8":
            ticker = input("Enter ticker for research: ").strip().upper()
            report = build_basic_stock_report(ticker)

            print("\nBasic stock research report:")
            print(f"- ticker: {report['ticker']}")
            print(f"- status: {report['status']}")
            print(f"- in_watchlist: {report['in_watchlist']}")
            print(f"- summary: {report['summary']}")
            print(f"- category_guess: {report['category_guess']}")
            print("- notes:")
            for note in report["notes"]:
                print(f"  - {note}")

        elif choice == "9":
            strategy_name = input("Enter strategy name (balanced/aggressive): ").strip().lower()
            profile = get_strategy_profile(strategy_name)

            if profile is None:
                print("Strategy not found.")
                continue

            print(f"\nStrategy profile: {strategy_name}")
            for key, value in profile.items():
                print(f"- {key}: {value}")

        elif choice == "10":
            ticker = input("Enter ticker to paper buy: ").strip().upper()
            price = input("Enter buy price: ").strip()
            shares = input("Enter number of shares: ").strip()

            success, message = paper_buy(portfolio, ticker, float(price), int(shares))
            print(message)

            summary = get_portfolio_summary(portfolio)
            print(f"Cash remaining: {summary['cash']:.2f}")
            print(f"Open positions: {summary['position_count']}")
            print(f"Tickers held: {summary['tickers']}")
            print(f"Trade count: {summary['trade_count']}")

        elif choice == "11":
            ticker = input("Enter ticker to paper sell: ").strip().upper()
            price = input("Enter sell price: ").strip()
            shares = input("Enter number of shares: ").strip()

            success, message = paper_sell(portfolio, ticker, float(price), int(shares))
            print(message)

            summary = get_portfolio_summary(portfolio)
            print(f"Cash remaining: {summary['cash']:.2f}")
            print(f"Open positions: {summary['position_count']}")
            print(f"Tickers held: {summary['tickers']}")
            print(f"Trade count: {summary['trade_count']}")

        elif choice == "12":
            summary = get_portfolio_summary(portfolio)
            print("\nPaper portfolio summary:")
            print(f"- cash: {summary['cash']:.2f}")
            print(f"- open_positions: {summary['position_count']}")
            print(f"- tickers_held: {summary['tickers']}")
            print(f"- trade_count: {summary['trade_count']}")

        elif choice == "13":
            trade_history = get_trade_history(portfolio)
            display_trade_history(trade_history)

        elif choice == "14":
            from strategy_rules import evaluate_trade_setup

            strategy_name = input("Enter strategy name (balanced/aggressive): ").strip().lower()
            portfolio_cash = float(input("Enter portfolio cash: ").strip())
            position_size_dollars = float(input("Enter position size in dollars: ").strip())
            entry_price = float(input("Enter entry price: ").strip())
            stop_loss_price = float(input("Enter stop loss price: ").strip())
            take_profit_price = float(input("Enter take profit price: ").strip())

            result = evaluate_trade_setup(
                strategy_name=strategy_name,
                portfolio_cash=portfolio_cash,
                position_size_dollars=position_size_dollars,
                entry_price=entry_price,
                stop_loss_price=stop_loss_price,
                take_profit_price=take_profit_price,
            )

            print("\nStrategy evaluation result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

        elif choice == "15":
            strategy_name = input("Enter strategy name (balanced/aggressive): ").strip().lower()
            portfolio_cash = float(input("Enter portfolio cash: ").strip())
            position_size_dollars = float(input("Enter position size in dollars: ").strip())
            entry_price = float(input("Enter entry price: ").strip())
            stop_loss_price = float(input("Enter stop loss price: ").strip())
            take_profit_price = float(input("Enter take profit price: ").strip())

            result = evaluate_paper_trade_decision(
                strategy_name=strategy_name,
                portfolio_cash=portfolio_cash,
                position_size_dollars=position_size_dollars,
                entry_price=entry_price,
                stop_loss_price=stop_loss_price,
                take_profit_price=take_profit_price,
            )

            print("\nPaper trade decision result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

        elif choice == "0":
            print("Exiting AI Portfolio Assistant.")
            break

        else:
            print("Invalid option. Please choose a valid menu number.")


if __name__ == "__main__":
    main()