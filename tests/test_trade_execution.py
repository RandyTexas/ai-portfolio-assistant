from paper_trading import create_paper_portfolio
from trade_execution import execute_paper_trade


def test_execute_paper_trade_rejects_invalid_setup():
    portfolio = create_paper_portfolio()

    result = execute_paper_trade(
        portfolio=portfolio,
        ticker="AAPL",
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=1500,
        entry_price=100,
        stop_loss_price=96,
        take_profit_price=108,
    )

    assert result["executed"] is False
    assert result["reason"] == "Position size is too large for this strategy."
    assert portfolio["cash"] == 10000.0
    assert portfolio["positions"] == {}


def test_execute_paper_trade_approves_and_buys():
    portfolio = create_paper_portfolio()

    result = execute_paper_trade(
        portfolio=portfolio,
        ticker="AAPL",
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        entry_price=100,
        stop_loss_price=96,
        take_profit_price=108,
    )

    assert result["executed"] is True
    assert result["reason"] == "Bought 5 shares of AAPL at 100.00."
    assert result["shares_bought"] == 5
    assert portfolio["cash"] == 9500.0
    assert portfolio["positions"]["AAPL"]["shares"] == 5


def test_execute_paper_trade_rejects_too_small_position_size():
    portfolio = create_paper_portfolio()

    result = execute_paper_trade(
        portfolio=portfolio,
        ticker="AAPL",
        strategy_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=50,
        entry_price=100,
        stop_loss_price=96,
        take_profit_price=108,
    )

    assert result["executed"] is False
    assert result["reason"] == "Position size is too small to buy at least 1 share."
    assert portfolio["cash"] == 10000.0
    assert portfolio["positions"] == {}