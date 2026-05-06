from live_trade_execution import execute_live_trade_with_effective_rules
from live_trade_decision import evaluate_live_trade_with_effective_rules
from ai_builder import (
    create_change_request,
    load_change_requests,
    update_change_request_status,
    get_approved_change_requests,
)
from implementation_queue import (
    add_approved_request_to_queue,
    load_implementation_queue,
    update_queue_item_status,
)
from market_data import (
    get_latest_stock_bar,
    get_latest_crypto_bar,
    get_latest_market_bar,
    refresh_watchlist_market_data,
)
from auto_exit import execute_auto_exit
from config.settings import APP_NAME, VERSION, DEFAULT_MODE
from effective_rules import build_effective_rules
from exit_rules import evaluate_exit_rules
from helpers import (
    print_banner,
    print_menu,
    display_watchlist,
    display_categories,
    display_ticker_symbols,
    display_stock_lookup,
    display_trade_history,
    display_change_requests,
    display_implementation_queue,
    display_watchlist_market_data,
)
from merged_position_exit import evaluate_position_with_effective_rules
from merged_trade_decision import evaluate_trade_with_effective_rules
from merged_trade_execution import execute_trade_with_effective_rules
from paper_trading import (
    create_paper_portfolio,
    paper_buy,
    paper_sell,
    get_portfolio_summary,
    get_trade_history,
)
from position_exit import evaluate_position_exit
from research.stock_research import build_basic_stock_report
from strategy import get_strategy_profile
from strategy_matrix import get_matrix_profile, list_matrix_profiles
from strategy_overrides import get_effective_strategy
from strategy_rules import evaluate_trade_setup
from trade_decision import evaluate_paper_trade_decision
from trade_execution import execute_paper_trade
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
            feed = input("Enter stock feed (iex/delayed_sip/sip) or leave blank for iex: ").strip().lower()
            if not feed:
                feed = "iex"

            report = build_basic_stock_report(ticker, feed=feed)

            print("\nBasic stock research report:")
            print(f"- ticker: {report['ticker']}")
            print(f"- status: {report['status']}")
            print(f"- in_watchlist: {report['in_watchlist']}")
            print(f"- summary: {report['summary']}")
            print(f"- category_guess: {report['category_guess']}")
            print(f"- market_data_status: {report['market_data_status']}")
            print("- notes:")
            for note in report["notes"]:
                print(f"  - {note}")

            latest_bar = report.get("latest_bar")
            if latest_bar:
                print("- latest_bar:")
                for key, value in latest_bar.items():
                    print(f"  - {key}: {value}")

        elif choice == "9":
            strategy_name = input("Enter risk profile name (passive/balanced/aggressive): ").strip().lower()
            profile = get_strategy_profile(strategy_name)

            if profile is None:
                print("Risk profile not found.")
                continue

            print(f"\nRisk profile: {strategy_name}")
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
            strategy_name = input("Enter risk profile name (passive/balanced/aggressive): ").strip().lower()
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
            strategy_name = input("Enter risk profile name (passive/balanced/aggressive): ").strip().lower()
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

        elif choice == "16":
            ticker = input("Enter ticker: ").strip().upper()
            strategy_name = input("Enter risk profile name (passive/balanced/aggressive): ").strip().lower()
            position_size_dollars = float(input("Enter position size in dollars: ").strip())
            entry_price = float(input("Enter entry price: ").strip())
            stop_loss_price = float(input("Enter stop loss price: ").strip())
            take_profit_price = float(input("Enter take profit price: ").strip())

            summary = get_portfolio_summary(portfolio)

            result = execute_paper_trade(
                portfolio=portfolio,
                ticker=ticker,
                strategy_name=strategy_name,
                portfolio_cash=summary["cash"],
                position_size_dollars=position_size_dollars,
                entry_price=entry_price,
                stop_loss_price=stop_loss_price,
                take_profit_price=take_profit_price,
            )

            print("\nPaper trade execution result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

            updated_summary = get_portfolio_summary(portfolio)
            print("\nUpdated portfolio summary:")
            print(f"- cash: {updated_summary['cash']:.2f}")
            print(f"- open_positions: {updated_summary['position_count']}")
            print(f"- tickers_held: {updated_summary['tickers']}")
            print(f"- trade_count: {updated_summary['trade_count']}")

        elif choice == "17":
            entry_price = float(input("Enter entry price: ").strip())
            current_price = float(input("Enter current price: ").strip())
            highest_price = float(input("Enter highest price reached: ").strip())

            take_profit_pct_input = input("Enter take profit % as decimal or leave blank (example 0.04): ").strip()
            take_profit_price_input = input("Enter take profit price or leave blank (example 110): ").strip()
            stop_loss_pct_input = input("Enter stop loss % as decimal or leave blank (example 0.05): ").strip()
            stop_loss_price_input = input("Enter stop loss price or leave blank (example 95): ").strip()
            trailing_stop_pct_input = input("Enter trailing stop % as decimal or leave blank (example 0.04): ").strip()
            trailing_stop_amount_input = input("Enter trailing stop dollar amount from peak or leave blank (example 5): ").strip()

            result = evaluate_exit_rules(
                entry_price=entry_price,
                current_price=current_price,
                highest_price=highest_price,
                take_profit_pct=float(take_profit_pct_input) if take_profit_pct_input else None,
                take_profit_price=float(take_profit_price_input) if take_profit_price_input else None,
                stop_loss_pct=float(stop_loss_pct_input) if stop_loss_pct_input else None,
                stop_loss_price=float(stop_loss_price_input) if stop_loss_price_input else None,
                trailing_stop_pct=float(trailing_stop_pct_input) if trailing_stop_pct_input else None,
                trailing_stop_amount=float(trailing_stop_amount_input) if trailing_stop_amount_input else None,
            )

            print("\nExit rule result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

        elif choice == "18":
            strategy_name = input("Enter risk profile name (passive/balanced/aggressive): ").strip().lower()
            ticker = input("Enter ticker for override check (or leave blank): ").strip().upper()

            profile = get_effective_strategy(strategy_name, ticker if ticker else None)

            if profile is None:
                print("Strategy not found.")
                continue

            print("\nEffective strategy result:")
            print(f"- strategy_name: {strategy_name}")
            print(f"- ticker: {ticker if ticker else 'none'}")
            for key, value in profile.items():
                print(f"- {key}: {value}")

        elif choice == "19":
            ticker = input("Enter ticker with open position: ").strip().upper()
            current_price = float(input("Enter current price: ").strip())
            highest_price = float(input("Enter highest price reached: ").strip())

            take_profit_pct_input = input("Enter take profit % as decimal or leave blank (example 0.04): ").strip()
            take_profit_price_input = input("Enter take profit price or leave blank (example 110): ").strip()
            stop_loss_pct_input = input("Enter stop loss % as decimal or leave blank (example 0.05): ").strip()
            stop_loss_price_input = input("Enter stop loss price or leave blank (example 95): ").strip()
            trailing_stop_pct_input = input("Enter trailing stop % as decimal or leave blank (example 0.04): ").strip()
            trailing_stop_amount_input = input("Enter trailing stop dollar amount from peak or leave blank (example 5): ").strip()

            result = evaluate_position_exit(
                portfolio=portfolio,
                ticker=ticker,
                current_price=current_price,
                highest_price=highest_price,
                take_profit_pct=float(take_profit_pct_input) if take_profit_pct_input else None,
                take_profit_price=float(take_profit_price_input) if take_profit_price_input else None,
                stop_loss_pct=float(stop_loss_pct_input) if stop_loss_pct_input else None,
                stop_loss_price=float(stop_loss_price_input) if stop_loss_price_input else None,
                trailing_stop_pct=float(trailing_stop_pct_input) if trailing_stop_pct_input else None,
                trailing_stop_amount=float(trailing_stop_amount_input) if trailing_stop_amount_input else None,
            )

            print("\nOpen position exit evaluation result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

        elif choice == "20":
            ticker = input("Enter ticker with open position: ").strip().upper()
            current_price = float(input("Enter current price: ").strip())
            highest_price = float(input("Enter highest price reached: ").strip())

            take_profit_pct_input = input("Enter take profit % as decimal or leave blank (example 0.04): ").strip()
            take_profit_price_input = input("Enter take profit price or leave blank (example 110): ").strip()
            stop_loss_pct_input = input("Enter stop loss % as decimal or leave blank (example 0.05): ").strip()
            stop_loss_price_input = input("Enter stop loss price or leave blank (example 95): ").strip()
            trailing_stop_pct_input = input("Enter trailing stop % as decimal or leave blank (example 0.04): ").strip()
            trailing_stop_amount_input = input("Enter trailing stop dollar amount from peak or leave blank (example 5): ").strip()

            result = execute_auto_exit(
                portfolio=portfolio,
                ticker=ticker,
                current_price=current_price,
                highest_price=highest_price,
                take_profit_pct=float(take_profit_pct_input) if take_profit_pct_input else None,
                take_profit_price=float(take_profit_price_input) if take_profit_price_input else None,
                stop_loss_pct=float(stop_loss_pct_input) if stop_loss_pct_input else None,
                stop_loss_price=float(stop_loss_price_input) if stop_loss_price_input else None,
                trailing_stop_pct=float(trailing_stop_pct_input) if trailing_stop_pct_input else None,
                trailing_stop_amount=float(trailing_stop_amount_input) if trailing_stop_amount_input else None,
            )

            print("\nPaper auto-sell result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

            updated_summary = get_portfolio_summary(portfolio)
            print("\nUpdated portfolio summary:")
            print(f"- cash: {updated_summary['cash']:.2f}")
            print(f"- open_positions: {updated_summary['position_count']}")
            print(f"- tickers_held: {updated_summary['tickers']}")
            print(f"- trade_count: {updated_summary['trade_count']}")

        elif choice == "21":
            print("\nAvailable trade-style matrix profiles:")
            for name in list_matrix_profiles():
                print(f"- {name}")

            profile_name = input("\nEnter trade-style matrix profile name: ").strip().lower()
            profile = get_matrix_profile(profile_name)

            if profile is None:
                print("Trade-style matrix profile not found.")
                continue

            print(f"\nTrade-style matrix profile: {profile_name}")
            for key, value in profile.items():
                print(f"- {key}: {value}")

        elif choice == "22":
            risk_profile_name = input("Enter risk profile name (passive/balanced/aggressive): ").strip().lower()
            trade_style_name = input("Enter trade-style name (quick_trade/short_hold) or leave blank: ").strip().lower()
            ticker = input("Enter ticker for override check or leave blank: ").strip().upper()

            rules = build_effective_rules(
                risk_profile_name=risk_profile_name,
                trade_style_name=trade_style_name if trade_style_name else None,
                ticker=ticker if ticker else None,
            )

            if rules is None:
                print("Could not build effective rules. Check your profile/style names.")
                continue

            print("\nMerged effective rules:")
            print(f"- risk_profile: {risk_profile_name}")
            print(f"- trade_style: {trade_style_name if trade_style_name else 'none'}")
            print(f"- ticker: {ticker if ticker else 'none'}")
            for key, value in rules.items():
                print(f"- {key}: {value}")

        elif choice == "23":
            risk_profile_name = input("Enter risk profile name (passive/balanced/aggressive): ").strip().lower()
            trade_style_name = input("Enter trade-style name (quick_trade/short_hold) or leave blank: ").strip().lower()
            ticker = input("Enter ticker for override check or leave blank: ").strip().upper()
            portfolio_cash = float(input("Enter portfolio cash: ").strip())
            position_size_dollars = float(input("Enter position size in dollars: ").strip())
            entry_price = float(input("Enter entry price: ").strip())

            result = evaluate_trade_with_effective_rules(
                risk_profile_name=risk_profile_name,
                trade_style_name=trade_style_name if trade_style_name else None,
                ticker=ticker if ticker else None,
                portfolio_cash=portfolio_cash,
                position_size_dollars=position_size_dollars,
                entry_price=entry_price,
            )

            print("\nMerged-rule trade decision result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

        elif choice == "24":
            ticker = input("Enter ticker: ").strip().upper()
            risk_profile_name = input("Enter risk profile name (passive/balanced/aggressive): ").strip().lower()
            trade_style_name = input("Enter trade-style name (quick_trade/short_hold) or leave blank: ").strip().lower()
            portfolio_cash = float(input("Enter portfolio cash: ").strip())
            position_size_dollars = float(input("Enter position size in dollars: ").strip())
            entry_price = float(input("Enter entry price: ").strip())

            result = execute_trade_with_effective_rules(
                portfolio=portfolio,
                ticker=ticker,
                risk_profile_name=risk_profile_name,
                trade_style_name=trade_style_name if trade_style_name else None,
                portfolio_cash=portfolio_cash,
                position_size_dollars=position_size_dollars,
                entry_price=entry_price,
            )

            print("\nMerged-rule paper trade execution result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

            updated_summary = get_portfolio_summary(portfolio)
            print("\nUpdated portfolio summary:")
            print(f"- cash: {updated_summary['cash']:.2f}")
            print(f"- open_positions: {updated_summary['position_count']}")
            print(f"- tickers_held: {updated_summary['tickers']}")
            print(f"- trade_count: {updated_summary['trade_count']}")

        elif choice == "25":
            ticker = input("Enter ticker with open position: ").strip().upper()
            risk_profile_name = input("Enter risk profile name (passive/balanced/aggressive): ").strip().lower()
            trade_style_name = input("Enter trade-style name (quick_trade/short_hold) or leave blank: ").strip().lower()
            current_price = float(input("Enter current price: ").strip())
            highest_price = float(input("Enter highest price reached: ").strip())

            result = evaluate_position_with_effective_rules(
                portfolio=portfolio,
                ticker=ticker,
                current_price=current_price,
                highest_price=highest_price,
                risk_profile_name=risk_profile_name,
                trade_style_name=trade_style_name if trade_style_name else None,
            )

            print("\nMerged-rule position exit result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

        elif choice == "26":
            title = input("Enter short title for the change request: ").strip()
            request_text = input("Enter the change you want the AI Builder to make: ").strip()
            priority = input("Enter priority (low/normal/high): ").strip().lower()

            if not title or not request_text:
                print("Title and request text are required.")
                continue

            if priority not in {"low", "normal", "high"}:
                priority = "normal"

            new_request = create_change_request(
                title=title,
                request_text=request_text,
                priority=priority,
            )

            print("\nSaved AI Builder request:")
            for key, value in new_request.items():
                print(f"- {key}: {value}")

        elif choice == "27":
            requests = load_change_requests()
            display_change_requests(requests)

        elif choice == "28":
            try:
                request_id = int(input("Enter request ID to update: ").strip())
            except ValueError:
                print("Request ID must be a number.")
                continue

            new_status = input("Enter new status (open/approved/closed): ").strip().lower()

            updated_request = update_change_request_status(request_id, new_status)

            if updated_request is None:
                print("Could not update request. Check the ID and status.")
                continue

            print("\nUpdated AI Builder request:")
            for key, value in updated_request.items():
                print(f"- {key}: {value}")

        elif choice == "29":
            approved_requests = get_approved_change_requests()
            display_change_requests(approved_requests)

        elif choice == "30":
            try:
                request_id = int(input("Enter approved request ID to queue: ").strip())
            except ValueError:
                print("Request ID must be a number.")
                continue

            queue_item = add_approved_request_to_queue(request_id)

            if queue_item is None:
                print("Could not queue request. Make sure it exists, is approved, and is not already queued.")
                continue

            print("\nQueued implementation item:")
            for key, value in queue_item.items():
                print(f"- {key}: {value}")

        elif choice == "31":
            queue_items = load_implementation_queue()
            display_implementation_queue(queue_items)

        elif choice == "32":
            try:
                queue_id = int(input("Enter queue ID to update: ").strip())
            except ValueError:
                print("Queue ID must be a number.")
                continue

            new_status = input(
                "Enter new queue status (ready/in_progress/completed): "
            ).strip().lower()

            updated_item = update_queue_item_status(queue_id, new_status)

            if updated_item is None:
                print("Could not update queue item. Check the queue ID and status.")
                continue

            print("\nUpdated implementation queue item:")
            for key, value in updated_item.items():
                print(f"- {key}: {value}")

        elif choice == "33":
            symbol = input("Enter stock symbol: ").strip().upper()
            feed = input("Enter feed (iex/delayed_sip/sip) or leave blank for iex: ").strip().lower()
            if not feed:
                feed = "iex"

            try:
                bar = get_latest_stock_bar(symbol, feed=feed)
            except Exception as exc:
                print(f"Error: {exc}")
                continue

            if bar is None:
                print("No stock bar data returned.")
                continue

            print("\nLatest stock bar:")
            for key, value in bar.items():
                print(f"- {key}: {value}")

        elif choice == "34":
            symbol = input("Enter crypto symbol (example BTC/USD): ").strip().upper()

            try:
                bar = get_latest_crypto_bar(symbol)
            except Exception as exc:
                print(f"Error: {exc}")
                continue

            if bar is None:
                print("No crypto bar data returned.")
                continue

            print("\nLatest crypto bar:")
            for key, value in bar.items():
                print(f"- {key}: {value}")

        elif choice == "35":
            feed = input("Enter stock feed (iex/delayed_sip/sip) or leave blank for iex: ").strip().lower()
            if not feed:
                feed = "iex"

            try:
                results = refresh_watchlist_market_data(feed=feed)
            except Exception as exc:
                print(f"Error: {exc}")
                continue

            display_watchlist_market_data(results)

        elif choice == "36":
            ticker = input("Enter ticker: ").strip().upper()
            risk_profile_name = input(
                "Enter risk profile name (passive/balanced/aggressive): "
            ).strip().lower()
            trade_style_name = input(
                "Enter trade-style name (quick_trade/short_hold) or leave blank: "
            ).strip().lower()
            portfolio_cash = float(input("Enter portfolio cash: ").strip())
            position_size_dollars = float(input("Enter position size in dollars: ").strip())
            feed = input("Enter stock feed (iex/delayed_sip/sip) or leave blank for iex. Ignored for crypto: ").strip().lower()

            if not feed:
                feed = "iex"

            try:
                result = evaluate_live_trade_with_effective_rules(
                    ticker=ticker,
                    risk_profile_name=risk_profile_name,
                    trade_style_name=trade_style_name if trade_style_name else None,
                    portfolio_cash=portfolio_cash,
                    position_size_dollars=position_size_dollars,
                    feed=feed,
                )
            except Exception as exc:
                print(f"Error: {exc}")
                continue

            print("\nLive merged-rule trade decision result:")
            for key, value in result.items():
                print(f"- {key}: {value}")
    
        elif choice == "37":
            ticker = input("Enter ticker: ").strip().upper()
            risk_profile_name = input(
                "Enter risk profile name (passive/balanced/aggressive): "
            ).strip().lower()
            trade_style_name = input(
                "Enter trade-style name (quick_trade/short_hold) or leave blank: "
            ).strip().lower()
            portfolio_cash = float(input("Enter portfolio cash: ").strip())
            position_size_dollars = float(input("Enter position size in dollars: ").strip())
            feed = input("Enter stock feed (iex/delayed_sip/sip) or leave blank for iex: ").strip().lower()

            if not feed:
                feed = "iex"

            try:
                result = execute_live_trade_with_effective_rules(
                    portfolio=portfolio,
                    ticker=ticker,
                    risk_profile_name=risk_profile_name,
                    trade_style_name=trade_style_name if trade_style_name else None,
                    portfolio_cash=portfolio_cash,
                    position_size_dollars=position_size_dollars,
                    feed=feed,
                )
            except Exception as exc:
                print(f"Error: {exc}")
                continue

            print("\nLive merged-rule paper trade execution result:")
            for key, value in result.items():
                print(f"- {key}: {value}")

            updated_summary = get_portfolio_summary(portfolio)
            print("\nUpdated portfolio summary:")
            print(f"- cash: {updated_summary['cash']:.2f}")
            print(f"- open_positions: {updated_summary['position_count']}")
            print(f"- tickers_held: {updated_summary['tickers']}")
            print(f"- trade_count: {updated_summary['trade_count']}")

        elif choice == "0":
            print("Exiting AI Portfolio Assistant.")
            break

        else:
            print("Invalid option. Please choose a valid menu number.")


if __name__ == "__main__":
    main()