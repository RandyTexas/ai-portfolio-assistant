from exit_rules import evaluate_exit_rules


def evaluate_position_exit(
    portfolio,
    ticker,
    current_price,
    highest_price,
    take_profit_pct=None,
    take_profit_price=None,
    stop_loss_pct=None,
    stop_loss_price=None,
    trailing_stop_pct=None,
    trailing_stop_amount=None,
):
    ticker = ticker.strip().upper()

    if ticker not in portfolio["positions"]:
        return {
            "exit": False,
            "reason": f"No open position found for {ticker}.",
            "ticker": ticker,
        }

    position = portfolio["positions"][ticker]
    entry_price = position["average_price"]
    shares = position["shares"]

    exit_result = evaluate_exit_rules(
        entry_price=entry_price,
        current_price=current_price,
        highest_price=highest_price,
        take_profit_pct=take_profit_pct,
        take_profit_price=take_profit_price,
        stop_loss_pct=stop_loss_pct,
        stop_loss_price=stop_loss_price,
        trailing_stop_pct=trailing_stop_pct,
        trailing_stop_amount=trailing_stop_amount,
    )

    return {
        "ticker": ticker,
        "shares": shares,
        "entry_price": round(entry_price, 2),
        "current_price": round(float(current_price), 2),
        "highest_price": round(float(highest_price), 2),
        "exit": exit_result["exit"],
        "reason": exit_result["reason"],
        "exit_type": exit_result.get("exit_type"),
        "active_take_profit_price": exit_result.get("active_take_profit_price"),
        "active_stop_loss_price": exit_result.get("active_stop_loss_price"),
        "active_trailing_stop_price": exit_result.get("active_trailing_stop_price"),
    }