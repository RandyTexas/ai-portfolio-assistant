from effective_rules import build_effective_rules
from manual_overrides import get_manual_ticker_override


def build_effective_rules_with_manual_override(
    risk_profile_name,
    trade_style_name=None,
    ticker=None,
):
    rules = build_effective_rules(
        risk_profile_name=risk_profile_name,
        trade_style_name=trade_style_name,
        ticker=ticker,
    )

    if rules is None:
        return None

    if not ticker:
        return rules

    manual_override = get_manual_ticker_override(ticker)

    if manual_override is None:
        return rules

    if not manual_override.get("enabled", True):
        return rules

    manual_rules = manual_override.get("rules", {})
    merged = dict(rules)
    merged.update(manual_rules)
    return merged