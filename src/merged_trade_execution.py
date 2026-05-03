from merged_trade_decision import evaluate_trade_with_effective_rules
from paper_trading import paper_buy


def execute_trade_with_effective_rules(
    portfolio,
    ticker,
    risk_profile_name,
    portfolio_cash,
    position_size_dollars,
    entry_price,
    trade_style_name=None,
):
    decision = evaluate_trade_with_effective_rules(
        risk_profile_name=risk_profile_name,
        trade_style_name=trade_style_name,
        ticker=ticker,
        portfolio_cash=portfolio_cash,
        position_size_dollars=position_size_dollars,
        entry_price=entry_price,
    )

    if decision["approved"] is False:
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