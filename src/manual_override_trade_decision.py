from override_merge import build_effective_rules_with_manual_override


def evaluate_trade_with_saved_override(
    ticker,
    risk_profile_name,
    portfolio_cash,
    position_size_dollars,
    entry_price,
    trade_style_name=None,
):
    rules = build_effective_rules_with_manual_override(
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

    if position_size_dollars > max_position_size:
        return {
            "approved": False,
            "reason": "Position size is too large for the effective rules.",
            "max_position_size": max_position_size,
            "stop_loss_price": entry_price * (1 - rules["stop_loss_pct"]),
            "take_profit_price": entry_price * (1 + rules["take_profit_pct"]),
            "rules_used": rules,
        }

    return {
        "approved": True,
        "reason": "Trade passes effective rules.",
        "max_position_size": max_position_size,
        "stop_loss_price": entry_price * (1 - rules["stop_loss_pct"]),
        "take_profit_price": entry_price * (1 + rules["take_profit_pct"]),
        "rules_used": rules,
    }