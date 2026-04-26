def create_paper_portfolio(starting_cash=10000.0):
    return {
        "cash": float(starting_cash),
        "positions": {},
        "trade_history": [],
    }


def paper_buy(portfolio, ticker, price, shares):
    ticker = ticker.strip().upper()
    price = float(price)
    shares = int(shares)

    total_cost = price * shares

    if shares <= 0:
        return False, "Shares must be greater than 0."

    if price <= 0:
        return False, "Price must be greater than 0."

    if total_cost > portfolio["cash"]:
        return False, "Not enough cash."

    portfolio["cash"] -= total_cost

    if ticker not in portfolio["positions"]:
        portfolio["positions"][ticker] = {
            "shares": 0,
            "average_price": 0.0,
        }

    current_shares = portfolio["positions"][ticker]["shares"]
    current_avg = portfolio["positions"][ticker]["average_price"]

    new_total_shares = current_shares + shares
    new_total_cost = (current_shares * current_avg) + total_cost
    new_average_price = new_total_cost / new_total_shares

    portfolio["positions"][ticker]["shares"] = new_total_shares
    portfolio["positions"][ticker]["average_price"] = new_average_price

    portfolio["trade_history"].append(
        {
            "action": "BUY",
            "ticker": ticker,
            "price": price,
            "shares": shares,
            "total": total_cost,
        }
    )

    return True, f"Bought {shares} shares of {ticker} at {price:.2f}."


def paper_sell(portfolio, ticker, price, shares):
    ticker = ticker.strip().upper()
    price = float(price)
    shares = int(shares)

    if shares <= 0:
        return False, "Shares must be greater than 0."

    if price <= 0:
        return False, "Price must be greater than 0."

    if ticker not in portfolio["positions"]:
        return False, f"No position found for {ticker}."

    owned_shares = portfolio["positions"][ticker]["shares"]

    if shares > owned_shares:
        return False, f"Not enough shares of {ticker} to sell."

    total_value = price * shares
    portfolio["cash"] += total_value
    portfolio["positions"][ticker]["shares"] -= shares

    portfolio["trade_history"].append(
        {
            "action": "SELL",
            "ticker": ticker,
            "price": price,
            "shares": shares,
            "total": total_value,
        }
    )

    if portfolio["positions"][ticker]["shares"] == 0:
        del portfolio["positions"][ticker]

    return True, f"Sold {shares} shares of {ticker} at {price:.2f}."


def get_portfolio_summary(portfolio):
    return {
        "cash": round(portfolio["cash"], 2),
        "position_count": len(portfolio["positions"]),
        "tickers": sorted(portfolio["positions"].keys()),
        "trade_count": len(portfolio["trade_history"]),
    }