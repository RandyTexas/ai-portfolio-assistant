from trade_decision import evaluate_paper_trade_decision
from paper_trading import paper_buy


def execute_paper_trade(
    portfolio,
    ticker,
    strategy_name,
    portfolio_cash,
    position_size_dollars,
    entry_price,
    stop_loss_price,
    take_profit_price,
):
    decision = evaluate_paper_trade_decision(
        strategy_name=strategy_name,
        portfolio_cash=portfolio_cash,
        position_size_dollars=position_size_dollars,
        entry_price=entry_price,
        stop_loss_price=stop_loss_price,
        take_profit_price=take_profit_price,
    )

    if decision["approved_for_paper_trade"] is False:
        return {
            "executed": False,
            "reason": decision["reason"],
            "decision": decision,
        }

    shares = int(position_size_dollars // entry_price)

    if shares <= 0:
        return {
            "executed": False,
            "reason": "Position size is too small to buy at least 1 share.",
            "decision": decision,
        }

    success, message = paper_buy(portfolio, ticker, entry_price, shares)

    return {
        "executed": success,
        "reason": message,
        "shares_bought": shares if success else 0,
        "decision": decision,
    }