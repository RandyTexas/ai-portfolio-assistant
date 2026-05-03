from merged_trade_decision import evaluate_trade_with_effective_rules


def test_merged_trade_decision_rejects_bad_profile():
    result = evaluate_trade_with_effective_rules(
        risk_profile_name="unknown",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
    )

    assert result["approved"] is False
    assert result["reason"] == "Could not build effective rules."


def test_merged_trade_decision_approves_balanced_trade():
    result = evaluate_trade_with_effective_rules(
        risk_profile_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
    )

    assert result["approved"] is True
    assert result["reason"] == "Trade passes merged effective rules."
    assert result["max_position_size"] == 1000.0
    assert result["stop_loss_price"] == 95.0
    assert result["take_profit_price"] == 108.0


def test_merged_trade_decision_uses_trade_style_override():
    result = evaluate_trade_with_effective_rules(
        risk_profile_name="balanced",
        trade_style_name="quick_trade",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
    )

    assert result["approved"] is True
    assert result["max_position_size"] == 500.0
    assert result["stop_loss_price"] == 98.0
    assert result["take_profit_price"] == 103.0


def test_merged_trade_decision_uses_ticker_override():
    result = evaluate_trade_with_effective_rules(
        risk_profile_name="balanced",
        ticker="NVDA",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
    )

    assert result["approved"] is True
    assert result["stop_loss_price"] == 97.0
    assert result["take_profit_price"] == 110.0


def test_merged_trade_decision_rejects_oversized_trade():
    result = evaluate_trade_with_effective_rules(
        risk_profile_name="balanced",
        trade_style_name="quick_trade",
        portfolio_cash=10000,
        position_size_dollars=600,
        entry_price=100,
    )

    assert result["approved"] is False
    assert result["reason"] == "Position size is too large for the merged effective rules."