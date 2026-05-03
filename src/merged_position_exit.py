from effective_rules import build_effective_rules
from position_exit import evaluate_position_exit


def evaluate_position_with_effective_rules(
    portfolio,
    ticker,
    current_price,
    highest_price,
    risk_profile_name,
    trade_style_name=None,
):
    rules = build_effective_rules(
        risk_profile_name=risk_profile_name,
        trade_style_name=trade_style_name,
        ticker=ticker,
    )

    if rules is None:
        return {
            "exit": False,
            "reason": "Could not build effective rules.",
        }

    result = evaluate_position_exit(
        portfolio=portfolio,
        ticker=ticker,
        current_price=current_price,
        highest_price=highest_price,
        take_profit_pct=rules.get("take_profit_pct"),
        stop_loss_pct=rules.get("stop_loss_pct"),
        trailing_stop_pct=rules.get("trailing_stop_pct"),
    )

    return {
        **result,
        "rules": rules,
    }