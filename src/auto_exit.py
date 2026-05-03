from paper_trading import paper_sell
from position_exit import evaluate_position_exit


def execute_auto_exit(
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
    exit_result = evaluate_position_exit(
        portfolio=portfolio,
        ticker=ticker,
        current_price=current_price,
        highest_price=highest_price,
        take_profit_pct=take_profit_pct,
        take_profit_price=take_profit_price,
        stop_loss_pct=stop_loss_pct,
        stop_loss_price=stop_loss_price,
        trailing_stop_pct=trailing_stop_pct,
        trailing_stop_amount=trailing_stop_amount,
    )

    if exit_result["exit"] is False:
        return {
            "sold": False,
            "reason": exit_result["reason"],
            "exit_result": exit_result,
        }

    shares = exit_result["shares"]
    success, message = paper_sell(portfolio, ticker, current_price, shares)

    return {
        "sold": success,
        "reason": message,
        "exit_result": exit_result,
        "shares_sold": shares if success else 0,
    }