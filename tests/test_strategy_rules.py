from strategy_rules import evaluate_trade_setup


def test_rejects_missing_strategy():
    result = evaluate_trade_setup(
        strategy_name="unknown",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=95,
        take_profit_price=110,
    )

    assert result["approved"] is False
    assert result["reason"] == "Strategy profile not found."


def test_rejects_non_positive_cash():
    result = evaluate_trade_setup(
        strategy_name="balanced",
        portfolio_cash=0,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=95,
        take_profit_price=110,
    )

    assert result["approved"] is False
    assert result["reason"] == "Portfolio cash must be greater than 0."


def test_rejects_non_positive_prices():
    result = evaluate_trade_setup(
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=0,
        stop_loss_price=95,
        take_profit_price=110,
    )

    assert result["approved"] is False
    assert result["reason"] == "Prices must be greater than 0."


def test_rejects_position_size_too_large():
    result = evaluate_trade_setup(
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=1500,
        entry_price=100,
        stop_loss_price=96,
        take_profit_price=108,
    )

    assert result["approved"] is False
    assert result["reason"] == "Position size is too large for this strategy."


def test_rejects_stop_loss_too_wide():
    result = evaluate_trade_setup(
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=90,
        take_profit_price=108,
    )

    assert result["approved"] is False
    assert result["reason"] == "Stop loss is wider than allowed for this strategy."


def test_rejects_take_profit_too_small():
    result = evaluate_trade_setup(
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=96,
        take_profit_price=104,
    )

    assert result["approved"] is False
    assert result["reason"] == "Take profit target is smaller than the strategy requires."


def test_approves_valid_balanced_setup():
    result = evaluate_trade_setup(
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=96,
        take_profit_price=108,
    )

    assert result["approved"] is True
    assert result["reason"] == "Trade setup passes the basic strategy checks."
    assert result["max_position_size"] == 1000.0
    assert result["stop_loss_pct"] == 0.04
    assert result["take_profit_pct"] == 0.08