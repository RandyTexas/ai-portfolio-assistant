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

    result = {
        "rules": rules,
        "manual_override_found": False,
        "manual_override_enabled": False,
        "manual_override_applied": False,
        "manual_override_name": None,
        "manual_override_rules": {},
    }

    if not ticker:
        return result

    manual_override = get_manual_ticker_override(ticker)

    if manual_override is None:
        return result

    result["manual_override_found"] = True
    result["manual_override_enabled"] = manual_override.get("enabled", True)
    result["manual_override_name"] = manual_override.get(
        "name", f"{ticker} manual override"
    )
    result["manual_override_rules"] = manual_override.get("rules", {})

    if not result["manual_override_enabled"]:
        return result

    merged = dict(rules)
    merged.update(result["manual_override_rules"])

    result["rules"] = merged
    result["manual_override_applied"] = True
    return result