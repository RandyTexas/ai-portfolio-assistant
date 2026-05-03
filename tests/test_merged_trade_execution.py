from merged_trade_execution import execute_trade_with_effective_rules
from paper_trading import create_paper_portfolio


def test_merged_trade_execution_rejects_bad_profile():
    portfolio = create_paper_portfolio()

    result = execute_trade_with_effective_rules(
        portfolio=portfolio,
        ticker="AAPL",
        risk_profile_name="unknown",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
    )

    assert result["executed"] is False
    assert result["reason"] == "Could not build effective rules."


def test_merged_trade_execution_rejects_oversized_trade():
    portfolio = create_paper_portfolio()

    result = execute_trade_with_effective_rules(
        portfolio=portfolio,
        ticker="AAPL",
        risk_profile_name="balanced",
        trade_style_name="quick_trade",
        portfolio_cash=10000,
        position_size_dollars=600,
        entry_price=100,
    )

    assert result["executed"] is False
    assert result["reason"] == "Position size is too large for the merged effective rules."


def test_merged_trade_execution_rejects_too_small_position():
    portfolio = create_paper_portfolio()

    result = execute_trade_with_effective_rules(
        portfolio=portfolio,
        ticker="AAPL",
        risk_profile_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=50,
        entry_price=100,
    )

    assert result["executed"] is False
    assert result["reason"] == "Position size is too small to buy at least 1 share."


def test_merged_trade_execution_executes_trade():
    portfolio = create_paper_portfolio()

    result = execute_trade_with_effective_rules(
        portfolio=portfolio,
        ticker="AAPL",
        risk_profile_name="balanced",
        trade_style_name="quick_trade",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
    )

    assert result["executed"] is True
    assert result["shares_bought"] == 5
    assert result["reason"] == "Bought 5 shares of AAPL at 100.00."
    assert portfolio["cash"] == 9500.0
    assert portfolio["positions"]["AAPL"]["shares"] == 5