from auto_exit import execute_auto_exit
from paper_trading import create_paper_portfolio, paper_buy


def test_auto_exit_rejects_missing_position():
    portfolio = create_paper_portfolio()

    result = execute_auto_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=108,
        highest_price=110,
        take_profit_pct=0.08,
    )

    assert result["sold"] is False
    assert result["reason"] == "No open position found for AAPL."


def test_auto_exit_does_not_sell_when_no_exit_triggered():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    result = execute_auto_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=103,
        highest_price=104,
        take_profit_pct=0.08,
        stop_loss_pct=0.05,
        trailing_stop_pct=0.04,
    )

    assert result["sold"] is False
    assert result["reason"] == "No exit rule triggered."
    assert portfolio["positions"]["AAPL"]["shares"] == 5


def test_auto_exit_sells_on_take_profit():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    result = execute_auto_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=108,
        highest_price=110,
        take_profit_pct=0.08,
    )

    assert result["sold"] is True
    assert result["shares_sold"] == 5
    assert result["reason"] == "Sold 5 shares of AAPL at 108.00."
    assert "AAPL" not in portfolio["positions"]


def test_auto_exit_sells_on_stop_loss():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    result = execute_auto_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=95,
        highest_price=102,
        stop_loss_pct=0.05,
    )

    assert result["sold"] is True
    assert result["shares_sold"] == 5
    assert result["exit_result"]["exit_type"] == "stop_loss"
    assert "AAPL" not in portfolio["positions"]


def test_auto_exit_sells_on_trailing_stop():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    result = execute_auto_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=105.6,
        highest_price=110,
        trailing_stop_pct=0.04,
    )

    assert result["sold"] is True
    assert result["shares_sold"] == 5
    assert result["exit_result"]["exit_type"] == "trailing_stop"
    assert "AAPL" not in portfolio["positions"]
    