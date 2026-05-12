from override_merge import build_effective_rules_with_manual_override


def evaluate_trade_with_saved_override(
    ticker,
    risk_profile_name,
    portfolio_cash,
    position_size_dollars,
    entry_price,
    trade_style_name=None,
):
    merged_result = build_effective_rules_with_manual_override(
        risk_profile_name=risk_profile_name,
        trade_style_name=trade_style_name,
        ticker=ticker,
    )

    if merged_result is None:
        return {
            "approved": False,
            "reason": "Could not build effective rules.",
        }

    rules = merged_result["rules"]
    max_position_size = portfolio_cash * rules["max_position_size_pct"]

    if position_size_dollars > max_position_size:
        return {
            "approved": False,
            "reason": "Position size is too large for the effective rules.",
            "max_position_size": max_position_size,
            "stop_loss_price": entry_price * (1 - rules["stop_loss_pct"]),
            "take_profit_price": entry_price * (1 + rules["take_profit_pct"]),
            "rules_used": rules,
            "manual_override_found": merged_result["manual_override_found"],
            "manual_override_enabled": merged_result["manual_override_enabled"],
            "manual_override_applied": merged_result["manual_override_applied"],
            "manual_override_name": merged_result["manual_override_name"],
            "manual_override_rules": merged_result["manual_override_rules"],
        }

    return {
        "approved": True,
        "reason": "Trade passes effective rules.",
        "max_position_size": max_position_size,
        "stop_loss_price": entry_price * (1 - rules["stop_loss_pct"]),
        "take_profit_price": entry_price * (1 + rules["take_profit_pct"]),
        "rules_used": rules,
        "manual_override_found": merged_result["manual_override_found"],
        "manual_override_enabled": merged_result["manual_override_enabled"],
        "manual_override_applied": merged_result["manual_override_applied"],
        "manual_override_name": merged_result["manual_override_name"],
        "manual_override_rules": merged_result["manual_override_rules"],
    }