from trade_decision import evaluate_paper_trade_decision


def test_trade_decision_rejects_missing_strategy():
    result = evaluate_paper_trade_decision(
        strategy_name="unknown",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=95,
        take_profit_price=110,
    )

    assert result["approved_for_paper_trade"] is False
    assert result["reason"] == "Strategy profile not found."


def test_trade_decision_rejects_oversized_position():
    result = evaluate_paper_trade_decision(
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=1500,
        entry_price=100,
        stop_loss_price=96,
        take_profit_price=108,
    )

    assert result["approved_for_paper_trade"] is False
    assert result["reason"] == "Position size is too large for this strategy."


def test_trade_decision_rejects_wide_stop_loss():
    result = evaluate_paper_trade_decision(
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=90,
        take_profit_price=108,
    )

    assert result["approved_for_paper_trade"] is False
    assert result["reason"] == "Stop loss is wider than allowed for this strategy."


def test_trade_decision_rejects_small_take_profit():
    result = evaluate_paper_trade_decision(
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=96,
        take_profit_price=104,
    )

    assert result["approved_for_paper_trade"] is False
    assert result["reason"] == "Take profit target is smaller than the strategy requires."


def test_trade_decision_approves_valid_setup():
    result = evaluate_paper_trade_decision(
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=96,
        take_profit_price=108,
    )

    assert result["approved_for_paper_trade"] is True
    assert result["reason"] == "Trade approved for paper trading."
    assert result["evaluation"]["approved"] is True
    assert result["evaluation"]["max_position_size"] == 1000.0
    assert result["evaluation"]["stop_loss_pct"] == 0.04
    assert result["evaluation"]["take_profit_pct"] == 0.08
    