from effective_rules import build_effective_rules


def evaluate_trade_with_effective_rules(
    risk_profile_name,
    portfolio_cash,
    position_size_dollars,
    entry_price,
    trade_style_name=None,
    ticker=None,
):
    rules = build_effective_rules(
        risk_profile_name=risk_profile_name,
        trade_style_name=trade_style_name,
        ticker=ticker,
    )

    if rules is None:
        return {
            "approved": False,
            "reason": "Could not build effective rules.",
        }

    max_position_size = portfolio_cash * rules["max_position_size_pct"]
    stop_loss_price = entry_price * (1 - rules["stop_loss_pct"])
    take_profit_price = entry_price * (1 + rules["take_profit_pct"])

    if position_size_dollars > max_position_size:
        return {
            "approved": False,
            "reason": "Position size is too large for the merged effective rules.",
            "rules": rules,
        }

    return {
        "approved": True,
        "reason": "Trade passes merged effective rules.",
        "rules": rules,
        "max_position_size": round(max_position_size, 2),
        "stop_loss_price": round(stop_loss_price, 2),
        "take_profit_price": round(take_profit_price, 2),
    }