from effective_rules import build_effective_rules


def test_build_effective_rules_with_risk_profile_only():
    rules = build_effective_rules("balanced")

    assert rules is not None
    assert rules["take_profit_pct"] == 0.08
    assert rules["stop_loss_pct"] == 0.05
    assert rules["trailing_stop_pct"] == 0.04
    assert rules["max_position_size_pct"] == 0.10


def test_build_effective_rules_with_trade_style_override():
    rules = build_effective_rules("balanced", "quick_trade")

    assert rules is not None
    assert rules["take_profit_pct"] == 0.03
    assert rules["stop_loss_pct"] == 0.02
    assert rules["trailing_stop_pct"] == 0.02
    assert rules["max_position_size_pct"] == 0.05


def test_build_effective_rules_with_ticker_override():
    rules = build_effective_rules("balanced", None, "NVDA")

    assert rules is not None
    assert rules["take_profit_pct"] == 0.10
    assert rules["stop_loss_pct"] == 0.03
    assert rules["trailing_stop_pct"] == 0.03
    assert rules["max_position_size_pct"] == 0.10


def test_build_effective_rules_with_trade_style_and_ticker_override():
    rules = build_effective_rules("balanced", "quick_trade", "NVDA")

    assert rules is not None
    assert rules["take_profit_pct"] == 0.10
    assert rules["stop_loss_pct"] == 0.03
    assert rules["trailing_stop_pct"] == 0.03
    assert rules["max_position_size_pct"] == 0.05


def test_build_effective_rules_returns_none_for_bad_risk_profile():
    rules = build_effective_rules("unknown")

    assert rules is None


def test_build_effective_rules_returns_none_for_bad_trade_style():
    rules = build_effective_rules("balanced", "unknown_style")

    assert rules is None
    